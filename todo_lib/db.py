"""todo_lib/db.py: SQLAlchemy 엔진/세션 팩토리 및 DB 초기화."""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """SQLAlchemy 선언적 베이스 클래스."""
    pass


def get_engine(db_path: str = "todo.db"):
    """SQLite 엔진을 생성한다. busy_timeout을 5초로 설정해 동시 접근 충돌을 완화한다."""
    engine = create_engine(f"sqlite:///{db_path}")

    @event.listens_for(engine, "connect")
    def set_busy_timeout(dbapi_conn, connection_record):
        # 다른 프로세스가 DB를 점유 중일 때 최대 5초 대기한다
        dbapi_conn.execute("PRAGMA busy_timeout = 5000")

    return engine


def get_session_factory(engine) -> sessionmaker:
    """세션 팩토리를 반환한다."""
    return sessionmaker(bind=engine)


def init_db(engine) -> None:
    """모델을 임포트해 Base에 등록한 뒤 테이블을 생성한다."""
    import todo_lib.models  # noqa: F401 - Base에 모델 등록을 위한 사이드이펙트 임포트
    Base.metadata.create_all(engine)
