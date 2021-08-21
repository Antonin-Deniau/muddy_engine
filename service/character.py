from core.persist import session
from entities.room import Room
from entities.character import Character

class CharacterService:
    def __init__(self):
        self.session = session
    
    def create_character(self, name, nick, user, previous_location):
        char = Character(name=name,
                         nick=nick,
                         user=user,
                         room=self.session.query(Room).filter(Room.id == 0).one_or_none())

        self.session.add(char)
        self.session.commit()
        return char

    def find_character(self, user, name):
        char = self.session.query(Character).filter(Character.name == name, Character.user == user).one_or_none()

        if name == None:
            raise ClientEx("Character does not exist")

        return char

character_service = CharacterService()
