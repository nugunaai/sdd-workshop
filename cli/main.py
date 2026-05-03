"""cli/main.py: Typer 기반 CLI entrypoint.
명령 파싱·검증·출력만 담당하며 비즈니스 규칙은 todo_lib.service에 위임한다.
"""
from typing import Optional

import typer
from sqlalchemy.exc import DatabaseError as SADatabaseError
from sqlalchemy.exc import OperationalError

import cli.output as output
import todo_lib.service as service
from todo_lib.db import get_engine, get_session_factory, init_db
from todo_lib.errors import AlreadyDoneError, TodoNotFoundError, ValidationError
from todo_lib.validators import validate_id

# 모듈 수준 DB 경로 — 테스트에서 monkeypatch로 교체한다
DB_PATH = "todo.db"

app = typer.Typer()


def _get_session():
    """DB 세션을 생성한다. 파일 접근/파싱 오류 시 오류 메시지를 출력하고 종료한다."""
    try:
        engine = get_engine(DB_PATH)
        init_db(engine)
        Session = get_session_factory(engine)
        return Session()
    except (OperationalError, SADatabaseError, Exception):
        output.print_error(
            "데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요"
        )
        raise typer.Exit(code=2)


@app.command()
def add(
    title: str = typer.Argument(..., help="할 일 제목"),
    due: Optional[str] = typer.Option(None, "--due", help="마감일 (YYYY-MM-DD)"),
    priority: Optional[str] = typer.Option(
        None, "--priority", help="우선순위 (high|medium|low)"
    ),
    tag: list[str] = typer.Option([], "--tag", help="태그 (반복 사용 가능, 최대 5개)"),
) -> None:
    """새 ToDo 항목을 추가한다."""
    session = _get_session()
    try:
        item, past_warning = service.add_todo(
            session, title=title, due_date_str=due, priority=priority, tags=tag
        )
        if past_warning:
            output.print_past_due_warning()
        output.print_add_success(item)
    except ValidationError as e:
        output.print_error(str(e))
        raise typer.Exit(code=1)
    except (OperationalError, SADatabaseError):
        output.print_error(
            "데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요"
        )
        raise typer.Exit(code=2)
    finally:
        session.close()


@app.command(name="list")
def list_todos(
    filter: Optional[str] = typer.Option(
        None, "--filter", help="필터 (done|pending)"
    ),
    priority: Optional[str] = typer.Option(
        None, "--priority", help="우선순위 (high|medium|low)"
    ),
    tag: Optional[str] = typer.Option(None, "--tag", help="태그로 필터링"),
) -> None:
    """ToDo 항목 목록을 조회한다."""
    session = _get_session()
    try:
        filter_done: bool | None = None
        if filter == "done":
            filter_done = True
        elif filter == "pending":
            filter_done = False
        elif filter is not None:
            output.print_error("필터는 done 또는 pending이어야 합니다")
            raise typer.Exit(code=1)

        items = service.list_todos(
            session, filter_done=filter_done, priority=priority, tag=tag
        )
        output.print_list_items(items)
    except ValidationError as e:
        output.print_error(str(e))
        raise typer.Exit(code=1)
    except (OperationalError, SADatabaseError):
        output.print_error(
            "데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요"
        )
        raise typer.Exit(code=2)
    finally:
        session.close()


@app.command()
def done(
    id: str = typer.Argument(..., help="완료 처리할 항목 ID"),
) -> None:
    """항목을 완료 처리한다."""
    try:
        todo_id = validate_id(id)
    except ValidationError as e:
        output.print_error(str(e))
        raise typer.Exit(code=1)

    session = _get_session()
    try:
        service.mark_done(session, todo_id)
        output.print_done_success(todo_id)
    except TodoNotFoundError:
        output.print_error(f"항목 {todo_id}를 찾을 수 없습니다")
        raise typer.Exit(code=1)
    except AlreadyDoneError:
        output.print_already_done(todo_id)
        raise typer.Exit(code=1)
    except (OperationalError, SADatabaseError):
        output.print_error(
            "데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요"
        )
        raise typer.Exit(code=2)
    finally:
        session.close()


@app.command()
def delete(
    id: str = typer.Argument(..., help="삭제할 항목 ID"),
) -> None:
    """항목을 영구 삭제한다."""
    try:
        todo_id = validate_id(id)
    except ValidationError as e:
        output.print_error(str(e))
        raise typer.Exit(code=1)

    session = _get_session()
    try:
        service.delete_item(session, todo_id)
        output.print_delete_success(todo_id)
    except TodoNotFoundError:
        output.print_error(f"항목 {todo_id}를 찾을 수 없습니다")
        raise typer.Exit(code=1)
    except (OperationalError, SADatabaseError):
        output.print_error(
            "데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요"
        )
        raise typer.Exit(code=2)
    finally:
        session.close()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
