"""todo_lib/validators.py: 제목/날짜/우선순위/ID 입력 검증 헬퍼."""
from datetime import date, datetime

from todo_lib.errors import ValidationError

VALID_PRIORITIES = {"high", "medium", "low"}


def validate_title(title: str) -> str:
    """제목이 비어 있거나 공백만이면 ValidationError를 발생시킨다."""
    if not title or not title.strip():
        raise ValidationError("제목은 필수 입력 항목입니다")
    return title.strip()


def validate_due_date(due_date_str: str | None) -> date | None:
    """YYYY-MM-DD 형식만 허용한다. 그 외 형식이면 ValidationError를 발생시킨다."""
    if due_date_str is None:
        return None
    try:
        return datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("유효한 날짜 형식이 아닙니다: YYYY-MM-DD")


def validate_priority(priority: str | None) -> str | None:
    """high|medium|low 이외의 값이면 ValidationError를 발생시킨다."""
    if priority is None:
        return None
    if priority not in VALID_PRIORITIES:
        raise ValidationError("우선순위는 high|medium|low 중 하나여야 합니다")
    return priority


def validate_id(value: str | int) -> int:
    """정수로 변환 불가능한 값이면 ValidationError를 발생시킨다."""
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValidationError("ID는 숫자여야 합니다")


def is_past_date(due_date: date) -> bool:
    """마감일이 오늘 이전이면 True를 반환한다."""
    return due_date < date.today()
