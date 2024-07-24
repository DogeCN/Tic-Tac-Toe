from game.button import *

class Player(Wrapper):

    def __init__(self, index):
        self.index = index
        self.queue = ButtonQueue()

    def apply(self, button:Button):
        super().apply(button)
        self.queue.append(button)

class PlayerGroup:
    players = (Player(0), Player(1))
    _index = 0

    @property
    def index(self):
        index = self._index
        self._index = 0 if index else 1
        return index

    @property
    def queue(self):
        return self.player(0).queue + self.player(1).queue

    def player(self, index:int):
        return self.players[index]

    def apply(self, button:Button):
        player = self.players[self.index]
        player.apply(button)
