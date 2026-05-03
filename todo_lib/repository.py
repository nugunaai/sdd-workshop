"""todo_lib/repository.py: DB CRUD 기본 연산."""
from datetime import date, datetime

from sqlalchemy.orm import Session

from todo_lib.models import ToDoItem


def create_todo(
    session: Session,
    title: str,
    due_date: date | None = None,
    priority: str | None = None,
) -> ToDoItem:
    """새 ToDoItem을 저장하고 반환한다."""
    item = ToDoItem(
        title=title,
        due_date=due_date,
        priority=priority,
        is_done=False,
        created_at=datetime.now(),
        completed_at=None,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def get_todo(session: Session, todo_id: int) -> ToDoItem | None:
    """ID로 항목을 조회한다. 없으면 None을 반환한다."""
    return session.get(ToDoItem, todo_id)


def get_all_todos(
    session: Session,
    is_done: bool | None = None,
    priority: str | None = None,
) -> list[ToDoItem]:
    """조건에 맞는 항목 목록을 id 오름차순으로 반환한다."""
    query = session.query(ToDoItem)
    if is_done is not None:
        query = query.filter(ToDoItem.is_done == is_done)
    if priority is not None:
        query = query.filter(ToDoItem.priority == priority)
    return query.order_by(ToDoItem.id).all()


def mark_todo_done(session: Session, item: ToDoItem) -> ToDoItem:
    """항목을 완료 상태로 변경하고 완료 일시를 기록한다."""
    item.is_done = True
    item.completed_at = datetime.now()
    session.commit()
    session.refresh(item)
    return item


def delete_todo(session: Session, item: ToDoItem) -> None:
    """항목을 물리적으로 삭제한다. 복구 불가."""
    session.delete(item)
    session.commit()
