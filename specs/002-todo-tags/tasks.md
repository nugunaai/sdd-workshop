# Tasks: ToDo 태그 기능 추가

**Input**: Design documents from `/specs/002-todo-tags/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-contract.md, quickstart.md

**Tests**: 모든 user story는 구현 전에 테스트 작업을 반드시 포함한다.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 구현 시작 전 공통 기준과 회귀 베이스라인 확정

- [ ] T001 기존 전체 테스트를 실행해 baseline 통과를 확인하고 결과를 specs/002-todo-tags/checklists/requirements.md에 기록
- [ ] T002 태그 기능 구현 범위/파일 매핑을 specs/002-todo-tags/plan.md 기준으로 점검하고 작업 순서를 specs/002-todo-tags/tasks.md에 확정

**Checkpoint**: 기존 테스트 전체 통과가 첫 번째 확인 기준으로 충족되어야 다음 단계 진행

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 모든 user story가 공통으로 의존하는 태그 인프라 구축

**⚠️ CRITICAL**: 이 단계 완료 전에는 어떤 user story도 구현하지 않는다.

- [ ] T003 [P] ToDoItem에 JSON tags 필드와 기본값 규칙을 추가 in todo_lib/models.py
- [ ] T004 [P] 태그 검증/정규화/중복 검사 유틸을 추가 in todo_lib/validators.py
- [ ] T005 create_todo/get_all_todos 시그니처에 tags/tag 인자를 추가 in todo_lib/repository.py
- [ ] T006 legacy row에서 tags 누락 시 빈 리스트로 처리하는 공통 호환 로직을 추가 in todo_lib/repository.py

**Checkpoint**: 태그 데이터 저장/조회의 공통 기반이 준비되어 user story 구현 가능

---

## Phase 3: User Story 1 - 태그가 있는 ToDo 생성 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 `todo add`에서 반복 `--tag` 옵션으로 태그를 저장할 수 있다.

**Independent Test**: `todo add "제목" --tag work --tag urgent`가 성공하고, 6개 초과/20자 초과/허용 문자 위반/중복 태그가 모두 거부되면 완료.

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T007 [P] [US1] 태그 입력 검증(unit) 테스트를 추가 in tests/unit/test_service_add.py
- [ ] T008 [P] [US1] `todo add --tag` 성공/실패(integration) 테스트를 추가 in tests/integration/test_cli_add.py

### Implementation for User Story 1

- [ ] T009 [US1] add_todo에 tags 인자 및 검증/정규화 로직을 구현 in todo_lib/service.py
- [ ] T010 [US1] create_todo 경로에 tags 저장을 구현 in todo_lib/repository.py
- [ ] T011 [US1] add 명령에 반복 `--tag` 옵션을 연결 in cli/main.py
- [ ] T012 [US1] add 관련 오류 메시지 매핑을 계약에 맞게 조정 in cli/main.py

**Checkpoint**: 태그 생성 기능이 독립적으로 동작하고 관련 테스트가 통과

---

## Phase 4: User Story 2 - 태그로 목록 필터링 (Priority: P2)

**Goal**: 사용자가 `todo list --tag <tag>`로 태그 기반 조회를 수행할 수 있다.

**Independent Test**: 태그가 섞인 데이터에서 `--tag` 조회 시 해당 태그 항목만 반환되고, 조건 불일치 시 빈 결과 메시지가 출력되면 완료.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T013 [P] [US2] 태그 필터 service(unit) 테스트를 추가 in tests/unit/test_service_list.py
- [ ] T014 [P] [US2] `todo list --tag` 및 복합 필터(integration) 테스트를 추가 in tests/integration/test_cli_list.py

### Implementation for User Story 2

- [ ] T015 [US2] list_todos에 tag 필터 인자를 추가하고 필터 조합 로직을 구현 in todo_lib/service.py
- [ ] T016 [US2] get_all_todos에 tag 조건 조회를 구현 in todo_lib/repository.py
- [ ] T017 [US2] list 명령에 `--tag` 옵션을 추가하고 service 인자를 연결 in cli/main.py
- [ ] T018 [US2] 목록 출력에 tags 필드를 포함하도록 포맷을 확장 in cli/output.py

**Checkpoint**: 태그 필터 조회 기능이 독립적으로 동작하고 관련 테스트가 통과

---

## Phase 5: User Story 3 - 기존 ToDo 흐름 유지 (Priority: P3)

**Goal**: 태그 기능 추가 후에도 기존 add/list/done/delete 동작이 회귀 없이 유지된다.

**Independent Test**: 태그 미사용 시나리오의 기존 테스트가 동일하게 통과하고, done/delete가 태그 유무와 무관하게 동작하면 완료.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T019 [P] [US3] 기존 동작 회귀 매트릭스 테스트를 보강 in tests/integration/test_cli_validation_matrix.py
- [ ] T020 [P] [US3] 태그 포함/미포함 persistence 회귀 테스트를 보강 in tests/integration/test_cli_persistence.py

### Implementation for User Story 3

- [ ] T021 [US3] done/delete 흐름이 tags 필드와 독립적으로 유지되도록 서비스 로직을 점검/보완 in todo_lib/service.py
- [ ] T022 [US3] 기존 출력 계약과 태그 출력 확장을 함께 만족하도록 출력 로직을 보정 in cli/output.py
- [ ] T023 [US3] 회귀 시나리오 기준으로 오류 코드/메시지 호환성을 보정 in cli/main.py

**Checkpoint**: 기존 핵심 기능 회귀 없이 태그 기능과 함께 동작

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 전 스토리 공통 마무리

- [ ] T024 [P] 전체 테스트 및 커버리지 명령을 실행하고 결과를 확인 in specs/002-todo-tags/quickstart.md
- [ ] T025 [P] 태그 기능 사용 예시와 검증 체크리스트를 최신 구현에 맞게 정리 in specs/002-todo-tags/quickstart.md
- [ ] T026 contracts와 plan 간 불일치 여부를 점검/정리 in specs/002-todo-tags/contracts/cli-contract.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 즉시 시작 가능
- **Phase 2 (Foundational)**: Phase 1 완료 후 시작, 모든 user story를 block
- **Phase 3~5 (User Stories)**: Phase 2 완료 후 시작
  - 우선순위 권장 순서: US1 → US2 → US3
- **Phase 6 (Polish)**: 모든 user story 완료 후 시작

### User Story Dependencies

- **US1 (P1)**: Foundational 완료 후 독립 진행 가능
- **US2 (P2)**: Foundational 완료 후 진행 가능, US1 산출(tags 저장)이 있으면 검증이 용이
- **US3 (P3)**: US1/US2 반영 이후 회귀 검증 단계로 진행

### Within Each User Story

- 테스트 작성 및 실패 확인 후 구현 시작
- service/repository 핵심 로직 반영 후 CLI 연결
- story별 테스트 green 확인 후 다음 단계 진행

### Parallel Opportunities

- Phase 2의 T003, T004는 병렬 가능
- US1 테스트 T007, T008 병렬 가능
- US2 테스트 T013, T014 병렬 가능
- US3 테스트 T019, T020 병렬 가능
- Polish의 T024, T025, T026은 상호 파일 충돌이 없도록 분배 시 병렬 가능

---

## Parallel Example: User Story 1

```bash
# 테스트 병렬 준비
Task: T007 [US1] tests/unit/test_service_add.py
Task: T008 [US1] tests/integration/test_cli_add.py

