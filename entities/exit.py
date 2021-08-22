from core.persist import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

class Exit(Base):
    __tablename__ = 'exit'

    id = Column(Integer, primary_key=True)

    entry_id = Column(Integer, ForeignKey('room.id'))
    entry = relationship("Room", back_populates="entries", foreign_keys=[entry_id])

    exit_id = Column(Integer, ForeignKey('room.id'))
    exit = relationship("Room", back_populates="exits", foreign_keys=[exit_id])

    owner_id = Column(Integer, ForeignKey('character.id'))
    owner = relationship("Character", back_populates="exits", foreign_keys=[owner_id])

    scripts = relationship('Script', secondary = 'script_to_exit')

    desc = Column(String)
    name = Column(String)

    # Hooks
    async def run_on_exit(self, ws, char):
        for script in self.scripts:
            script.run_on_exit(ws, char, room)

