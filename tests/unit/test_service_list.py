"""tests/unit/test_service_list.py: list_todos 서비스 단위 테스트 (T020)."""
import pytest

from todo_lib.errors import ValidationError


def test_list_empty(db_session):
    """항목이 없으면 빈 리스트를 반환한다."""
    from todo_lib.service import list_todos

    assert list_todos(db_session) == []


def test_list_all(db_session):
    """모든 항목을 반환한다."""
    from todo_lib.service import add_todo, list_todos

    add_todo(db_session, title="항목1")
    add_todo(db_session, title="항목2")
    assert len(list_todos(db_session)) == 2


def test_list_filter_pending(db_session):
    """미완료 필터는 완료된 항목을 제외한다."""
    from todo_lib.service import add_todo, list_todos, mark_done

    item1, _ = add_todo(db_session, title="미완료")
    item2, _ = add_todo(db_session, title="완료됨")
    mark_done(db_session, item2.id)

    items = list_todos(db_session, filter_done=False)
    assert len(items) == 1
    assert items[0].title == "미완료"


def test_list_filter_done(db_session):
    """완료 필터는 완료된 항목만 반환한다."""
    from todo_lib.service import add_todo, list_todos, mark_done

    item1, _ = add_todo(db_session, title="미완료")
    item2, _ = add_todo(db_session, title="완료됨")
    mark_done(db_session, item2.id)

    items = list_todos(db_session, filter_done=True)
    assert len(items) == 1
    assert items[0].title == "완료됨"


def test_list_filter_priority(db_session):
    """우선순위 필터는 해당 우선순위 항목만 반환한다."""
    from todo_lib.service import add_todo, list_todos

    add_todo(db_session, title="높음", priority="high")
    add_todo(db_session, title="낮음", priority="low")

    items = list_todos(db_session, priority="high")
    assert len(items) == 1
    assert items[0].title == "높음"


def test_list_invalid_priority_raises(db_session):
    """잘못된 우선순위 값은 ValidationError를 발생시킨다."""
    from todo_lib.service import list_todos

    with pytest.raises(ValidationError):
        list_todos(db_session, priority="urgent")


def test_list_sorted_by_id(db_session):
    """목록은 항상 id 오름차순으로 정렬된다."""
    from todo_lib.service import add_todo, list_todos

    add_todo(db_session, title="A")
    add_todo(db_session, title="B")
    add_todo(db_session, title="C")

    items = list_todos(db_session)
    assert [i.title for i in items] == ["A", "B", "C"]
