from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/test_work"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
conn = engine.connect()

class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = "test_work"

    id: int = Column(Integer, primary_key = True, index = True, autoincrement = True)
    fio: str = Column(String)


Base.metadata.create_all(bind=engine)