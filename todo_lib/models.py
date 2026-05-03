"""todo_lib/models.py: ToDoItem SQLAlchemy ORM 모델."""
from datetime import date, datetime

from sqlalchemy import JSON, Boolean, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from todo_lib.db import Base


class ToDoItem(Base):
    """ToDo 항목 엔티티. id는 자동 부여되며 삭제는 물리적 행 삭제다."""
    __tablename__ = "todo_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    priority: Mapped[str | None] = mapped_column(String, nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # 태그 목록. 최대 5개, 각 20자 이하, [A-Za-z0-9_-] 문자만 허용
    tags: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
