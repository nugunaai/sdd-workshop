"""todo_lib/service.py: 도메인 서비스 레이어 (비즈니스 규칙 처리)."""
from datetime import date

from sqlalchemy.orm import Session

from todo_lib.errors import AlreadyDoneError, TodoNotFoundError, ValidationError
from todo_lib.models import ToDoItem
from todo_lib.repository import (
    create_todo,
    delete_todo as repo_delete,
    get_all_todos,
    get_todo,
    mark_todo_done,
)
from todo_lib.validators import (
    is_past_date,
    validate_due_date,
    validate_id,
    validate_priority,
    validate_tags,
    validate_title,
)


def add_todo(
    session: Session,
    title: str,
    due_date_str: str | None = None,
    priority: str | None = None,
    tags: list[str] | None = None,
) -> tuple[ToDoItem, bool]:
    """새 ToDo 항목을 추가한다.

    Returns:
        (item, past_warning): past_warning은 마감일이 과거일 때 True다.
    Raises:
        ValidationError: 제목이 비어 있거나 날짜/우선순위/태그 형식이 잘못된 경우.
    """
    title = validate_title(title)
    due_date = validate_due_date(due_date_str)
    priority = validate_priority(priority)
    validated_tags = validate_tags(tags if tags is not None else [])

    past_warning = False
    if due_date is not None:
        past_warning = is_past_date(due_date)

    item = create_todo(
        session, title=title, due_date=due_date, priority=priority, tags=validated_tags
    )
    return item, past_warning


def list_todos(
    session: Session,
    filter_done: bool | None = None,
    priority: str | None = None,
    tag: str | None = None,
) -> list[ToDoItem]:
    """조건에 맞는 항목 목록을 반환한다.

    Raises:
        ValidationError: 우선순위 값이 유효하지 않은 경우.
    """
    if priority is not None:
        priority = validate_priority(priority)
    return get_all_todos(session, is_done=filter_done, priority=priority, tag=tag)


def mark_done(session: Session, todo_id: int) -> ToDoItem:
    """항목을 완료 상태로 변경한다.

    Raises:
        TodoNotFoundError: ID에 해당하는 항목이 없는 경우.
        AlreadyDoneError: 이미 완료된 항목인 경우.
    """
    item = get_todo(session, todo_id)
    if item is None:
        raise TodoNotFoundError(todo_id)
    if item.is_done:
        raise AlreadyDoneError(todo_id)
    return mark_todo_done(session, item)


def delete_item(session: Session, todo_id: int) -> None:
    """항목을 영구 삭제한다.

    Raises:
        TodoNotFoundError: ID에 해당하는 항목이 없는 경우.
    """
    item = get_todo(session, todo_id)
    if item is None:
        raise TodoNotFoundError(todo_id)
    repo_delete(session, item)
