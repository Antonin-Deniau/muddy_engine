import muddy_parser

class Player:
    def __init__(self, world, name):
        self.previous_location = None
        self.location = world.get_metadata("entrypoint")
        self.world = world
        self.name = name
        self.action = None

    def move(self, new_location):
        self.previous_location = self.location
        self.location = new_location

class Room:
    def __init__(self, data_file, name, desc):
        [desc, objs] = muddy_parser.parse(desc)
        self.ns = data_file.namespace
        self.desc = desc
        self.name = name
        self.objs = { k.key.split(".")[-1]: { "entity": data_file.get_object(k.key), "desc": k.vals } for k in objs }
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
                loc = self.objs[action[1]]

                self.move_player(player, loc["entity"].name)
                print("You walk to {}".format(loc["desc"]))
                return

            if back != None or action[1] == "back":
                self.move_player(player, back)
                return

            print("Unknown location")
            return

        print("Unknown comand")


class Container:
    def __init__(self, data_file, name, desc):
        [desc, items] = muddy_parser.parse(desc)
        self.name = name
        self.items = items
        self.desc = desc
        
    def load(self, player):
        pass
    
    def draw(self, player):
        print(self.desc)
        print("locations: back")

    def update(self, player):
        back = player.previous_location
        action = player.action

        if len(action) == 2 and action[0] == "go":
            if back != None and action[1] == "back":
                player.move(back)
                return

            print("Unknown location")
            return

        print("Unknown command")


class Item:
    pass

class Potion(Item):
    def __init__(self, data_file, name, desc, effects):
        pass

classes = {
        "room": Room,
        "container": Container,
        "item": Item,
        "potion": Potion,
        "player": Player,
}
