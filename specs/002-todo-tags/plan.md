# Implementation Plan: ToDo 태그 기능 추가

**Branch**: `002-todo-tags` | **Date**: 2026-05-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-tags/spec.md`

## Summary

기존 CLI ToDo 앱에 태그 기능을 통합한다. 핵심 변경은 `todo_lib.models.ToDoItem`에 JSON 기반 `tags` 필드를 추가하고,
`todo_lib.service.list_todos`에 태그 필터를 확장하며, CLI 조회 명령에 `--tag` 옵션을 추가하는 것이다.
구현은 기존 `todo_lib/` + `cli/` 구조를 유지하고, 기존 add/list/done/delete 동작 및 테스트가 깨지지 않도록 회귀 테스트를 우선한다.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: Typer, SQLAlchemy (runtime), pytest, pytest-cov (test)  
**Storage**: SQLite (`todo.db`) + SQLAlchemy ORM, `tags`는 JSON 컬럼으로 저장  
**Testing**: pytest (unit + integration), pytest-cov  
**Target Platform**: Windows PowerShell/CMD, macOS, Linux  
**Project Type**: CLI application (single project)  
**Performance Goals**: 1,000개 항목에서 add/list/done/delete/tag-filter가 체감상 즉시(일반 개발자 환경에서 1초 이내)  
**Constraints**: 기존 코드(`todo_lib/`, `cli/main.py`)와 직접 통합, 신규 외부 패키지 추가 금지, 기존 테스트 무결성 유지  
**Scale/Scope**: 단일 사용자 로컬 ToDo 데이터(수백~수천 항목), 단일 태그 필터 조회만 지원

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] 레이어 분리: 태그 검증/필터는 `todo_lib`에서 처리하고 CLI는 입력/출력만 담당한다.
- [x] 테스트 우선: 태그 추가/필터/회귀 시나리오를 unit/integration Red 테스트로 먼저 작성한다.
- [x] 최소 의존성: 기존 패키지(Typer, SQLAlchemy, pytest, pytest-cov)만 사용한다.
- [x] 단순함 우선: JSON 컬럼 + 기존 CRUD 함수 확장으로 해결하며 과도한 추상화를 도입하지 않는다.
- [x] CLI 범위 준수: REST API, GUI, Web Interface를 추가하지 않는다.

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-tags/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cli-contract.md
└── tasks.md             # Phase 2에서 생성
```

### Source Code (repository root)

```text
todo_lib/
├── models.py        # ToDoItem.tags(JSON) 필드 추가
├── validators.py    # 태그 검증 규칙 추가
├── repository.py    # 태그 저장/조회 조건 확장
└── service.py       # add/list에 tags 및 tag-filter 로직 통합

cli/
├── main.py          # list 명령에 --tag 옵션 추가
└── output.py        # 태그 표시 포맷 확장

tests/
├── unit/
│   ├── test_service_add.py
│   └── test_service_list.py
└── integration/
    ├── test_cli_add.py
    └── test_cli_list.py
```

**Structure Decision**:
- 사용자 요청에 따라 기존 `todo_lib/` 코드와 직접 통합한다.
- `models.py`에 `tags`를 JSON 컬럼으로 추가해 단순한 저장 구조를 유지한다.
- `service.py`에서 태그 검증/정규화/필터를 처리해 레이어 분리를 지킨다.
- CLI 옵션은 `cli/main.py` 명령 시그니처에 직접 추가한다 (`commands.py` 역할).
- 기존 테스트를 회귀 기준으로 유지하고 태그 관련 테스트만 증분 추가한다.

## Phase 0: Research Plan

연구 항목:
1. SQLite + SQLAlchemy에서 JSON 컬럼을 안정적으로 다루는 패턴 (기본값, null/empty list, query 조건)
2. 태그 정규화 규칙(공백 trim, case-insensitive 비교, 표시 원형 유지)과 중복 검출 전략
3. Typer에서 반복 옵션(`--tag`) 처리 방식과 에러 메시지 UX
4. 기존 테스트 불변성 보장을 위한 회귀 테스트 전략

산출물: `research.md` (모든 결정과 대안 기록)

## Phase 1: Design & Contracts

1. 데이터 모델 설계
- `ToDoItem.tags` JSON 필드, 검증 규칙, 상태 불변 조건 정의

2. CLI 계약 정의
- `add`/`list` 명령의 `--tag` 입력/필터 시그니처, 오류/성공 메시지, exit code 계약 정의

3. 실행/검증 가이드 작성
- 로컬 실행, 태그 시나리오 검증, 회귀 테스트 명령 문서화

4. 에이전트 컨텍스트 동기화
- `.github/copilot-instructions.md`의 SPECKIT 구간을 `specs/002-todo-tags/plan.md`로 갱신

산출물: `data-model.md`, `contracts/cli-contract.md`, `quickstart.md`, 업데이트된 컨텍스트 파일

## Phase 2: Task Planning Approach

`/speckit.tasks`에서 아래 순서로 작업 분해:
1. 태그 관련 unit/integration 실패 테스트 먼저 작성 (Red)
2. `models.py` + `validators.py` + `repository.py` 최소 구현 (Green)
3. `service.py` 태그 추가/필터 로직 연결
4. `cli/main.py`, `cli/output.py` 옵션/출력 반영
5. 기존 테스트 전체 회귀 실행 및 리팩터링

## Post-Design Constitution Check

- [x] 레이어 분리: 비즈니스 규칙은 `todo_lib`, CLI는 입출력으로 유지된다.
- [x] 테스트 우선: tasks 분해에서 테스트 작성이 구현보다 선행된다.
- [x] 최소 의존성: 기존 기술 스택만 사용한다.
- [x] 단순함 우선: JSON 컬럼 기반 단순 모델 확장을 채택했다.
- [x] CLI 범위 준수: CLI 외 인터페이스를 추가하지 않는다.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 없음 | N/A | N/A |
