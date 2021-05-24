from core.muddy_parser import parse

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

    def draw(self, player):
        keys = self.objs.keys()

        locs = [*keys, "back"] if player.previous_location != None else keys
        print(self.desc)
        print("Peoples in the room: {}".format(", ".join(self.players.keys())))
        print("locations: {}".format(", ".join(locs)))
        
    def load(self, player):
        self.players[player.name] = player

    def update(self, player):
        back = player.previous_location
        action = player.action

        if len(action) == 2 and action[0] == "go":
            if action[1] in self.objs.keys():
                loc = world.get_location(self.objs[action[1]])

                self.move_player(player, loc["entity"].name)
                print("You walk to {}".format(loc["desc"]))
                return

            if back != None or action[1] == "back":
                self.move_player(player, back)
                return

            print("Unknown location")
            return

        print("Unknown comand")

