from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Signal
from game.board import Board
from threading import Thread
from random import randint
from iobase import dump, load
import time

class MainWindow(QMainWindow):
    choose = Signal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(100, 100, 400, 400)
        Center = QWidget(self)
        self.setCentralWidget(Center)
        self.board = Board(Center)

        self.choose.connect(self.choose_)
    
    def choose_(self, index:int):
        self.board.buttons[index].click()

    def get_(self, current:int):
        board = [0 for _ in range(9)]
        for player in self.board.group.players:
            for button in player.queue:
                sign = button.sign
                board[button.row * 3 + button.column] = sign if player.index == current else 256-sign
        return bytes(board)

class QLearning:

    def __init__(self):
        self.qtable = {} #type: dict[bytes, list[float]]
        self.choices = [] #type: list[tuple[list, int]]

    def choice(self, board:bytes = None):
        exists = []
        if board:
            blist = list(board)
            for i in range(len(blist)):
                if blist[i] != 0:
                    exists.append(i)
        else:
            board = bytes([0 for _ in range(9)])
        print(board)
        if board in self.qtable:
            rates = self.qtable[board]
            mrate = max(rates)
            indexes = []
            for i in range(len(rates)):
                if rates[i] == mrate:
                    indexes.append(i)
            ri = indexes[randint(0, len(indexes)-1)]
            while ri in exists:
                ri = indexes[randint(0, len(indexes)-1)]
            self.choices.append((rates, ri))
            return ri
        else:
            return self.rand_choice(board, exists)

    def rand_choice(self, board, exists):
        empty = [0 for _ in range(9)]
        self.qtable[board] = empty
        ri = randint(0, 8)
        while ri in exists:
            ri = randint(0, 8)
        self.choices.append((empty, ri))
        return ri

    def reward(self, reward:int):
        for rates, ri in self.choices:
            rates[ri] += reward

class Shell:

    def __init__(self):
        self.QIntelligents = [QLearning(), QLearning()]
        self.thread = Thread(target=self.exec, daemon=True)
        self.App = QApplication()
        self.Frame = MainWindow()
    
    def exec_(self):
        self.Frame.show()
        self.thread.start()
        self.App.exec()

    def make_choice(self, index:int, current:int):
        self.Frame.choose.emit(index)
        time.sleep(0.15)
        if self.Frame.board.gaming:
            return self.Frame.get_(current)
        else:
            return False

    def ai(self, index:int):
        return self.QIntelligents[index]

    def exec(self):
        current = 0
        board = self.make_choice(self.ai(1).choice(), 1)
        while True:
            board = self.make_choice(self.ai(current).choice(board), current)
            if board:
                current = 1 - current
            else:
                self.ai(current).reward(1)
                self.ai(1-current).reward(-1)
                with open('Q1.log', 'w') as f1, open('Q2.log', 'w') as f2:
                    table1 = self.ai(0).qtable
                    for b in table1:
                        f1.write(str(list(b)) + ':' + str(table1[b]) + '\n')
                    table2 = self.ai(1).qtable
                    for b in table2:
                        f2.write(str(list(b)) + ':' + str(table2[b]) + '\n')
                self.Frame.board.restart()
                '''
                dump('Q1.data', self.ai(0).qtable)
                dump('Q2.data', self.ai(1).qtable)
                '''

shell = Shell()

'''
try:
    shell.ai(0).qtable = load('Q1.data')
    shell.ai(1).qtable = load('Q2.data')
except:
    ...
'''
shell.exec_()
