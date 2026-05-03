# Tasks: CLI 기반 ToDo 관리 앱

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: 테스트는 선택 사항이 아니다. 모든 user story는 구현 전에 테스트 작업이 반드시 포함되어야 한다.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- CLI 및 비즈니스 레이어: `todo_lib/`, `cli/`
- 테스트: `tests/unit/`, `tests/integration/`
- 설계 문서: `specs/001-cli-todo-app/`
- REST API/GUI/Web 관련 경로는 사용하지 않는다.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 프로젝트 초기화와 공통 개발 환경 준비

- [ ] T001 Initialize uv project metadata and dependency groups in pyproject.toml
- [ ] T002 Create base package structure files in todo_lib/__init__.py and cli/__init__.py
- [ ] T003 [P] Add CLI module entrypoint scaffold in cli/main.py
- [ ] T004 [P] Add test package markers in tests/unit/__init__.py and tests/integration/__init__.py
- [ ] T005 Configure pytest and coverage defaults in pyproject.toml
- [ ] T006 [P] Add baseline test fixtures for temporary SQLite path in tests/conftest.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 모든 user story에 공통으로 필요한 핵심 기반 구현

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Implement SQLAlchemy engine/session factory and busy-timeout setup in todo_lib/db.py
- [ ] T008 [P] Implement ToDoItem ORM model schema in todo_lib/models.py
- [ ] T009 [P] Implement DB initialization and table creation helper in todo_lib/db.py
- [ ] T010 Implement repository CRUD base operations in todo_lib/repository.py
- [ ] T011 Implement shared validation helpers for title/date/priority/id in todo_lib/validators.py
- [ ] T012 [P] Implement CLI output formatting and error printing helpers in cli/output.py
- [ ] T013 Implement service-level exception classes and error mapping in todo_lib/errors.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - ToDo 항목 추가 (Priority: P1) 🎯 MVP

**Goal**: 제목/마감일/우선순위를 받아 새 항목을 저장하고 ID 포함 확인 메시지를 제공한다.

**Independent Test**: `todo add` 실행 후 DB에 항목이 저장되고, 빈 제목/잘못된 날짜 입력이 거부되는지 검증한다.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Add unit tests for add validation and ID assignment in tests/unit/test_service_add.py
- [ ] T015 [P] [US1] Add integration tests for add command success and input errors in tests/integration/test_cli_add.py
- [ ] T039 [US1] Add persistence restart integration test (process restart 후 list 재조회) in tests/integration/test_cli_persistence.py

### Implementation for User Story 1

- [ ] T016 [US1] Implement add_todo service workflow in todo_lib/service.py
- [ ] T017 [US1] Implement due-date past warning behavior in todo_lib/service.py
- [ ] T018 [US1] Wire `todo add` command options and service call in cli/main.py
- [ ] T019 [US1] Implement add command success/error/warning messages in cli/output.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - 전체 목록 조회 및 필터링 (Priority: P2)

**Goal**: 전체 목록 조회와 완료 상태/우선순위 필터링 조회를 지원한다.

**Independent Test**: 혼합 데이터에서 `todo list` 기본 조회 및 필터 조합 결과가 정확한지 검증한다.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T020 [P] [US2] Add unit tests for list filtering rules in tests/unit/test_service_list.py
- [ ] T021 [P] [US2] Add integration tests for list command outputs in tests/integration/test_cli_list.py

### Implementation for User Story 2

- [ ] T022 [US2] Implement list_todos filtering query logic in todo_lib/service.py
- [ ] T023 [US2] Wire `todo list` filter options and service call in cli/main.py
- [ ] T024 [US2] Implement list row rendering and empty-list message in cli/output.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - 항목 완료 처리 (Priority: P3)

**Goal**: ID 기준 완료 처리와 중복 완료/없는 ID 오류 응답을 지원한다.

**Independent Test**: `todo done <id>` 실행 후 상태 전환, 중복 완료 안내, 없는 ID 오류를 각각 검증한다.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T025 [P] [US3] Add unit tests for done state transition rules in tests/unit/test_service_done.py
- [ ] T026 [P] [US3] Add integration tests for done command responses in tests/integration/test_cli_done.py
- [ ] T040 [US3] Add integration test for non-numeric ID input on `todo done` in tests/integration/test_cli_done.py

### Implementation for User Story 3

- [ ] T027 [US3] Implement mark_done workflow and completed_at handling in todo_lib/service.py
- [ ] T028 [US3] Wire `todo done` command and ID parsing behavior in cli/main.py
- [ ] T029 [US3] Implement done command response messages in cli/output.py

