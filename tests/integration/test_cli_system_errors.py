"""tests/integration/test_cli_system_errors.py: DB 손상 오류 처리 통합 테스트 (T035)."""
import pytest
from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


def test_corrupted_db_list(monkeypatch, tmp_path):
    """손상된 DB 파일로 list 명령 실행 시 exit code 2와 오류 메시지를 반환한다."""
    db_file = tmp_path / "corrupted.db"
    # 유효하지 않은 내용으로 파일을 생성해 SQLite 파싱 오류를 유발한다
    db_file.write_text("이것은 유효하지 않은 SQLite 파일입니다")
    monkeypatch.setattr("cli.main.DB_PATH", str(db_file))

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 2
    assert "데이터 파일이 손상되었습니다" in result.output


def test_corrupted_db_add(monkeypatch, tmp_path):
    """손상된 DB 파일로 add 명령 실행 시 exit code 2와 오류 메시지를 반환한다."""
    db_file = tmp_path / "corrupted.db"
    db_file.write_bytes(b"\x00\x01\x02\x03\xff\xfe" * 100)
    monkeypatch.setattr("cli.main.DB_PATH", str(db_file))

    result = runner.invoke(app, ["add", "테스트"])
    assert result.exit_code == 2
    assert "데이터 파일이 손상되었습니다" in result.output


def test_corrupted_db_error_message_content(monkeypatch, tmp_path):
    """오류 메시지에 백업/삭제 안내가 포함된다."""
    db_file = tmp_path / "corrupted.db"
    db_file.write_text("not a sqlite file")
    monkeypatch.setattr("cli.main.DB_PATH", str(db_file))

    result = runner.invoke(app, ["list"])
    assert "백업하거나 삭제 후 재시도하세요" in result.output
