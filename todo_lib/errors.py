"""todo_lib/errors.py: 서비스 레이어 예외 클래스."""


class ValidationError(Exception):
    """사용자 입력 검증 실패 시 발생하는 예외."""
    pass


class TodoNotFoundError(Exception):
    """존재하지 않는 항목 ID 접근 시 발생하는 예외."""

    def __init__(self, todo_id: int) -> None:
        self.todo_id = todo_id
        super().__init__(f"항목 {todo_id}를 찾을 수 없습니다")


class AlreadyDoneError(Exception):
    """이미 완료된 항목에 완료 처리 시도 시 발생하는 예외."""

    def __init__(self, todo_id: int) -> None:
        self.todo_id = todo_id
        super().__init__(f"항목 {todo_id}는 이미 완료된 항목입니다")


class DatabaseError(Exception):
    """DB 파일 접근/파싱 실패 시 발생하는 예외."""
    pass
