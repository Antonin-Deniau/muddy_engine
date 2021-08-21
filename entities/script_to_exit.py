from core.persist import Base
from sqlalchemy import Column, Integer, ForeignKey

class ScriptToExit(Base):
    __tablename__ = 'script_to_exit'
    exit_id   = Column(Integer, ForeignKey('exit.id'), primary_key = True)
    script_id = Column(Integer, ForeignKey('script.id'), primary_key = True)