**Checkpoint**: User Stories 1, 2, 3 should be independently functional

---

## Phase 6: User Story 4 - 항목 삭제 (Priority: P4)

**Goal**: ID 기준 영구 삭제와 없는 ID 오류 응답을 지원한다.

**Independent Test**: `todo delete <id>` 실행 후 항목 제거와 존재하지 않는 ID 오류를 검증한다.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T030 [P] [US4] Add unit tests for delete behavior in tests/unit/test_service_delete.py
- [ ] T031 [P] [US4] Add integration tests for delete command responses in tests/integration/test_cli_delete.py
- [ ] T041 [US4] Add integration test for non-numeric ID input on `todo delete` in tests/integration/test_cli_delete.py

### Implementation for User Story 4

- [ ] T032 [US4] Implement delete_todo workflow in todo_lib/service.py
- [ ] T033 [US4] Wire `todo delete` command and ID parsing behavior in cli/main.py
- [ ] T034 [US4] Implement delete command response messages in cli/output.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 전체 품질 보강과 문서/검증 마무리

- [ ] T035 [P] Add corrupted DB handling integration test in tests/integration/test_cli_system_errors.py
- [ ] T036 Implement SQLite open/read failure to exit-code mapping in cli/main.py and todo_lib/errors.py
- [ ] T037 [P] Update quickstart verification steps in specs/001-cli-todo-app/quickstart.md
- [ ] T038 Run full test and coverage command documentation update in specs/001-cli-todo-app/quickstart.md
- [ ] T042 Add measurable command-time benchmark test for SC-001 (<=30s) in tests/integration/test_cli_performance.py
- [ ] T043 Add 1,000-item responsiveness test for SC-005 in tests/integration/test_cli_performance.py
- [ ] T044 Add invalid-input matrix test for SC-003 (error message + no data corruption) in tests/integration/test_cli_validation_matrix.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - MVP baseline
- **User Story 2 (P2)**: Depends on US1 command skeleton reuse in cli/main.py
- **User Story 3 (P3)**: Depends on US1 data creation path and shared ID validation
- **User Story 4 (P4)**: Depends on US1 data creation path and shared ID validation

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Service rule implementation before CLI wiring
- CLI wiring before output polish
- Story complete before moving to next priority

### Parallel Opportunities

- T003, T004, T006 can run in parallel during Setup
- T008, T009, T012 can run in parallel during Foundational
- Each story의 테스트 2개는 [P]로 병렬 작성 가능
- T042, T043, T044는 기능 구현 완료 후 병렬로 수행 가능
- Story 간 병렬 개발은 가능하지만, 현재 계획은 커밋 단위 안정성을 위해 우선순위 순차 진행을 권장

---

## Parallel Example: User Story 1

```bash
# Run in parallel after entering Phase 3:
Task: T014 [US1] unit tests in tests/unit/test_service_add.py
Task: T015 [US1] integration tests in tests/integration/test_cli_add.py
```

## Parallel Example: User Story 2

```bash
# Run in parallel after entering Phase 4:
Task: T020 [US2] unit tests in tests/unit/test_service_list.py
Task: T021 [US2] integration tests in tests/integration/test_cli_list.py
```

## Parallel Example: User Story 3

```bash
# Run in parallel after entering Phase 5:
Task: T025 [US3] unit tests in tests/unit/test_service_done.py
Task: T026 [US3] integration tests in tests/integration/test_cli_done.py
```

## Parallel Example: User Story 4

```bash
# Run in parallel after entering Phase 6:
Task: T030 [US4] unit tests in tests/unit/test_service_delete.py
Task: T031 [US4] integration tests in tests/integration/test_cli_delete.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate with US1 unit/integration tests
5. Demo MVP (`todo add` + persistence)

### Incremental Delivery

1. Setup + Foundational 완료
2. US1 추가 후 검증
3. US2 추가 후 검증
4. US3 추가 후 검증
5. US4 추가 후 검증
6. Polish 단계에서 시스템 오류/문서/커버리지 마무리

### Commit Strategy (One Task = One Commit)

- 각 체크박스 task를 하나의 커밋 단위로 수행한다.
- 커밋 메시지는 `feat:`/`test:`/`chore:` 접두사로 task ID를 포함한다.
- 예: `test: T014 add unit tests for add_todo validation`

---

## Notes

- [P] tasks는 서로 다른 파일을 변경하도록 분해했다.
- [Story] 라벨은 User Story phase에만 부여했다.
- 모든 user story는 독립 테스트 기준을 포함한다.
- spec, plan, tasks는 SQLite + SQLAlchemy 결정으로 정렬했다.
