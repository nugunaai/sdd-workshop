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
uv pip install typer sqlalchemy pytest pytest-cov
```

## 3) CLI 실행
```bash
python -m cli.main --help
python -m cli.main add "문서 정리" --due 2026-05-10 --priority high
python -m cli.main list
python -m cli.main list --filter pending
python -m cli.main done 1
python -m cli.main delete 1
```

## 4) 테스트 우선 개발 루프
1. 실패 테스트 작성 (Red)
2. 최소 구현 추가 (Green)
3. 리팩터링 (Refactor)

## 5) 테스트 실행
```bash
pytest
pytest --cov=todo_lib --cov=cli --cov-report=term-missing
```

## 6) 기본 동작 확인 체크리스트
- `add`가 ID를 반환하고 항목이 저장되는가?
- `list`가 필터/우선순위를 올바르게 반영하는가?
- `done`이 상태를 변경하고 중복 완료를 안내하는가?
- `delete`가 항목을 제거하고 없는 ID를 오류 처리하는가?
