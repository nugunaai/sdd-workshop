# CLI Contract

## Command Surface

### 1) Add
- Command:
  - `todo add "<title>" [--due YYYY-MM-DD] [--priority high|medium|low]`
- Input rules:
  - `title` required, blank/whitespace 금지
  - `--due` 형식은 `YYYY-MM-DD`
  - `--priority` 값은 `high|medium|low`
- Success output:
  - `항목이 추가되었습니다 (ID: <id>)`
- Error output examples:
  - `제목은 필수 입력 항목입니다`
  - `유효한 날짜 형식이 아닙니다: YYYY-MM-DD`
  - `우선순위는 high|medium|low 중 하나여야 합니다`

### 2) List
- Command:
  - `todo list [--filter done|pending] [--priority high|medium|low]`
- Output fields (per item):
  - `ID`, `제목`, `마감일`, `우선순위`, `완료 여부`
- Empty output:
  - `등록된 항목이 없습니다`

### 3) Done
- Command:
  - `todo done <id>`
- Success output:
  - `항목 <id>가 완료 처리되었습니다`
- Non-success output:
  - `항목 <id>는 이미 완료된 항목입니다`
  - `항목 <id>를 찾을 수 없습니다`
  - `ID는 숫자여야 합니다`

### 4) Delete
- Command:
  - `todo delete <id>`
- Success output:
  - `항목 <id>가 삭제되었습니다`
- Error output:
  - `항목 <id>를 찾을 수 없습니다`
  - `ID는 숫자여야 합니다`

## Exit Code Contract
- `0`: 정상 수행
- `1`: 사용자 입력 오류(검증 실패, 존재하지 않는 ID 등)
- `2`: 시스템 오류(DB 파일 손상/접근 불가)

## System Error Contract
- SQLite 파일 손상/접근 실패 시:
  - `데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요`
  - Exit code `2`
