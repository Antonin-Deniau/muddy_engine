from core.persist import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Script(Base):
    __tablename__ = 'script'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    perms = Column(Integer)
    code = Column(String)

    owner = relationship("Character", remote_side=[id] backref="scripts")

