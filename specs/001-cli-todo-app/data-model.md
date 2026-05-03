# Data Model: CLI 기반 ToDo 관리 앱

## Entity: ToDoItem

### Fields
- `id` (INTEGER, PK, auto-increment)
- `title` (TEXT, NOT NULL)
- `due_date` (DATE, NULL)
- `priority` (TEXT, NULL, allowed: `high`, `medium`, `low`)
- `is_done` (BOOLEAN, NOT NULL, default: `false`)
- `created_at` (DATETIME, NOT NULL)
- `completed_at` (DATETIME, NULL)

### Validation Rules
- `title`:
  - 빈 문자열/공백-only 금지 (FR-011)
- `due_date`:
  - 입력 형식은 `YYYY-MM-DD`만 허용 (FR-012)
  - 과거 날짜면 경고 출력 후 저장 허용 (FR-014)
- `priority`:
  - `high|medium|low` 외 값 거부 (FR-013)
- `id`:
  - 정수만 허용, 존재하지 않으면 명확한 오류 (FR-010)

### State Transitions
- Initial state:
  - `is_done=false`, `completed_at=NULL`
- Done transition (`todo done <id>`):
  - `is_done=false` -> `is_done=true`
  - `completed_at=now()`
- Repeated done:
  - 이미 완료 항목은 상태 변경 없이 안내 메시지
- Delete transition (`todo delete <id>`):
  - row physical delete (복구 불가)

## Derived Query Views
- All items: 정렬 기준 `id ASC`
- Filter `pending`: `is_done=false`
- Filter `done`: `is_done=true`
- Priority filter: `priority = :priority`
- Combined filters: `WHERE` 조건 조합

## Persistence Notes
- DB file: `todo.db` (SQLite)
- ORM: SQLAlchemy declarative model
- Session scope: CLI command 단위 session 생성/종료
- 오류 처리: DB open/read 실패 시 사용자 메시지 출력 후 종료 (FR-015)
