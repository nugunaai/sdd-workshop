"""tests/integration/test_cli_delete.py: todo delete CLI 통합 테스트 (T031, T041)."""
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


def test_delete_success():
    """항목을 삭제하면 성공 메시지가 출력된다."""
    item_id = _add_item()
    result = runner.invoke(app, ["delete", item_id])
    assert result.exit_code == 0
    assert f"항목 {item_id}가 삭제되었습니다" in result.output


def test_delete_removes_from_list():
    """삭제 후 목록 조회 시 해당 항목이 나타나지 않는다."""
    item_id = _add_item("삭제될 항목")
    runner.invoke(app, ["delete", item_id])
    result = runner.invoke(app, ["list"])
    assert "삭제될 항목" not in result.output


def test_delete_not_found():
    """존재하지 않는 ID는 오류 메시지와 exit code 1을 반환한다."""
    result = runner.invoke(app, ["delete", "999"])
    assert result.exit_code == 1
    assert "찾을 수 없습니다" in result.output


def test_delete_keeps_other_items():
    """삭제는 대상 항목만 제거하고 다른 항목은 유지한다."""
    _add_item("유지할 항목")
    item_id = _add_item("삭제될 항목")
    runner.invoke(app, ["delete", item_id])

    result = runner.invoke(app, ["list"])
    assert "유지할 항목" in result.output
    assert "삭제될 항목" not in result.output


# T041: non-numeric ID 입력 테스트
def test_delete_nonnumeric_id():
    """숫자가 아닌 ID는 'ID는 숫자여야 합니다' 오류 메시지와 exit code 1을 반환한다."""
    result = runner.invoke(app, ["delete", "abc"])
    assert result.exit_code == 1
    assert "ID는 숫자여야 합니다" in result.output


def test_delete_nonnumeric_id_special_chars():
    """특수문자 ID도 올바르게 거부된다."""
    result = runner.invoke(app, ["delete", "1a"])
    assert result.exit_code == 1
    assert "ID는 숫자여야 합니다" in result.output
