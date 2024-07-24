from iobase import load
from random import choice

class QLearning:

    def __init__(self, frame):
        self.frame = frame
        self.qtable = load('q/Q.data')    #type: dict[bytes, list[int]]

    def choice(self):

        board = self.frame.get_board()

        result = None
        empty = []
        for i in range(len(board)):
            if board[i] == 0:
                empty.append(i)

        print(board)
        board = bytes(board)

        if board in self.qtable:
            rates = self.qtable[board]
            mrate = max(rates)
            indexes = []
            for i in range(len(rates)):
                if rates[i] == mrate and i in empty:
                    indexes.append(i)
            if indexes:
                result = choice(indexes)
        
        if result is None:
            print('Random')
            result = choice(empty)

        self.frame.choose(result)
