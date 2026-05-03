"""tests/unit/test_service_delete.py: delete_item 서비스 단위 테스트 (T030)."""
import pytest

from todo_lib.errors import TodoNotFoundError


def test_delete_success(db_session):
    """항목을 삭제하면 목록에서 사라진다."""
    from todo_lib.service import add_todo, delete_item, list_todos

    item, _ = add_todo(db_session, title="삭제할 항목")
    delete_item(db_session, item.id)
    assert list_todos(db_session) == []


def test_delete_not_found(db_session):
    """존재하지 않는 ID는 TodoNotFoundError를 발생시킨다."""
    from todo_lib.service import delete_item

    with pytest.raises(TodoNotFoundError):
        delete_item(db_session, 999)


def test_delete_removes_only_target(db_session):
    """삭제는 대상 항목만 제거하고 나머지는 유지한다."""
    from todo_lib.service import add_todo, delete_item, list_todos

    item1, _ = add_todo(db_session, title="유지 항목")
    item2, _ = add_todo(db_session, title="삭제 항목")
    delete_item(db_session, item2.id)

    remaining = list_todos(db_session)
    assert len(remaining) == 1
    assert remaining[0].title == "유지 항목"


def test_delete_is_permanent(db_session):
    """삭제된 항목은 ID로 다시 조회되지 않는다."""
    from todo_lib.repository import get_todo
    from todo_lib.service import add_todo, delete_item

    item, _ = add_todo(db_session, title="영구 삭제 항목")
    item_id = item.id
    delete_item(db_session, item_id)
    assert get_todo(db_session, item_id) is None
