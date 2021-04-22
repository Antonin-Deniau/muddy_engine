class ClientEx(Exception):
    def __init__(self, message):
        self.message = message


class ExitEx(Exception):
    pass

