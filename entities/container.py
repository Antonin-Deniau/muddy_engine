from core.muddy_parser import parse
from core.utils import prn

class Container:
    def __init__(self, world, name, desc):
        [desc, items] = parse(desc)
        self.name = name
        self.items = items
        self.desc = desc
        
    async def load(self, ws, player):
        pass
    
    async def draw(self, ws, player):
        await prn(ws, self.desc)
        await prn(ws, "locations: back")

    async def update(self, ws, player):
        back = player.previous_location
        action = player.action

        if len(action) == 2 and action[0] == "go":
            if back != None and action[1] == "back":
                player.move(back)
                return

            await prn(ws, "Unknown location")
            return

        await prn(ws, "Unknown command")
