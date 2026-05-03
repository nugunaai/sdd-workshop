"""tests/unit/test_service_add.py: add_todo 서비스 단위 테스트 (T014).
NOTE: 구현 전 Red 상태로 먼저 작성한다.
"""
import pytest
from datetime import date, timedelta

from todo_lib.errors import ValidationError


def test_add_title_only(db_session):
    """제목만 입력해 추가하면 ID 1이 부여되고 선택 필드는 None이다."""
    from todo_lib.service import add_todo

    item, past_warning = add_todo(db_session, title="테스트 항목")
    assert item.id == 1
    assert item.title == "테스트 항목"
    assert item.due_date is None
    assert item.priority is None
    assert item.is_done is False
    assert past_warning is False


def test_add_with_all_fields(db_session):
    """제목·마감일·우선순위를 모두 입력하면 모두 저장된다."""
    from todo_lib.service import add_todo

    future = date.today() + timedelta(days=7)
    item, past_warning = add_todo(
        db_session,
        title="전체 필드",
        due_date_str=future.strftime("%Y-%m-%d"),
        priority="high",
    )
    assert item.title == "전체 필드"
    assert item.due_date == future
    assert item.priority == "high"
    assert past_warning is False


def test_add_increments_id(db_session):
    """두 번 추가하면 두 번째 항목의 ID가 첫 번째보다 크다."""
    from todo_lib.service import add_todo

    item1, _ = add_todo(db_session, title="첫 번째")
    item2, _ = add_todo(db_session, title="두 번째")
    assert item2.id > item1.id


def test_add_blank_title_raises(db_session):
    """빈 문자열 제목은 ValidationError를 발생시킨다."""
    from todo_lib.service import add_todo

    with pytest.raises(ValidationError):
        add_todo(db_session, title="")


def test_add_whitespace_title_raises(db_session):
    """공백만으로 구성된 제목은 ValidationError를 발생시킨다."""
    from todo_lib.service import add_todo

    with pytest.raises(ValidationError):
        add_todo(db_session, title="   ")


def test_add_invalid_date_raises(db_session):
    """날짜 형식이 아닌 문자열은 ValidationError를 발생시킨다."""
    from todo_lib.service import add_todo

    with pytest.raises(ValidationError):
        add_todo(db_session, title="항목", due_date_str="내일")


def test_add_invalid_date_format_raises(db_session):
    """YYYYMMDD 형식(구분자 없음)은 ValidationError를 발생시킨다."""
    from todo_lib.service import add_todo

    with pytest.raises(ValidationError):
        add_todo(db_session, title="항목", due_date_str="20260532")


def test_add_invalid_priority_raises(db_session):
    """허용 범위 밖의 우선순위 값은 ValidationError를 발생시킨다."""
    from todo_lib.service import add_todo

    with pytest.raises(ValidationError):
        add_todo(db_session, title="항목", priority="urgent")


def test_add_past_date_returns_warning(db_session):
    """과거 마감일은 ValidationError 없이 저장되고 past_warning이 True다."""
    from todo_lib.service import add_todo

    past = date.today() - timedelta(days=1)
    item, past_warning = add_todo(
        db_session, title="과거 마감", due_date_str=past.strftime("%Y-%m-%d")
    )
    assert past_warning is True
    assert item.id is not None


def test_add_strips_title_whitespace(db_session):
    """앞뒤 공백이 있는 제목은 trim 처리 후 저장된다."""
    from todo_lib.service import add_todo

    item, _ = add_todo(db_session, title="  앞뒤 공백  ")
    assert item.title == "앞뒤 공백"
