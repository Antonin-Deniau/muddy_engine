from core.persist import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Object(Base):
    __tablename__ = 'object'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)

    scripts = relationship('Script', secondary = 'script_to_object')

    holder_id = Column(Integer, ForeignKey('character.id'))
    holder = relationship("Character", back_populates="inventory", foreign_keys=[holder_id])

    owner_id = Column(Integer, ForeignKey('character.id'))
    owner = relationship("Character", back_populates="objects", foreign_keys=[owner_id])
