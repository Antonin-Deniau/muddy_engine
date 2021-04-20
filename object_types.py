import muddy

class Player:
    def __init__(self, world, name):
        self.previous_location = None
        self.location = world.get_metadata("entrypoint")
        self.world = world
        self.name = name
        self.action = None

    def move(self, new_location):
        self.previous_location = self.location.split('.')[-1]
        self.location = new_location.split('.')[-1]

class Room:
    def __init__(self, data_file, desc):
        [desc, objs] = muddy.parse(desc)
        self.ns = data_file.namespace
        self.desc = desc
        self.objs = objs


    def draw(self, player):
        keys = [e.key for e in self.objs]
        locs = [*keys, player.previous_location] if player.previous_location != None else keys

        print(self.desc)
        print("locations: {}".format(", ".join(locs)))

    def update(self, player):
        back = player.previous_location
        action = player.action

        if len(action) == 2 and action[0] == "go":
            if action[1] in [e.key for e in self.objs]:
                loc = "{}.{}".format(self.ns, action[1])

                player.move(action[1])
                print("You walk to {}".format(action[1]))
                return

            if back != None and (action[1] == back or action[1] == "back"):
                player.move(back)
                print("You walk to {}".format(back))
                return

            print("Unknown location")
            return

        print("Unknown comand")


class Container:
    def __init__(self, data_file, desc):
        [desc, items] = muddy.parse(desc)
        self.items = items
        self.desc = desc

    def draw(self, player):
        back = player.previous_location

        print(self.desc)
        if back:
            print("locations: {}".format(back))

    def update(self, player):
        back = player.previous_location
        action = player.action

        if len(action) == 2 and action[0] == "go":
            if back != None and (action[1] == back or action[1] == "back"):
                player.move(back)
                print("You walk to {}".format(back))
                return

            print("Unknown location")
            return

        print("Unknown command")


class Item:
    pass

class Potion(Item):
    def __init__(self, data_file, desc, effects):
        pass

classes = {
        "room": Room,
        "container": Container,
        "item": Item,
        "potion": Potion,
        "player": Player,
}
