"""tests/integration/test_cli_list.py: todo list CLI 통합 테스트 (T021)."""
import pytest
from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def patch_db(monkeypatch, tmp_path):
    """각 테스트마다 독립된 임시 DB 경로를 사용하도록 패치한다."""
    monkeypatch.setattr("cli.main.DB_PATH", str(tmp_path / "test.db"))


def test_list_empty():
    """항목이 없으면 '등록된 항목이 없습니다'를 출력한다."""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "등록된 항목이 없습니다" in result.output


def test_list_shows_all_items():
    """항목이 있으면 모든 항목이 출력된다."""
    runner.invoke(app, ["add", "항목 A"])
    runner.invoke(app, ["add", "항목 B"])
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "항목 A" in result.output
    assert "항목 B" in result.output


def test_list_shows_fields():
    """각 항목은 ID·제목·마감일·우선순위·완료 여부를 포함한다."""
    runner.invoke(app, ["add", "필드 테스트", "--due", "2099-01-01", "--priority", "high"])
    result = runner.invoke(app, ["list"])
    assert "필드 테스트" in result.output
    assert "2099-01-01" in result.output
    assert "high" in result.output
    assert "미완료" in result.output


def test_list_filter_pending():
    """--filter pending은 미완료 항목만 출력한다."""
    runner.invoke(app, ["add", "미완료 항목"])
    r = runner.invoke(app, ["add", "완료될 항목"])
    # ID 파싱 후 done 처리
    import re
    m = re.search(r"ID: (\d+)", r.output)
    assert m
    runner.invoke(app, ["done", m.group(1)])

    result = runner.invoke(app, ["list", "--filter", "pending"])
    assert result.exit_code == 0
    assert "미완료 항목" in result.output
    assert "완료될 항목" not in result.output


def test_list_filter_done():
    """--filter done은 완료된 항목만 출력한다."""
    runner.invoke(app, ["add", "미완료 항목"])
    r = runner.invoke(app, ["add", "완료될 항목"])
    import re
    m = re.search(r"ID: (\d+)", r.output)
    assert m
    runner.invoke(app, ["done", m.group(1)])

    result = runner.invoke(app, ["list", "--filter", "done"])
    assert result.exit_code == 0
    assert "완료될 항목" in result.output
    assert "미완료 항목" not in result.output


def test_list_filter_priority():
    """--priority 필터는 해당 우선순위 항목만 출력한다."""
    runner.invoke(app, ["add", "높음 항목", "--priority", "high"])
    runner.invoke(app, ["add", "낮음 항목", "--priority", "low"])

    result = runner.invoke(app, ["list", "--priority", "high"])
    assert result.exit_code == 0
    assert "높음 항목" in result.output
    assert "낮음 항목" not in result.output


def test_list_invalid_filter_fails():
    """잘못된 --filter 값은 exit code 1과 오류 메시지를 반환한다."""
    result = runner.invoke(app, ["list", "--filter", "invalid"])
    assert result.exit_code == 1


# --- T014: --tag 필터 통합 테스트 ---

def test_list_tag_filter_returns_matching_items():
    """--tag 필터는 해당 태그를 포함한 항목만 반환한다."""
    runner.invoke(app, ["add", "work 항목", "--tag", "work"])
    runner.invoke(app, ["add", "home 항목", "--tag", "home"])

    result = runner.invoke(app, ["list", "--tag", "work"])
    assert result.exit_code == 0
    assert "work 항목" in result.output
    assert "home 항목" not in result.output


def test_list_tag_filter_no_match_shows_empty_message():
    """--tag 필터에 매칭 항목이 없으면 빈 목록 메시지를 출력한다."""
    runner.invoke(app, ["add", "other 항목", "--tag", "other"])

    result = runner.invoke(app, ["list", "--tag", "nonexistent"])
    assert result.exit_code == 0
    assert "등록된 항목이 없습니다" in result.output


def test_list_tag_filter_combined_with_priority():
    """--tag와 --priority 복합 필터는 두 조건 모두 만족하는 항목만 반환한다."""
    runner.invoke(app, ["add", "work+high", "--tag", "work", "--priority", "high"])
    runner.invoke(app, ["add", "work+low", "--tag", "work", "--priority", "low"])
    runner.invoke(app, ["add", "home+high", "--tag", "home", "--priority", "high"])

    result = runner.invoke(app, ["list", "--tag", "work", "--priority", "high"])
    assert result.exit_code == 0
    assert "work+high" in result.output
    assert "work+low" not in result.output
    assert "home+high" not in result.output


def test_list_without_tag_filter_shows_all():
    """--tag 없이 호출하면 태그 유무와 관계없이 모든 항목을 반환한다."""
    runner.invoke(app, ["add", "태그 있음", "--tag", "work"])
    runner.invoke(app, ["add", "태그 없음"])

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "태그 있음" in result.output
    assert "태그 없음" in result.output


# --- T031: case-insensitive 비교, original case 출력 테스트 ---

def test_list_tag_filter_is_case_insensitive():
    """태그 필터는 대소문자 무관하게 매칭한다."""
    runner.invoke(app, ["add", "Work 항목", "--tag", "Work"])

    result_lower = runner.invoke(app, ["list", "--tag", "work"])
    assert result_lower.exit_code == 0
    assert "Work 항목" in result_lower.output

    result_upper = runner.invoke(app, ["list", "--tag", "WORK"])
    assert result_upper.exit_code == 0
    assert "Work 항목" in result_upper.output


def test_list_tag_output_preserves_original_case():
    """목록 출력에서 태그는 최초 입력 시의 원본 대소문자를 유지한다."""
    runner.invoke(app, ["add", "케이스 항목", "--tag", "MyTag"])

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    # 원본 대소문자(MyTag)가 출력에 포함되어야 한다
    assert "MyTag" in result.output
