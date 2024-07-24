from iobase import load
from random import randint, choice

class QLearning:

    def __init__(self, frame):
        self.frame = frame
        self.qtable = load('q/Q.data')    #type: dict[bytes, list[int]]

    def choice(self):
        board = self.frame.get_board()

        result = None
        exists = []
        blist = list(board)
        for i in range(len(blist)):
            if blist[i] != 0:
                exists.append(i)

        if board in self.qtable:
            rates = self.qtable[board]
            mrate = max(rates)
            indexes = []
            for i in range(len(rates)):
                if rates[i] == mrate and i not in exists:
                    indexes.append(i)
            if indexes:
                return choice(indexes)
        
        if result is None:
            print('Random')
            result = randint(0, 8)

        self.frame.choose.emit(result)
