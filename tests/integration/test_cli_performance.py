"""tests/integration/test_cli_performance.py: SC-001/SC-005 성능 기준 테스트 (T042, T043)."""
import time

import pytest
from typer.testing import CliRunner

from cli.main import app
from todo_lib.db import get_engine, get_session_factory, init_db
from todo_lib.service import add_todo

runner = CliRunner(mix_stderr=True)


@pytest.fixture
def db_with_1000_items(monkeypatch, tmp_path):
    """1,000개 항목이 미리 저장된 임시 DB를 준비하고 DB_PATH를 패치한다."""
    db_file = str(tmp_path / "perf.db")
    monkeypatch.setattr("cli.main.DB_PATH", db_file)

    engine = get_engine(db_file)
    init_db(engine)
    Session = get_session_factory(engine)
    session = Session()
    for i in range(1000):
        add_todo(session, title=f"항목 {i + 1}")
    session.close()
    engine.dispose()

    return db_file


# T042: SC-001 단일 명령 30초 이내 완료 기준
def test_sc001_add_within_30s(monkeypatch, tmp_path):
    """SC-001: add 명령이 30초 이내에 완료된다."""
    monkeypatch.setattr("cli.main.DB_PATH", str(tmp_path / "sc001.db"))

    start = time.perf_counter()
    result = runner.invoke(app, ["add", "성능 테스트 항목"])
    elapsed = time.perf_counter() - start

    assert result.exit_code == 0
    assert elapsed < 30.0, f"add 명령이 {elapsed:.2f}초 소요됨 (한도: 30초)"


def test_sc001_list_within_30s(monkeypatch, tmp_path):
    """SC-001: list 명령이 30초 이내에 완료된다."""
    monkeypatch.setattr("cli.main.DB_PATH", str(tmp_path / "sc001_list.db"))
    runner.invoke(app, ["add", "항목"])

    start = time.perf_counter()
    result = runner.invoke(app, ["list"])
    elapsed = time.perf_counter() - start

    assert result.exit_code == 0
    assert elapsed < 30.0, f"list 명령이 {elapsed:.2f}초 소요됨 (한도: 30초)"


# T043: SC-005 1,000개 항목 기준 1초 이내 응답
def test_sc005_list_1000_items_within_1s(db_with_1000_items):
    """SC-005: 1,000개 항목 상태에서 list가 1초 이내에 응답한다."""
    start = time.perf_counter()
    result = runner.invoke(app, ["list"])
    elapsed = time.perf_counter() - start

    assert result.exit_code == 0
    assert elapsed < 1.0, f"list 명령이 {elapsed:.2f}초 소요됨 (한도: 1초)"


def test_sc005_add_with_1000_items_within_1s(db_with_1000_items):
    """SC-005: 1,000개 항목 상태에서 add가 1초 이내에 응답한다."""
    start = time.perf_counter()
    result = runner.invoke(app, ["add", "1001번째 항목"])
    elapsed = time.perf_counter() - start

    assert result.exit_code == 0
    assert elapsed < 1.0, f"add 명령이 {elapsed:.2f}초 소요됨 (한도: 1초)"


def test_sc005_done_with_1000_items_within_1s(db_with_1000_items):
    """SC-005: 1,000개 항목 상태에서 done이 1초 이내에 응답한다."""
    start = time.perf_counter()
    result = runner.invoke(app, ["done", "1"])
    elapsed = time.perf_counter() - start

    assert result.exit_code == 0
    assert elapsed < 1.0, f"done 명령이 {elapsed:.2f}초 소요됨 (한도: 1초)"


def test_sc005_delete_with_1000_items_within_1s(db_with_1000_items):
    """SC-005: 1,000개 항목 상태에서 delete가 1초 이내에 응답한다."""
    start = time.perf_counter()
    result = runner.invoke(app, ["delete", "1"])
    elapsed = time.perf_counter() - start

    assert result.exit_code == 0
    assert elapsed < 1.0, f"delete 명령이 {elapsed:.2f}초 소요됨 (한도: 1초)"
