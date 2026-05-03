"""cli/output.py: CLI 출력 포맷팅 및 오류 메시지 헬퍼."""
import typer

from todo_lib.models import ToDoItem


def print_add_success(item: ToDoItem) -> None:
    """항목 추가 성공 메시지를 출력한다."""
    typer.echo(f"항목이 추가되었습니다 (ID: {item.id})")


def print_past_due_warning() -> None:
    """마감일이 과거 날짜임을 경고한다."""
    typer.echo("마감일이 과거 날짜입니다")


def print_list_items(items: list[ToDoItem]) -> None:
    """항목 목록을 출력한다. 항목이 없으면 안내 메시지를 출력한다."""
    if not items:
        typer.echo("등록된 항목이 없습니다")
        return
    for item in items:
        done_label = "완료" if item.is_done else "미완료"
        due_label = item.due_date.strftime("%Y-%m-%d") if item.due_date else "-"
        priority_label = item.priority or "-"
        typer.echo(
            f"[{item.id}] {item.title} | 마감일: {due_label} | "
            f"우선순위: {priority_label} | {done_label}"
        )


def print_done_success(todo_id: int) -> None:
    """완료 처리 성공 메시지를 출력한다."""
    typer.echo(f"항목 {todo_id}가 완료 처리되었습니다")


def print_already_done(todo_id: int) -> None:
    """이미 완료된 항목 안내 메시지를 출력한다."""
    typer.echo(f"항목 {todo_id}는 이미 완료된 항목입니다")


def print_delete_success(todo_id: int) -> None:
    """삭제 성공 메시지를 출력한다."""
    typer.echo(f"항목 {todo_id}가 삭제되었습니다")


def print_error(message: str) -> None:
    """오류 메시지를 출력한다."""
    typer.echo(message)
