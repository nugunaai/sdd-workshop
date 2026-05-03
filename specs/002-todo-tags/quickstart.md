# Quickstart: ToDo 태그 기능 통합

## Prerequisites
- Python 3.12
- uv

## 1) 환경 준비
```bash
uv venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
# source .venv/bin/activate
```

## 2) 의존성 동기화
```bash
uv sync
```

## 3) 태그 기능 실행 예시
```bash
# 태그 없이 추가 (기존 동작 유지)
todo add "문서 정리"

# 태그 포함 추가 (--tag 반복)
todo add "릴리즈 준비" --priority high --tag work --tag release

# 전체 조회
todo list

# 태그 필터 조회
todo list --tag work

# 복합 필터 조회
todo list --filter pending --priority high --tag release
```

## 4) 테스트 우선 개발 루프
1. 태그 관련 실패 테스트 작성 (Red)
2. 최소 구현으로 통과 (Green)
3. 회귀 포함 리팩터링 (Refactor)

## 5) 테스트 실행
```bash
# 전체 회귀 (기존 + 신규)
uv run pytest tests/ -v

# 태그 관련 통합 테스트 우선 실행
uv run pytest tests/integration/test_cli_add.py tests/integration/test_cli_list.py -v

# 태그 관련 서비스 테스트 우선 실행
uv run pytest tests/unit/test_service_add.py tests/unit/test_service_list.py -v

# 커버리지 확인
uv run pytest tests/ --cov --cov-report=term-missing
```

## 6) 검증 체크리스트
- `add --tag`가 최대 5개/20자/허용 문자 규칙을 지키는가?
- 중복 태그(case-insensitive)가 거부되는가?
- `list --tag`가 정확히 일치 항목만 반환하는가?
- 태그 미사용 기존 명령 흐름이 동일하게 동작하는가?
- 전체 테스트 스위트가 green 상태인가?
