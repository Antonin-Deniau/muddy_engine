from core.persist import Base
from sqlalchemy import Column, Integer, ForeignKey


class ScriptToObject(Base):
    __tablename__ = 'script_to_object'
    object_id   = Column(Integer, ForeignKey('object.id'), primary_key = True)
    script_id = Column(Integer, ForeignKey('script.id'), primary_key = True)

