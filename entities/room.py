from core.utils import prn
from core.persist import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from entities.exit import Exit
from entities.character import Character

class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    spawn = Column(Boolean)

    characters = relationship("Character", back_populates="room", foreign_keys=[Character.room_id])

    scripts = relationship('Script', secondary = 'script_to_room')

    exits = relationship("Exit", back_populates="exit", foreign_keys=[Exit.exit_id])
    entries = relationship("Exit", back_populates="entry", foreign_keys=[Exit.entry_id])

    owner_id = Column(Integer, ForeignKey('character.id'))
    owner = relationship("Character", back_populates="rooms", foreign_keys=[owner_id])


    async def room_exit(self, ws, char):
        for script in self.scripts:
            script.run_in_room_exit(ws, char, room)

    async def room_enter(self, ws, char):
        await prn(ws, self.desc)

        for script in self.scripts:
            script.run_in_room_enter(ws, char, room)