# 구현 병렬 준비(파일 분리 시)
Task: T010 [US1] todo_lib/repository.py
Task: T011 [US1] cli/main.py
```

## Parallel Example: User Story 2

```bash
# 테스트 병렬 준비
Task: T013 [US2] tests/unit/test_service_list.py
Task: T014 [US2] tests/integration/test_cli_list.py

# 구현 병렬 준비(파일 분리 시)
Task: T016 [US2] todo_lib/repository.py
Task: T017 [US2] cli/main.py
```

## Parallel Example: User Story 3

```bash
# 회귀 테스트 병렬 준비
Task: T019 [US3] tests/integration/test_cli_validation_matrix.py
Task: T020 [US3] tests/integration/test_cli_persistence.py
```

---

## Implementation Strategy

### MVP First (US1 우선)

1. Phase 1 완료 (기존 테스트 baseline 통과 필수)
2. Phase 2 완료 (공통 태그 인프라)
3. Phase 3 완료 (US1)
4. US1 독립 검증 후 공유

### Incremental Delivery

1. US1 완료 후 태그 저장 가치 제공
2. US2 추가로 검색 가치 제공
3. US3 회귀 안정성 확보 후 마무리

### Quality Gate

- 각 단계 완료 시 `uv run pytest tests/ -v` 통과를 확인한다.
- 최종 단계에서 커버리지 포함 명령으로 회귀 위험을 점검한다.
