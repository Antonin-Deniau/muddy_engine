from core.exceptions import ClientEx
from core.persist import session
from entities.room import Room
from entities.exit import Exit
from entities.character import Character
from core.exceptions import ClientEx



import traceback
from service.room import room_service

class CharacterService:
    def __init__(self):
        self.session = session
    
    def create_character(self, name, nick, user):
        char = Character(name=name,
                         nick=nick,
                         user=user,
                         room=self.session.query(Room).filter(Room.spawn == True).one_or_none())

        self.session.add(char)
        self.session.commit()
        return char

    def find_character(self, user, name):
        char = self.session.query(Character).filter(
                Character.name == name,
                Character.user == user).one_or_none()
        if char == None:
            raise ClientEx("Character does not exist")

        return char

    async def list_inventory(self, ws, user):
        await prn(ws, "Inventory:")
        for obj in user.inventory:
            await prn(ws, "\t- [#{}] {}\t({})".format(obj.id, obj.name, obj.desc))


    async def move_character(self, ws, user, data):
        args = data["content"]
        exit = self.session.query(Exit).filter(
                Exit.exit_id == user.room_id,
                Exit.id == args[0]).one_or_none()

        if exit == None: raise ClientEx("Exit {} does not exist".format(args[0]))

        try:
            await user.room.room_leave(ws, user)
            await exit.run_on_exit(ws, user)

            if exit.entry == None: raise ClientEx("This exit lead nowhere.")

            user.room = exit.entry
            await user.room.room_enter(ws, user)
            await room_service.look_user_room(ws, user)

            self.session.commit()
        except ClientEx as e:
            raise ClientEx(e)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.session.rollback()

character_service = CharacterService()
