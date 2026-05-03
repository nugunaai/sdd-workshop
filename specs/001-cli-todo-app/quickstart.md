# Quickstart: CLI 기반 ToDo 관리 앱

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

## 2) 의존성 설치
```bash
uv sync
```

## 3) CLI 실행
```bash
# 진입점: pyproject.toml에 정의된 'todo' 스크립트 사용
todo --help
todo add "문서 정리" --due 2026-05-10 --priority high
todo list
todo list --filter pending
todo list --priority high
todo done 1
todo delete 1

# 또는 모듈 직접 실행
python -m cli.main --help
```

## 4) 테스트 우선 개발 루프
1. 실패 테스트 작성 (Red)
2. 최소 구현 추가 (Green)
3. 리팩터링 (Refactor)

## 5) 테스트 실행
```bash
# 기본 테스트 실행 (73개 테스트, ~20초)
uv run pytest tests/ -v

# 커버리지 포함 실행
uv run pytest tests/ --cov --cov-report=term-missing

# 특정 모듈만 실행
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v

# 성능 테스트만 실행 (1,000개 항목 기준)
uv run pytest tests/integration/test_cli_performance.py -v
```

## 6) 기본 동작 확인 체크리스트
- `add`가 ID를 반환하고 항목이 저장되는가?
- `list`가 필터/우선순위를 올바르게 반영하는가?
- `done`이 상태를 변경하고 중복 완료를 안내하는가?
- `delete`가 항목을 제거하고 없는 ID를 오류 처리하는가?
