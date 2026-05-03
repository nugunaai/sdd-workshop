"""tests/integration/test_cli_persistence.py: 앱 재시작 후 데이터 지속성 테스트 (T039).
NOTE: 구현 전 Red 상태로 먼저 작성한다.
"""
import pytest
from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def patch_db(monkeypatch, tmp_path):
    """각 테스트마다 독립된 임시 DB 경로를 사용하도록 패치한다."""
    db_file = str(tmp_path / "persist.db")
    monkeypatch.setattr("cli.main.DB_PATH", db_file)


def test_persistence_after_restart():
    """항목 추가 후 새 invocation(앱 재시작 시뮬레이션)으로 조회해도 항목이 유지된다."""
    # 항목 추가 (첫 번째 invocation)
    result_add = runner.invoke(app, ["add", "지속성 테스트 항목"])
    assert result_add.exit_code == 0

    # 새 invocation으로 목록 조회 (앱 재시작 시뮬레이션)
    result_list = runner.invoke(app, ["list"])
    assert result_list.exit_code == 0
    assert "지속성 테스트 항목" in result_list.output


def test_multiple_items_persist():
    """여러 항목을 추가한 뒤 재시작해도 모두 유지된다."""
    runner.invoke(app, ["add", "항목 A"])
    runner.invoke(app, ["add", "항목 B"])
    runner.invoke(app, ["add", "항목 C"])

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "항목 A" in result.output
    assert "항목 B" in result.output
    assert "항목 C" in result.output


# --- T028: 마이그레이션 안전성 및 legacy row 정규화 테스트 ---

def test_migration_is_idempotent(monkeypatch, tmp_path):
    """init_db를 두 번 호출해도 오류 없이 실행된다(idempotent)."""
    from todo_lib.db import get_engine, init_db

    db_file = str(tmp_path / "idempotent.db")
    monkeypatch.setattr("cli.main.DB_PATH", db_file)
    engine = get_engine(db_file)
    # 두 번 연속 호출해도 예외가 발생하지 않아야 한다
    init_db(engine)
    init_db(engine)


def test_legacy_row_tags_normalized_to_empty_list(monkeypatch, tmp_path):
    """tags 컬럼이 없는 legacy DB에서 앱 시작 시 마이그레이션이 적용되고
    기존 행의 tags가 빈 리스트로 정규화된다."""
    import sqlite3
    from todo_lib.db import get_engine, init_db, get_session_factory
    from todo_lib.repository import get_all_todos

    db_file = str(tmp_path / "legacy.db")
    monkeypatch.setattr("cli.main.DB_PATH", db_file)

    # tags 컬럼 없는 legacy 테이블 수동 생성
    conn = sqlite3.connect(db_file)
    conn.execute(
        "CREATE TABLE todo_items ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title TEXT NOT NULL, "
        "due_date DATE, "
        "priority TEXT, "
        "is_done BOOLEAN NOT NULL DEFAULT 0, "
        "created_at DATETIME NOT NULL, "
        "completed_at DATETIME"
        ")"
    )
    conn.execute(
        "INSERT INTO todo_items (title, is_done, created_at) "
        "VALUES ('레거시 항목', 0, '2024-01-01 00:00:00')"
    )
    conn.commit()
    conn.close()

    # 앱 시작 시 init_db 호출 → 마이그레이션 적용
    engine = get_engine(db_file)
    init_db(engine)

    Session = get_session_factory(engine)
    session = Session()
    try:
        items = get_all_todos(session)
        assert len(items) == 1
        # legacy row의 tags는 빈 리스트로 정규화되어야 한다
        assert items[0].tags == []
    finally:
        session.close()
