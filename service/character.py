from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from core.persist import Base, session

class Character(Base):
    __tablename__ = 'character'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nick = Column(String)
    previous_location = Column(String)
    location = Column(String)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="characters")


    #Transcient properties
    def __init__(self, **kwargs):
        #self.action = kwargs['location']
        #kwargs.pop('location')

        self.action = None
        self.location = ""
        self.previous_location = ""
        self.world = None
        
        self.name = kwargs["name"]
        self.nick = kwargs["nick"]
        self.user = kwargs["user"]
        self.previous_location = kwargs["previous_location"]
        self.location = kwargs["location"]

    def set_action(self, action):
        self.action = action
    
    def get_action(self):
        return self.action

    def set_world(self, world):
        self.world = world

    def get_world(self):
        return self.world


class CharacterService:
    def __init__(self):
        self.session = session
    
    def create_character(self, name, nick, user, previous_location, location):
        char = Character(name=name, nick=nick, user=user, previous_location=previous_location, location=location)
        self.session.add(char)
        self.session.commit()
        return char

character_service = CharacterService()
