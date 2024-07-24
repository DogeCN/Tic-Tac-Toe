from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Signal
from game.board import Board
from threading import Thread
import time

class MainWindow(QMainWindow):
    choose = Signal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(100, 100, 400, 400)
        Center = QWidget(self)
        self.setCentralWidget(Center)
        self.broad = Board(Center)

        self.choose.connect(self.choose_)
    
    def choose_(self, index:int):
        self.broad.buttons[index].click()

    def get_(self, current:int):
        broad = [0 for _ in range(9)]
        for player in self.broad.group.players:
            for button in player.queue:
                sign = button.sign
                broad[button.row * 3 + button.column] = sign if player.index == current else 256-sign
        return bytes(broad)

class QLearning:
    qtable = {} #type: dict[bytes, list[float]]
    choices = [] #type: list[tuple[list, int]]

    def choice(self, broad:bytes = None):
        if not broad:
            broad = bytes([0 for _ in range(9)])

        if broad in self.qtable:
            rates = self.qtable[broad]
            mrate = max(rates)
            indexes = []
            for i in range(len(rates)):
                if rates[i] == mrate:
                    indexes.append(i)
            ri = indexes[self.random(len(indexes))]
            self.choices.append((rates, ri))
            return rates[ri]
        else:
            empty = [0 for _ in range(9)]
            self.qtable[broad] = empty
            ri = self.random(9)
            self.choices.append((empty, ri))
            return ri

    @staticmethod
    def random(max):
        return int(time.time()) % max

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
        if self.Frame.broad.gaming:
            return self.Frame.get_(current)
        else:
            return False

    def ai(self, index:int):
        return self.QIntelligents[index]

    def exec(self):
        current = 0
        while True:
            board = self.make_choice(self.ai(current).choice(), current)
            if board:
                current = 1 - current
            else:
                self.ai(0).reward(1)
                self.Frame.broad.restart()

shell = Shell()

shell.exec_()
