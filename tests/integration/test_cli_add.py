"""tests/integration/test_cli_add.py: todo add CLI 통합 테스트 (T015).
NOTE: 구현 전 Red 상태로 먼저 작성한다.
"""
import pytest
from typer.testing import CliRunner

from cli.main import app

# mix_stderr=True: stdout과 stderr를 result.output으로 함께 캡처한다
runner = CliRunner(mix_stderr=True)


@pytest.fixture(autouse=True)
def patch_db(monkeypatch, tmp_path):
    """각 테스트마다 독립된 임시 DB 경로를 사용하도록 패치한다."""
    db_file = str(tmp_path / "test.db")
    monkeypatch.setattr("cli.main.DB_PATH", db_file)


def test_add_title_only():
    """제목만 입력하면 ID 1로 성공 메시지가 출력된다."""
    result = runner.invoke(app, ["add", "새 할 일"])
    assert result.exit_code == 0
    assert "항목이 추가되었습니다 (ID: 1)" in result.output


def test_add_with_all_options():
    """제목·마감일·우선순위를 모두 입력하면 성공한다."""
    result = runner.invoke(
        app, ["add", "옵션 항목", "--due", "2099-12-31", "--priority", "high"]
    )
    assert result.exit_code == 0
    assert "항목이 추가되었습니다" in result.output


def test_add_blank_title_fails():
    """빈 제목은 exit code 1과 오류 메시지를 반환한다."""
    result = runner.invoke(app, ["add", ""])
    assert result.exit_code == 1
    assert "제목은 필수 입력 항목입니다" in result.output


def test_add_whitespace_title_fails():
    """공백만인 제목은 exit code 1과 오류 메시지를 반환한다."""
    result = runner.invoke(app, ["add", "   "])
    assert result.exit_code == 1
    assert "제목은 필수 입력 항목입니다" in result.output


def test_add_invalid_date_fails():
    """잘못된 날짜 형식은 exit code 1과 오류 메시지를 반환한다."""
    result = runner.invoke(app, ["add", "항목", "--due", "내일"])
    assert result.exit_code == 1
    assert "유효한 날짜 형식이 아닙니다" in result.output


def test_add_invalid_priority_fails():
    """잘못된 우선순위는 exit code 1과 오류 메시지를 반환한다."""
    result = runner.invoke(app, ["add", "항목", "--priority", "urgent"])
    assert result.exit_code == 1
    assert "우선순위는" in result.output


def test_add_past_date_shows_warning():
    """과거 마감일은 경고 메시지와 함께 성공적으로 저장된다."""
    result = runner.invoke(app, ["add", "과거 마감", "--due", "2020-01-01"])
    assert result.exit_code == 0
    assert "마감일이 과거 날짜입니다" in result.output
    assert "항목이 추가되었습니다" in result.output


def test_add_second_item_gets_new_id():
    """두 번째 항목은 첫 번째와 다른 ID를 부여받는다."""
    runner.invoke(app, ["add", "첫 번째"])
    result = runner.invoke(app, ["add", "두 번째"])
    assert result.exit_code == 0
    assert "ID: 2" in result.output
