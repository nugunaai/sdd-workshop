# CLI Contract: ToDo 태그 기능

## Command Surface

### 1) Add
- Command:
  - `todo add "<title>" [--due YYYY-MM-DD] [--priority high|medium|low] [--tag <tag>]...`
- Input rules:
  - `title` required, blank/whitespace 금지
  - `--tag`는 0~5회 입력 가능
  - 각 태그는 1~20자, 허용 문자 `[A-Za-z0-9_-]`
  - 중복 태그(case-insensitive) 금지
- Success output:
  - `항목이 추가되었습니다 (ID: <id>)`
- Error output examples:
  - `태그는 최대 5개까지 입력할 수 있습니다`
  - `태그는 영문, 숫자, '-', '_'만 사용할 수 있습니다`
  - `태그는 최대 20자까지 허용됩니다`
  - `중복 태그는 허용되지 않습니다`

### 2) List
- Command:
  - `todo list [--filter done|pending] [--priority high|medium|low] [--tag <tag>]`
- Filter semantics:
  - `--tag`가 지정되면 해당 태그(대소문자 비구분)를 가진 항목만 반환
  - `--filter`, `--priority`, `--tag`는 동시에 조합 가능
- Output fields (per item):
  - `ID`, `제목`, `마감일`, `우선순위`, `태그`, `완료 여부`
- Empty output:
  - `등록된 항목이 없습니다`

### 3) Done
- Command:
  - `todo done <id>`
- Contract unchanged:
  - 기존 성공/오류 메시지와 exit code 유지

### 4) Delete
- Command:
  - `todo delete <id>`
- Contract unchanged:
  - 기존 성공/오류 메시지와 exit code 유지

## Exit Code Contract
- `0`: 정상 수행
- `1`: 사용자 입력 오류(검증 실패, 존재하지 않는 ID 등)
- `2`: 시스템 오류(DB 파일 손상/접근 불가)

## Backward Compatibility
- 태그를 입력하지 않는 기존 명령 사용 패턴은 그대로 동작해야 한다.
- 기존 `add/list/done/delete` 테스트의 기대 출력과 동작을 변경하지 않는다(태그 출력 필드 추가는 목록 형식 확장으로 취급).
