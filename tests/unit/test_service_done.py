"""tests/unit/test_service_done.py: mark_done 서비스 단위 테스트 (T025)."""
import pytest

from todo_lib.errors import AlreadyDoneError, TodoNotFoundError


def test_mark_done_success(db_session):
    """미완료 항목을 완료 처리하면 is_done=True, completed_at이 설정된다."""
    from todo_lib.service import add_todo, mark_done

    item, _ = add_todo(db_session, title="할 일")
    done_item = mark_done(db_session, item.id)
    assert done_item.is_done is True
    assert done_item.completed_at is not None


def test_mark_done_not_found(db_session):
    """존재하지 않는 ID는 TodoNotFoundError를 발생시킨다."""
    from todo_lib.service import mark_done

    with pytest.raises(TodoNotFoundError):
        mark_done(db_session, 999)


def test_mark_done_already_done(db_session):
    """이미 완료된 항목에 완료 처리 시 AlreadyDoneError를 발생시킨다."""
    from todo_lib.service import add_todo, mark_done

    item, _ = add_todo(db_session, title="이미 완료")
    mark_done(db_session, item.id)
    with pytest.raises(AlreadyDoneError):
        mark_done(db_session, item.id)


def test_mark_done_does_not_change_other_items(db_session):
    """완료 처리는 대상 항목에만 영향을 준다."""
    from todo_lib.service import add_todo, list_todos, mark_done

    item1, _ = add_todo(db_session, title="완료 대상")
    item2, _ = add_todo(db_session, title="유지 항목")
    mark_done(db_session, item1.id)

    remaining = list_todos(db_session, filter_done=False)
    assert len(remaining) == 1
    assert remaining[0].title == "유지 항목"
