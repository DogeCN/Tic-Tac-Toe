from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from sprites.button import Button, Wrapper
from sprites.player import Player
from config import get_mode
from ui.skin import default
from random import choice
from ui import res

class MainWindow(QMainWindow):
    psignal = Signal()
    nsignal = Signal()

    def __init__(self):
        super().__init__()
        res.Reg()
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(100, 100, 400, 400)
        self.setFixedSize(400, 400)
        self.setWindowIcon(QIcon(':/img/favicon.ico'))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.psignal.emit()
        elif event.key() == Qt.Key.Key_Right:
            self.nsignal.emit()

class Step(list[Button]):
    pointer = -1

    def __init__(self, board):
        self.board = board #type: Board

    def append(self, button:Button):
        super().append(button)
        self.pointer += 1

    def clear(self):
        super().clear()
        self.pointer = 0

    def pre(self):
        if self.pointer >= 0:
            Wrapper.clear(self[self.pointer])
            self.board.gaming = True
            pointer = self.pointer
            length = 6 if len(self) >= 6 else len(self)
            for button in self[pointer-length+1:pointer]:
                button.setFlat(False)
                button.sign += 1
            ...
            self.pointer -= 1
    
    def next(self):
        if self.pointer < len(self):
            self.pointer += 1
            button = self[self.pointer]
            default.apply(button)
            self.board.judge()
            return button


class Board:
    gaming = True
    board = [[None for _ in range(3)] for _ in range(3)] #type: list[list[Button]]

    def __init__(self):
        self.mode = get_mode()
        self.ai = Intelligence(self)
        self.step = Step(self)
        app = QApplication()
        frame = MainWindow()
        center = QWidget(frame)
        frame.setCentralWidget(center)
        grid = QGridLayout(center)
        for row in range(3):
            for column in range(3):
                button = Button(frame, row, column)
                self.board[row][column] = button
                button.clicked.connect(lambda *x, b=button: self.emit(b))
                button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                grid.addWidget(button, row, column)
        frame.psignal.connect(self.step.pre)
        frame.nsignal.connect(self.step.next)
        frame.show()
        if self.mode % 2:
            self.ai.choose(0)
        app.exec()

    def get(self, row:int, column:int):
        return self.board[row][column]

    def row(self, row:int):
        return self.board[row]

    @property
    def rows(self):
        return self.board

    def column(self, column:int):
        return [self.get(row, column) for row in range(3)]

    @property
    def columns(self):
        return [self.column(i) for i in range(3)]

    def diagonal(self, diagonal:int|bool):
        return [self.get(i, 2 - i) for i in range(3)] if diagonal else [self.get(i, i) for i in range(3)]

    @property
    def diagonals(self):
        return [self.diagonal(0), self.diagonal(1)]

    @property
    def probables(self):
        return self.rows + self.columns + self.diagonals

    @property
    def buttons(self) -> list[Button]:
        buttons = []
        for r in self.board:
            buttons += r
        return buttons

    def emit(self, button:Button):
        if self.gaming:
            if button in default.queue:
                return
            default.apply(button)
            if self.judge():
                return
            index = default._index
            self.step.append(button)
            if index != self.mode and self.mode != 2:
                self.ai.choose(index)
        else:
            self.step.clear()
            self.restart()

    def judge(self):
        for player in default.players:
            if sorted(player.queue, key=lambda b:(b.row, b.column)) in self.probables:
                self.gaming = False
                winner = default.player(player.index)
                for button in winner.queue:
                    button.setFlat(False)
                    button.sign = 3
                    super(Player, winner).apply(button)
                if self.mode == 3:
                    self.restart()
                return True
        return False

    def restart(self):
        self.gaming = True
        for button in self.buttons:
            button.setFlat(True)
            Wrapper.clear(button)
        for player in default.players:
            player.queue.clear()
        default._index = 0
        if self.mode % 2:
            self.ai.choose(0)

class Intelligence:

    def __init__(self, board:Board):
        self.board = board

    @property
    def probables(self):
        return self.board.probables

    @property
    def empty(self):
        return [b for b in self.board.buttons if not b.sign]

    def choose(self, index:int):
        self.choice(index).animateClick()

    def choice(self, index:int) -> Button:
        result = None
        myqueue = default.player(index).queue
        opqueue = default.player(1-index).queue
        mylen, oplen = len(myqueue), len(opqueue)
        if mylen > 1:
            result = self.choice_infront(myqueue)
        if not result and oplen > 1:
            result = self.choice_infront(opqueue)
        if not result and mylen > 2:
            result = self.choice_infront([myqueue[1], opqueue[0]])
        if not result and oplen > 2:
            result = self.choice_infront([opqueue[1], myqueue[0]])
        if not result:
            prolist = []
            if myqueue:
                prolist += self.find_probables(myqueue[0])
            if oplen > 2:
                prolist += self.find_probables(opqueue[1])
            elif opqueue:
                prolist += self.find_probables(opqueue[0])
            if prolist:
                result = choice(prolist)
            else:
                result = choice(self.empty)
        return result

    def choice_infront(self, queue:list[Button]):
        for p in self.probables:
            front = {b for b in queue if b.sign > 1}
            pro = set(p)
            if front.issubset(pro):
                result = (pro-front).pop()
                if result.sign:
                    continue
                return result
                        
    def choice_probables(self, button:Button):
        return choice(self.find_probables(button))

    def find_probables(self, button:Button):
        prolist = []
        bset = {button}
        for p in self.probables:
            pset = set(p)
            if bset.issubset(pset):
                for button in pset-bset:
                    if not button.sign:
                        prolist.append(button)
        return prolist

Board()
