from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from PySide6.QtCore import Qt
from sprites.button import Button, Wrapper
from sprites.player import Player
from settings import Setting
from ui.main import MainWindow
from ui.skin import default
from random import choice

class Board:
    gaming = True
    board = [[None for _ in range(3)] for _ in range(3)] #type: list[list[Button]]

    def __init__(self):
        self.ai = Intelligence(self)
        self.steps = Steps(self)
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
        frame.psignal.connect(self.steps.pre)
        frame.nsignal.connect(self.steps.next)
        frame.new.connect(self.restart)
        frame.show()
        if Setting.mode % 2:
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
            self.steps.record()
            if self.judge():
                return
            index = default._index
            if index != Setting.mode and Setting.mode != 2:
                self.ai.choose(index)
        else:
            self.restart()

    def judge(self):
        for player in default.players:
            if sorted(player.queue, key=lambda b:(b.row, b.column)) in self.probables:
                self.gaming = False
                winner = default.player(player.index)
                default._index = 0
                for button in winner.queue:
                    button.setFlat(False)
                    button.sign = 3
                    super(Player, winner).apply(button)
                if Setting.mode == 3:
                    self.restart()
                return True
        return False

    def restart(self):
        self.steps.rec_empty()
        self.gaming = True
        for button in self.buttons:
            button.setFlat(True)
            Wrapper.clear(button)
        for player in default.players:
            player.queue.clear()
        default._index = 0
        if Setting.mode % 2:
            self.ai.choose(0)

class Steps(list[list[list[tuple[int]]]]):
    pointer = -1

    def __init__(self, board:Board):
        self.board = board
        self.rec_empty()

    @property
    def current(self):
        return self[self.pointer]

    def record(self):
        behind = len(self) - self.pointer - 1
        if behind:
            for _ in range(behind):
                self.pop()
        group = []
        for player in default.players:
            queue = []
            for button in player.queue:
                queue.insert(0, (button.row, button.column))
            group.append(queue)
        super().append(group)
        self.pointer += 1

    def rec_empty(self):
        super().append([])
        self.pointer += 1

    def occurent(self):
        index = default._index
        for button in self.board.buttons:
            Wrapper.clear(button)
            button.setFlat(True)
        for i in range(2):
            default.player(i).queue.clear()
        if self.current:
            for i in range(2):
                queue = self.current[i]
                for pos in queue:
                    default._index = i
                    default.apply(self.board.get(*pos))
        else:
            index = 0
        default._index = index

    def pre(self):
        if self.pointer > 0:
            default.index
            self.board.gaming = True
            self.pointer -= 1
            self.occurent()
            self.board.judge()

    def next(self):
        if self.pointer < len(self) - 1:
            default.index
            self.board.gaming = True
            self.pointer += 1
            self.occurent()
            self.board.judge()

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
            result = self.choice_infront(myqueue[:2])
        if not result and oplen > 1:
            result = self.choice_infront(opqueue[:2])
        if not result and oplen > 2:
            result = self.choice_infront([opqueue[-1], myqueue[0]])
        if not result and mylen > 2:
            result = self.choice_infront([myqueue[1], opqueue[0]])
        if not result and oplen > 2:
            result = self.choice_probables(opqueue[1])
        if not result:
            mypro = oppro = set()
            if myqueue:
                mypro = self.find_probables(myqueue[0])
            elif opqueue:
                oppro = self.find_probables(opqueue[0]) 
            same = mypro.intersection(oppro)
            if same:
                result = self.choice_one(same)
            else:
                if mypro:
                    result = self.choice_one(mypro)
                elif oppro:
                    result = self.choice_one(oppro)
                else:
                    result = self.choice_one(self.empty)
        return result

    def choice_one(self, buttons:list[Button]):
        return choice(list(buttons))

    def choice_infront(self, queue:list[Button]):
        front = set(queue)
        for p in self.probables:
            pro = set(p)
            if front.issubset(pro):
                result = (pro-front).pop()
                if result.sign:
                    continue
                return result
                        
    def choice_probables(self, button:Button):
        return self.choice_one(self.find_probables(button))

    def find_probables(self, button:Button):
        prolist = set()
        bset = {button}
        for p in self.probables:
            pset = set(p)
            if bset.issubset(pset):
                for button in pset-bset:
                    if not button.sign:
                        prolist.add(button)
        return prolist

Board()
