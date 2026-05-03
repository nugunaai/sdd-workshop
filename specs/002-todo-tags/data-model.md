# Data Model: ToDo 태그 기능 추가

## Entity: ToDoItem

### Fields
- `id` (INTEGER, PK, auto-increment)
- `title` (TEXT, NOT NULL)
- `due_date` (DATE, NULL)
- `priority` (TEXT, NULL, allowed: `high`, `medium`, `low`)
- `tags` (JSON, NOT NULL, default: `[]`)
- `is_done` (BOOLEAN, NOT NULL, default: `false`)
- `created_at` (DATETIME, NOT NULL)
- `completed_at` (DATETIME, NULL)

### Tag Semantics
- 저장 형태: 문자열 리스트 (예: `["work", "Urgent"]`)
- 입력 문법: `--tag` 옵션 반복 (`todo add "제목" --tag work --tag urgent`)
- 최대 개수: 5
- 개별 길이: 20자 이하
- 허용 문자: 영문/숫자/하이픈/언더스코어 (`[A-Za-z0-9_-]`)
- 공백: 허용하지 않음
- 중복 판단: 공백 trim + case-insensitive 기준으로 동일하면 중복
- 표시 규칙: 저장/출력은 최초 입력 원형 유지

### Validation Rules
- `title`:
  - 빈 문자열/공백-only 금지
- `priority`:
  - `high|medium|low` 외 값 거부
- `tags`:
  - 개수 > 5 거부
  - 길이 > 20 거부
  - 허용 문자 외 입력 거부
  - 동일 항목 내 중복 태그 거부 (case-insensitive)
- `id`:
  - 정수만 허용, 존재하지 않으면 오류

### State Transitions
- Initial state:
  - `is_done=false`, `completed_at=NULL`
  - `tags=[]` (태그 미입력 시)
- Done transition (`todo done <id>`):
  - `is_done=false` -> `is_done=true`
  - `completed_at=now()`
- Delete transition (`todo delete <id>`):
  - row physical delete (복구 불가)

## Derived Query Views
- All items: `id ASC`
- Pending/done filter: `is_done` 조건
- Priority filter: `priority` 조건
- Tag filter: 요청 태그를 정규화한 값이 항목 태그 정규화 집합에 포함되는 항목만 반환
- Combined filters: `is_done + priority + tag` 조건 동시 적용

## Persistence Notes
- DB file: `todo.db` (SQLite)
- ORM: SQLAlchemy declarative model
- JSON column: SQLAlchemy `JSON` 타입 사용
- Session scope: command 단위 session 생성/종료
- Migration strategy: 기존 DB에는 `tags` 컬럼 추가가 필요하며 기존 항목은 `[]`로 취급
