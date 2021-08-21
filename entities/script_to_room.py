from core.persist import Base
from sqlalchemy import Column, Integer, ForeignKey

class ScriptToRoom(Base):
    __tablename__ = 'script_to_room'
    room_id   = Column(Integer, ForeignKey('room.id'), primary_key = True)
    script_id = Column(Integer, ForeignKey('script.id'), primary_key = True)

