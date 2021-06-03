from core.muddy_parser import parse
from core.utils import prn

class Room:
    def __init__(self, world, name, desc):
        [desc, objs] = parse(desc)
        self.world = world
        self.desc = desc
        self.name = name
        self.objs = objs
        self.players = {}
    
    def move_player(self, player, dest):
        del self.players[player.name]
        player.move(dest)

    async def draw(self, ws, player):
        keys = [x.key for x in self.objs]

        locs = [*keys, "back"] if player.previous_location != None else keys
        await prn(ws, self.desc)
        await prn(ws, "Peoples in the room: {}".format(", ".join(self.players.keys())))
        await prn(ws, "locations: {}".format(", ".join(locs)))
        
    async def load(self, ws, player):
        self.players[player.name] = player

    async def update(self, ws, player):
        back = player.previous_location
        action = player.action

        if len(action) == 2 and action[0] == "go":
            if action[1] in [x.key for x in self.objs]:
                loc = self.world.get_location(action[1])

                self.move_player(player, loc.name)
                await prn(ws, "You walk to {}".format(loc.desc))
                return

            if back != None or action[1] == "back":
                self.move_player(player, back)
                return

            await prn(ws, "Unknown location")
            return

        await prn(ws, "Unknown comand")

