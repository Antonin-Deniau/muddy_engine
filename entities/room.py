from core.utils import prn
from core.persist import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    spawn = Column(Boolean)

    characters = relationship("Character", back_populates="room")

    scripts = relationship('Script', secondary = 'script_to_room')

    exits = relationship("Exit", back_populates="exit", foreign_keys=[Exit.exit_id])
    entries = relationship("Exit", back_populates="entry", foreign_keys=[Exit.entry_id])


    async def run(self, ws, char):
        await prn(ws, self.desc)

        for script in self.scripts:
            script.run_in_room(ws, char)

