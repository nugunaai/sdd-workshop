"""tests/integration/test_cli_validation_matrix.py: SC-003 입력 오류 매트릭스 테스트 (T044).
잘못된 입력 100%에서 오류 메시지가 출력되고 데이터가 손상되지 않음을 검증한다.
"""
import pytest
from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def patch_db(monkeypatch, tmp_path):
    """각 테스트마다 독립된 임시 DB 경로를 사용하도록 패치한다."""
    monkeypatch.setattr("cli.main.DB_PATH", str(tmp_path / "test.db"))


# --- add 입력 오류 매트릭스 ---

def test_add_empty_title():
    result = runner.invoke(app, ["add", ""])
    assert result.exit_code == 1
    assert "제목은 필수 입력 항목입니다" in result.output


def test_add_whitespace_title():
    result = runner.invoke(app, ["add", "   "])
    assert result.exit_code == 1
    assert "제목은 필수 입력 항목입니다" in result.output


def test_add_invalid_date_format():
    result = runner.invoke(app, ["add", "항목", "--due", "20260101"])
    assert result.exit_code == 1
    assert "유효한 날짜 형식이 아닙니다" in result.output


def test_add_nonsense_date():
    result = runner.invoke(app, ["add", "항목", "--due", "내일"])
    assert result.exit_code == 1
    assert "유효한 날짜 형식이 아닙니다" in result.output


def test_add_invalid_priority():
    result = runner.invoke(app, ["add", "항목", "--priority", "urgent"])
    assert result.exit_code == 1
    assert "우선순위는" in result.output


# --- done 입력 오류 매트릭스 ---

def test_done_nonexistent_id():
    result = runner.invoke(app, ["done", "999"])
    assert result.exit_code == 1
    assert "찾을 수 없습니다" in result.output


def test_done_nonnumeric_id():
    result = runner.invoke(app, ["done", "abc"])
    assert result.exit_code == 1
    assert "ID는 숫자여야 합니다" in result.output


# --- delete 입력 오류 매트릭스 ---

def test_delete_nonexistent_id():
    result = runner.invoke(app, ["delete", "999"])
    assert result.exit_code == 1
    assert "찾을 수 없습니다" in result.output


def test_delete_nonnumeric_id():
    result = runner.invoke(app, ["delete", "abc"])
    assert result.exit_code == 1
    assert "ID는 숫자여야 합니다" in result.output


# --- 데이터 비손상 검증 ---

def test_no_data_corruption_on_multiple_invalid_inputs():
    """잘못된 입력을 여러 번 시도해도 기존 데이터가 손상되지 않는다."""
    # 유효한 항목 추가
    result = runner.invoke(app, ["add", "기존 항목"])
    assert result.exit_code == 0

    # 다양한 잘못된 입력 시도
    runner.invoke(app, ["add", ""])
    runner.invoke(app, ["add", "항목", "--due", "잘못된날짜"])
    runner.invoke(app, ["add", "항목", "--priority", "invalid"])
    runner.invoke(app, ["done", "abc"])
    runner.invoke(app, ["delete", "xyz"])
    runner.invoke(app, ["done", "999"])
    runner.invoke(app, ["delete", "999"])

    # 기존 데이터 유지 확인
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "기존 항목" in result.output
