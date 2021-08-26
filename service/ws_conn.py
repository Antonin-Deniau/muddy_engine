class WsConn:
    def __init__(self):
        self.players = {}

    def add(self, player, ws):
        self.players[player.id] = ws


    def remove(self, player):
        del self.players[player.id]


    def get(self, player):
        return self.players[player.id]


ws_conn = WsConn()
