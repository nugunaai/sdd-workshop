<!--
Sync Impact Report
- Version change: N/A (template) -> 1.0.0
- Modified principles:
	- [PRINCIPLE_1_NAME] -> I. 레이어 분리
	- [PRINCIPLE_2_NAME] -> II. 테스트 우선 (NON-NEGOTIABLE)
	- [PRINCIPLE_3_NAME] -> III. 최소 의존성
	- [PRINCIPLE_4_NAME] -> IV. 단순함 우선
	- [PRINCIPLE_5_NAME] -> V. CLI 도구 구현
- Added sections:
	- 프로젝트 범위와 제약
	- 개발 워크플로와 품질 게이트
- Removed sections:
	- 없음
- Templates requiring updates:
	- ✅ updated: .specify/templates/plan-template.md
	- ✅ updated: .specify/templates/spec-template.md
	- ✅ updated: .specify/templates/tasks-template.md
	- ✅ updated: .specify/templates/commands/*.md (해당 파일 없음, 점검 완료)
- Follow-up TODOs:
	- 없음
-->

# CLI ToDo App Constitution

## Core Principles

### I. 레이어 분리
비즈니스 로직은 반드시 사용자 인터페이스 레이어와 분리된 독립 레이어에 구현한다.
CLI 입력 파싱, 출력 포맷팅, 입출력 에러 처리는 Interface Layer에서만 수행하며,
도메인 규칙과 상태 변경은 Application/Domain Layer에서만 수행한다.
이 원칙은 테스트 용이성과 변경 내성을 보장하기 위한 비타협 규칙이다.

### II. 테스트 우선 (NON-NEGOTIABLE)
모든 기능은 구현 코드보다 테스트 코드가 먼저 작성되어야 하며,
테스트 실패(Red) 상태를 확인한 뒤에만 구현(Green)으로 진행한다.
테스트가 없는 구현 코드는 병합할 수 없다.
이 원칙은 회귀 방지와 요구사항 검증을 위한 최소 품질 게이트다.

### III. 최소 의존성
외부 패키지는 표준 라이브러리로 해결 불가능한 명확한 요구가 있을 때만 도입한다.
새 의존성 도입 시 목적, 대안 검토 결과, 유지보수 비용을 문서화해야 한다.
불필요한 의존성 추가는 금지한다.
이 원칙은 보안 표면과 유지비를 줄이고 장기 안정성을 높인다.

### IV. 단순함 우선
현재 요구사항을 충족하는 가장 단순하고 직접적인 설계를 우선한다.
지금 필요하지 않은 추상화, 일반화, 확장 포인트는 도입하지 않는다.
복잡한 구조가 필요하다고 판단되면, 단순 대안이 왜 불충분한지 근거를 먼저 제시해야 한다.
이 원칙은 구현 속도와 가독성을 높이고 과설계를 방지한다.

### V. CLI 도구 구현
이 프로젝트는 터미널에서 실행되는 생산성 관리 CLI 도구를 만든다.
REST API 서버, GUI, 웹 인터페이스 구현은 프로젝트 범위 밖이며 계획/설계/작업에
포함할 수 없다.
이 원칙은 제품 방향성과 납품 경계를 명확히 유지한다.

## 프로젝트 범위와 제약

- 애플리케이션 타입은 단일 CLI 애플리케이션으로 한정한다.
- 사용자 상호작용 채널은 명령행 인자와 표준 입출력(stdin/stdout/stderr)만 허용한다.
- 네트워크 API 제공, 브라우저 렌더링, 데스크톱 UI 프레임워크 도입은 금지한다.
- 구조 기본값은 src/cli, src/application, src/domain, tests 계층을 따른다.

## 개발 워크플로와 품질 게이트

1. 요구사항 단위로 테스트 시나리오를 먼저 작성하고 실패를 확인한다.
2. 최소 구현으로 테스트를 통과시킨다.
3. 필요 시 리팩터링하되 테스트 그린 상태를 유지한다.
4. 코드 리뷰에서 다음 항목을 반드시 확인한다:
	- 레이어 침범 여부
	- 테스트 선행 여부와 커버리지 적합성
	- 의존성 추가 근거
	- CLI 범위 위반 여부

## Governance

이 Constitution은 프로젝트의 최상위 개발 규범이며, 하위 계획/명세/작업 문서는
본 문서와 충돌할 수 없다.

개정 절차:
1. 개정 제안은 변경 배경, 영향 범위, 마이그레이션 필요 여부를 포함해야 한다.
2. 최소 1회 이상 동료 리뷰를 거쳐 승인한다.
3. 승인 시 관련 템플릿과 가이드를 동일 커밋 또는 연속 커밋으로 동기화한다.

버전 정책(SemVer):
- MAJOR: 원칙 삭제, 원칙 의미의 비호환 재정의, 거버넌스의 파괴적 변경
- MINOR: 새 원칙/섹션 추가, 기존 규칙의 실질적 확장
- PATCH: 의미 변화 없는 문구 명확화, 오탈자 수정, 표현 정리

컴플라이언스 검토:
- 모든 Plan은 Constitution Check 게이트를 통과해야 한다.
- 모든 Spec은 범위 준수(CLI only)와 테스트 가능성을 명시해야 한다.
- 모든 Tasks는 테스트 선행 작업이 구현 작업보다 앞서야 한다.
- 분기별 1회 이상 원칙 준수 여부를 점검하고 필요 시 개정안을 발의한다.

**Version**: 1.0.0 | **Ratified**: 2026-05-02 | **Last Amended**: 2026-05-02
