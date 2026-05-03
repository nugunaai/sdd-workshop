"""tests/integration/test_cli_done.py: todo done CLI 통합 테스트 (T026, T040)."""
import re

import pytest
from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def patch_db(monkeypatch, tmp_path):
    """각 테스트마다 독립된 임시 DB 경로를 사용하도록 패치한다."""
    monkeypatch.setattr("cli.main.DB_PATH", str(tmp_path / "test.db"))


def _add_item(title: str = "테스트 항목") -> str:
    """항목을 추가하고 생성된 ID를 반환한다."""
    r = runner.invoke(app, ["add", title])
    m = re.search(r"ID: (\d+)", r.output)
    assert m, f"ID를 찾을 수 없습니다: {r.output}"
    return m.group(1)


def test_done_success():
    """미완료 항목 완료 처리 시 성공 메시지가 출력된다."""
    item_id = _add_item()
    result = runner.invoke(app, ["done", item_id])
    assert result.exit_code == 0
    assert f"항목 {item_id}가 완료 처리되었습니다" in result.output


def test_done_updates_status():
    """완료 처리 후 목록에서 해당 항목이 완료로 표시된다."""
    item_id = _add_item("완료 상태 확인")
    runner.invoke(app, ["done", item_id])
    result = runner.invoke(app, ["list", "--filter", "done"])
    assert "완료 상태 확인" in result.output


def test_done_already_done():
    """이미 완료된 항목에 완료 처리 시 안내 메시지와 exit code 1이 반환된다."""
    item_id = _add_item()
    runner.invoke(app, ["done", item_id])
    result = runner.invoke(app, ["done", item_id])
    assert result.exit_code == 1
    assert f"항목 {item_id}는 이미 완료된 항목입니다" in result.output


def test_done_not_found():
    """존재하지 않는 ID는 오류 메시지와 exit code 1을 반환한다."""
    result = runner.invoke(app, ["done", "999"])
    assert result.exit_code == 1
    assert "찾을 수 없습니다" in result.output


# T040: non-numeric ID 입력 테스트
def test_done_nonnumeric_id():
    """숫자가 아닌 ID는 'ID는 숫자여야 합니다' 오류 메시지와 exit code 1을 반환한다."""
    result = runner.invoke(app, ["done", "abc"])
    assert result.exit_code == 1
    assert "ID는 숫자여야 합니다" in result.output


def test_done_nonnumeric_id_special_chars():
    """특수문자 ID도 올바르게 거부된다."""
    result = runner.invoke(app, ["done", "1a2b"])
    assert result.exit_code == 1
    assert "ID는 숫자여야 합니다" in result.output
