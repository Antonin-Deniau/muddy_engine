from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from persist import Base, Session

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nick = Column(String)
    previous_location = Column(String)
    location = Column(String)

    user = relationship("User")

    #Transcient properties
    def __init__(self):
        self.action = None
        self.world = None

    def set_action(self, action):
        self.action = action
    
    def get_action(self):
        return self.action

    def set_world(self, world):
        self.world = world

    def get_world(self):
        return self.world


class CharacterRepository:
    def __init__(self):
        self.session = Session()

character_repository = CharacterRepository()
