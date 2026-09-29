from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import String, Integer, Column, BLOB
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass
class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    algo = Column(String(255))
    n_max = Column(Integer)
    steps = Column(Integer)
    image = Column(BLOB)
     
Base.metadata.create_all(engine)
