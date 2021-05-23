
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
