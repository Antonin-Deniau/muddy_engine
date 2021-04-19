import muddy

class Room:
    def __init__(self, data_file, desc):
        [desc, objs] = muddy.parse(desc)
        self.ns = data_file.namespace
        self.desc = desc
        self.objs = objs


    def draw(self, gamestate):
        back = gamestate["previous_location"] if "previous_location" in gamestate else None

        print(self.desc)

        keys = [e.key for e in self.objs]
        locs = [*keys, back] if back != None else keys
        print("locations: {}".format(", ".join(locs)))

    def update(self, gamestate):
        back = gamestate["previous_location"] if "previous_location" in gamestate else None
        action = gamestate["action"]

        if len(action) == 2 and action[0] == "go":
            if action[1] in [e.key for e in self.objs]:
                loc = "{}.{}".format(self.ns, action[1])

                gamestate["previous_location"] = gamestate["location"].split('.')[-1]
                gamestate["location"] = action[1].split(':')[-1]
                print("You walk to {}".format(action[1]))
                return gamestate

            if back != None and (action[1] == back or action[1] == "back"):
                gamestate["previous_location"] = gamestate["location"]
                gamestate["location"] = back
                print("You walk to {}".format(back))
                return gamestate

            print("Unknown location")
            return gamestate

        print("Unknown comand")
        return gamestate


class Container:
    def __init__(self, data_file, desc, items={}):
        [desc, objs] = muddy.parse(desc)
        self.items = items
        self.desc = desc

    def draw(self, gamestate):
        back = gamestate["previous_location"] if "previous_location" in gamestate else None

        print(self.desc)
        if back:
            print("locations: {}".format(back))

    def update(self, gamestate):
        back = gamestate["previous_location"] if "previous_location" in gamestate else None
        action = gamestate["action"]

        if len(action) == 2 and action[0] == "go":
            if back != None and (action[1] == back or action[1] == "back"):
                gamestate["previous_location"] = gamestate["location"]
                gamestate["location"] = back
                print("You walk to {}".format(back))
                return gamestate

            print("Unknown location")
            return gamestate

        print("Unknown command")
        return gamestate


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
}
