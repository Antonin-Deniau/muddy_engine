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
    room = relationship("Room", foreign_keys=[room_id])

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="characters")

    inventory = relationship("Object", back_populates="holder", foreign_keys="Object.holder_id")


    # CREATED MUD OBJECTS
    scripts = relationship("Script", back_populates="owner")
    exits = relationship("Exit", back_populates="owner")
    rooms = relationship("Room", back_populates="owner", foreign_keys="Room.owner_id")
    objects = relationship("Object", back_populates="owner", foreign_keys="Object.owner_id")

