"""tests/conftest.py: 임시 SQLite DB를 사용하는 공통 pytest fixture."""
import pytest
from todo_lib.db import get_engine, get_session_factory, init_db


@pytest.fixture
def db_session(tmp_path):
    """임시 SQLite DB에 연결된 세션 fixture (테스트 종료 후 자동 해제)."""
    db_path = str(tmp_path / "test.db")
    engine = get_engine(db_path)
    init_db(engine)
    Session = get_session_factory(engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture
def db_path(tmp_path):
    """임시 SQLite DB 파일 경로 fixture."""
    return str(tmp_path / "test.db")
