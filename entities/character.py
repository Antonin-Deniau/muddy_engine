from core.persist import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

class Character(Base):
    __tablename__ = 'character'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nick = Column(String)
    desc = Column(String)

    room_id = Column(Integer, ForeignKey('room.id'))
    room = relationship("Room", back_populates="characters")

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="characters")
