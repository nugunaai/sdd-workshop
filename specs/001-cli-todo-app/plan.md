# Implementation Plan: CLI 기반 ToDo 관리 앱

**Branch**: `001-cli-todo-app` | **Date**: 2026-05-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

개인 개발자를 위한 CLI ToDo 앱의 핵심 기능(추가/조회/완료/삭제)을 Python 3.12 기반으로 구현한다.
비즈니스 로직은 `todo_lib/`에 분리하고, `cli/`는 Typer 기반 명령 파싱/출력만 담당한다.
데이터 저장은 로컬 SQLite 파일(`todo.db`)과 SQLAlchemy ORM을 사용하며, 테스트는 pytest + pytest-cov로 Red-Green 순서로 진행한다.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12  
**Primary Dependencies**: Typer, SQLAlchemy (런타임), pytest, pytest-cov (dev)  
**Storage**: SQLite 로컬 파일(`todo.db`, 서버 불필요)  
**Testing**: pytest, pytest-cov  
**Target Platform**: Windows PowerShell/CMD, macOS, Linux
**Project Type**: CLI application (단일 프로젝트)  
**Performance Goals**: 1,000개 항목 기준 add/list/done/delete 명령이 체감상 즉시 응답(일반 개발자 환경에서 1초 이내)  
**Constraints**: 의존성은 `typer`, `sqlalchemy`, `pytest`, `pytest-cov` 외 추가 금지; REST API/GUI/Web 범위 제외; 테스트 우선 개발 필수  
**Scale/Scope**: 단일 사용자 로컬 ToDo 데이터(주요 사용 규모: 수백~수천 항목)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] 레이어 분리: `todo_lib/`(비즈니스)와 `cli/`(입력/출력)로 분리한다.
- [x] 테스트 우선: 각 명령 기능별 단위/통합 테스트를 Red로 먼저 작성한다.
- [x] 최소 의존성: 사용자 지정 최소 패키지(typer, sqlalchemy, pytest, pytest-cov)만 사용한다.
- [x] 단순함 우선: 인터페이스 계층(`ITodoRepository` 등) 없이 직접 클래스/함수로 구현한다.
- [x] CLI 범위 준수: 명령행 인터페이스만 구현하며 네트워크/GUI는 제외한다.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

```text
specs/001-cli-todo-app/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cli-contract.md
└── tasks.md             # Phase 2에서 생성
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. This project is CLI-only and MUST keep a single-project
  layout with clear layer separation.
-->

```text
todo_lib/
├── __init__.py
├── models.py
├── repository.py
├── service.py
└── db.py

cli/
├── __init__.py
└── main.py

tests/
├── unit/
│   ├── test_service_add.py
│   ├── test_service_list.py
│   ├── test_service_done.py
│   └── test_service_delete.py
└── integration/
  └── test_cli_commands.py
```

**Structure Decision**:
- `todo_lib/`는 SQLAlchemy 모델/저장소/도메인 서비스로 비즈니스 규칙과 영속화를 캡슐화한다.
- `cli/`는 Typer command 정의와 출력 포맷팅만 수행하고, `todo_lib.service`를 호출한다.
- `tests/unit`은 서비스 로직 중심, `tests/integration`은 CLI 명령 입출력 중심으로 분리한다.
- 패키지 관리는 `uv`를 사용한다.

## Phase 0: Research Plan

연구 항목:
1. SQLite + SQLAlchemy를 단일 사용자 CLI에서 단순/안전하게 사용하는 패턴
2. Typer command 구조와 테스트 가능한 설계 패턴
3. 날짜 입력 검증(`YYYY-MM-DD`) 및 과거 날짜 경고 처리 방식
4. 손상된 SQLite 파일 접근 실패 시 사용자 오류 메시지 표준화
5. 동시 파일 접근(다중 프로세스)에서의 현실적 처리 전략

산출물: `research.md` (모든 기술 선택과 대안 비교 기록)

## Phase 1: Design & Contracts

1. 데이터 모델 설계
- `ToDoItem` 엔티티 필드/제약/상태 전이 정의
- ID 부여, 완료 상태 전환, 삭제 규칙 명시

2. CLI 계약 정의
- `add`, `list`, `done`, `delete` 명령 시그니처/입력 검증/출력 메시지/에러 코드 정의

3. 실행 및 테스트 가이드 작성
- `uv` 기반 설치/실행/테스트/커버리지 명령 정리

4. 에이전트 컨텍스트 동기화
- `.github/copilot-instructions.md`의 SPECKIT 구간을 현재 plan 경로로 갱신

## Phase 2: Task Planning Approach

`/speckit.tasks`에서 아래 순서로 작업을 분해한다.
1. 테스트 선행 작업(단위/통합) 작성
2. `todo_lib` 최소 구현(add/list/done/delete)
3. `cli` 명령 연결과 출력 메시지 구현
4. 예외/엣지케이스 검증
5. 커버리지 기준 점검 및 리팩터링

## Post-Design Constitution Check

- [x] 레이어 분리: 설계 문서에서 `todo_lib`와 `cli` 경계가 명확하다.
- [x] 테스트 우선: Task 분해 순서가 테스트 선행을 강제한다.
- [x] 최소 의존성: 허용된 4개 패키지만 사용한다.
- [x] 단순함 우선: 추상 인터페이스 없이 직접 구현한다.
- [x] CLI 범위 준수: CLI command 외 인터페이스를 만들지 않는다.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 없음 | N/A | N/A |
