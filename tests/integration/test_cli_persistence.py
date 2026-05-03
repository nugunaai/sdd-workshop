"""tests/integration/test_cli_persistence.py: 앱 재시작 후 데이터 지속성 테스트 (T039).
NOTE: 구현 전 Red 상태로 먼저 작성한다.
"""
import pytest
from typer.testing import CliRunner

from cli.main import app

runner = CliRunner(mix_stderr=True)


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
