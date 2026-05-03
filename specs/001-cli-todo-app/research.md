# Research: CLI 기반 ToDo 관리 앱

## Decision 1: 로컬 저장소는 SQLite + SQLAlchemy 사용
- Decision: 데이터 저장소는 SQLite(`todo.db`)를 사용하고 ORM은 SQLAlchemy를 사용한다.
- Rationale: 사용자 요구사항에서 저장소를 SQLite로 지정했고, SQLAlchemy는 모델/쿼리/트랜잭션 처리를 일관되게 유지한다. 단일 사용자 CLI 스코프에서 서버 없이 로컬 파일 기반으로 충분하다.
- Alternatives considered:
  - JSON 파일(`todo.json`): 단순하지만 동시성/무결성/질의 확장성 측면에서 취약
  - CSV: 스키마 제약과 상태 전환 처리에 부적합

## Decision 2: CLI 프레임워크는 Typer 사용
- Decision: CLI entrypoint는 Typer로 구현한다.
- Rationale: 사용자 요구사항으로 고정되었고, subcommand 선언과 help 제공이 간결하다.
- Alternatives considered:
  - argparse: 의존성 최소 측면 장점이 있으나 요구사항에서 Typer 지정
  - Click: Typer의 기반이지만 type hint 중심 개발 경험 측면에서 Typer가 적합

## Decision 3: 테스트 도구는 pytest + pytest-cov
- Decision: 단위 테스트와 CLI 통합 테스트를 pytest로 작성하고 pytest-cov로 커버리지를 측정한다.
- Rationale: Constitution의 테스트 우선 원칙을 만족하고 Python 생태계 표준 도구 조합이다.
- Alternatives considered:
  - unittest: 내장 도구지만 fixture/parametrize 측면에서 pytest가 효율적

## Decision 4: 날짜 검증 정책
- Decision: 날짜 입력은 `YYYY-MM-DD` 형식만 허용한다. 형식 오류는 저장 거부, 과거 날짜는 경고 후 저장 허용.
- Rationale: spec의 FR-012, FR-014를 직접 만족한다.
- Alternatives considered:
  - 자연어 날짜 파싱: 의존성 증가와 모호성 증가
  - 과거 날짜 거부: 사용 시나리오 제약이 과도함

## Decision 5: 손상 데이터 파일 처리 정책
- Decision: DB 파일 접근/파싱 실패 시 명확한 오류 메시지를 출력하고 종료한다.
- Rationale: 자동 복구는 오탐/데이터 유실 위험이 있고 단순함 원칙에 반한다.
- Alternatives considered:
  - 자동 복구/초기화: 사용자 데이터 유실 가능성
  - 백업 후 자동 재생성: 복잡도 증가

## Decision 6: 동시 접근 처리
- Decision: 기본 정책은 단일 사용자/단일 프로세스 사용을 권장한다. 다중 프로세스 접근 시 SQLite 트랜잭션 및 busy timeout으로 충돌을 완화하고, lock timeout 발생 시 사용자에게 재시도 메시지를 제공한다.
- Rationale: spec의 단일 사용자 가정과 현실적 CLI 사용 패턴을 유지하면서 최소한의 안전장치를 제공한다.
- Alternatives considered:
  - 파일 잠금 전용 구현: 플랫폼별 차이와 복잡도 증가
  - 별도 서버형 DB: 범위 위반

## Decision 7: 의존성 정책 검증
- Decision: 패키지는 `typer`, `sqlalchemy`, `pytest`, `pytest-cov`만 사용한다.
- Rationale: 사용자 지정 최소 의존성 규칙 준수.
- Alternatives considered:
  - pydantic/dateutil 등 추가 패키지: 현재 요구사항 충족에 불필요

## Notes
- 현재 spec의 일부 문구(JSON 저장 가정)는 사용자 최신 지시(SQLite)와 상충한다.
- 구현 시에는 본 plan 기준(SQLite)을 따르고, 후속 spec 동기화를 권장한다.
