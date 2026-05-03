# Research: ToDo 태그 기능 추가

## Decision 1: `tags`는 SQLAlchemy JSON 컬럼으로 저장
- Decision: `todo_lib.models.ToDoItem`에 `tags` JSON 컬럼을 추가하고, 각 항목의 태그를 문자열 리스트로 저장한다.
- Rationale: 사용자 요구가 "JSON 컬럼(단순함 우선)"으로 명시되어 있고, 별도 조인 테이블 없이 기존 모델 확장만으로 구현 가능하다.
- Alternatives considered:
  - 태그 전용 테이블 + 관계 매핑: 정규화 장점이 있지만 현재 스코프 대비 복잡도 증가
  - 문자열 CSV 저장: 파싱/검증/정확한 필터링이 취약

## Decision 2: 태그 입력 문법은 `--tag` 반복 옵션
- Decision: `todo add "제목" --tag work --tag urgent` 형태를 표준으로 사용한다.
- Rationale: Clarification 결과로 확정되었고 Typer에서 반복 옵션 처리와 UX가 단순하다.
- Alternatives considered:
  - `--tags work,urgent`: split 규칙/escape 처리가 추가로 필요
  - A/B 동시 지원: 문법 중복으로 테스트/문서 복잡도 증가

## Decision 3: 비교는 case-insensitive, 표시는 최초 입력 원형 유지
- Decision: 태그 비교 및 중복 판단은 소문자 정규화 기준으로 처리하고, 출력은 사용자가 처음 입력한 형태를 유지한다.
- Rationale: 검색 일관성과 사용자 가독성을 동시에 만족한다.
- Alternatives considered:
  - 모두 lowercase 저장/표시: 사용자 기대(입력 원형) 저하
  - case-sensitive 비교: 중복/필터의 예측 가능성 저하

## Decision 4: 태그 검증 규칙
- Decision: 태그는 최대 5개, 각 20자 이내, 허용 문자는 영문/숫자/-/_, 공백 금지, 중복 금지로 검증한다.
- Rationale: spec FR-003~FR-007, FR-016과 Clarification을 직접 충족한다.
- Alternatives considered:
  - 공백/특수문자 허용: CLI quoting 및 예외 케이스 증가
  - 길이/개수 제한 완화: 요구사항 위반

## Decision 5: 태그 필터는 service 레이어에서 기존 필터와 결합
- Decision: `service.list_todos`에 `tag` 인자를 추가하고, repository 조회에서 `is_done`, `priority`, `tag` 조건을 결합한다.
- Rationale: 기존 레이어 경계를 유지하면서 `todo list --tag` 요구를 최소 변경으로 충족한다.
- Alternatives considered:
  - CLI에서 결과 후처리 필터: 데이터 접근 책임이 CLI로 이동하여 레이어 침범
  - 태그 전용 조회 API 분리: 현재 범위 대비 과도한 분기

## Decision 6: 회귀 안정성 우선 전략
- Decision: 기존 테스트를 그대로 유지한 채 태그 시나리오 테스트를 증분 추가하고, 전체 테스트 스위트를 매번 실행한다.
- Rationale: 사용자의 "기존 테스트가 깨지지 않아야 함" 요구를 정량적으로 검증한다.
- Alternatives considered:
  - 태그 테스트만 부분 실행: 회귀 누락 위험 증가

## Notes
- 현재 CLI 파일명은 `cli/main.py`이며, 사용자 요청의 `commands.py` 역할을 해당 파일이 수행한다.
- JSON 컬럼은 SQLite에서 SQLAlchemy가 직렬화/역직렬화를 처리하므로 추가 패키지 없이 구현 가능하다.
