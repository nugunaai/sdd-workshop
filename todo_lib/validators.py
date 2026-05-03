"""todo_lib/validators.py: 제목/날짜/우선순위/ID/태그 입력 검증 헬퍼."""
import re
from datetime import date, datetime

from todo_lib.errors import ValidationError

VALID_PRIORITIES = {"high", "medium", "low"}

# 태그 허용 문자: 영문자, 숫자, 하이픈, 언더스코어
_TAG_PATTERN = re.compile(r'^[A-Za-z0-9_-]+$')
_MAX_TAG_COUNT = 5
_MAX_TAG_LENGTH = 20


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


def validate_tags(tags: list[str]) -> list[str]:
    """태그 목록을 검증하고 정규화된 목록을 반환한다.

    - 최대 5개 태그만 허용한다.
    - 각 태그는 최대 20자까지 허용한다.
    - 허용 문자: 영문자, 숫자, 하이픈(-), 언더스코어(_).
    - 공백만으로 이루어진 태그는 거부한다.
    - 대소문자 무관 중복은 허용하지 않는다.
    - 원본 대소문자를 유지한다.

    Raises:
        ValidationError: 규칙 위반 시.
    """
    if len(tags) > _MAX_TAG_COUNT:
        raise ValidationError("태그는 최대 5개까지 입력할 수 있습니다")

    normalized: list[str] = []
    seen_lower: set[str] = set()

    for tag in tags:
        stripped = tag.strip()
        if not stripped:
            raise ValidationError("태그는 영문, 숫자, '-', '_'만 사용할 수 있습니다")
        if len(stripped) > _MAX_TAG_LENGTH:
            raise ValidationError("태그는 최대 20자까지 허용됩니다")
        if not _TAG_PATTERN.match(stripped):
            raise ValidationError("태그는 영문, 숫자, '-', '_'만 사용할 수 있습니다")
        lower = stripped.lower()
        if lower in seen_lower:
            raise ValidationError("중복 태그는 허용되지 않습니다")
        seen_lower.add(lower)
        normalized.append(stripped)

    return normalized
