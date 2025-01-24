from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from PySide6.QtCore import Qt
from sprites.button import Button
from sprites.player import Player
from settings import Setting
from network import NetWork
from ui.main import MainWindow
from ui.skin import default
from random import choice


class Board:
    gaming = True
    board = [[None for _ in range(3)] for _ in range(3)]  # type: list[list[Button]]

    def __init__(self):
        app = QApplication()
        self.ai = Intelligence(self)
        self.steps = Steps(self)
        self.build_frame()
        if Setting.online:
            Setting.online = False
        self.net = NetWork(self.frame)
        self.connect_actions()
        if Setting.ast(2):
            self.ai.choose(0)
        app.exec()

    def build_frame(self):
        self.frame = MainWindow()
        center = QWidget(self.frame)
        self.frame.setCentralWidget(center)
        grid = QGridLayout(center)
        for row in range(3):
            for column in range(3):
                button = Button(self.frame, row, column)
                self.board[row][column] = button
                button.clicked.connect(lambda *x, b=button: self.emit(b))
                button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                grid.addWidget(button, row, column)
        self.frame.show()

    def connect_actions(self):
        self.frame.send.connect(self.net.send)
        self.frame.psignal.connect(self.steps.pre)
        self.frame.nsignal.connect(self.steps.next)
        self.frame.new.connect(self.restart)
        self.frame.client.connect(self.net.start_client)
        self.net.received.connect(self.receive)
        self.net.connected.connect(self.online)

    def online(self, index: int):
        if Setting.online:
            Setting.online = False
        else:
            Setting.online = True
        default._index = index
        for button in self.buttons:
            button.setEnabled(not bool(index))
            button.setFlat(True)
        self.gaming = True
        for player in default.players:
            player.queue.clear()

    def receive(self, group: list):
        self.steps.record(group)
        self.steps.occurent()
        if group:
            enable = True
        else:
            enable = False
            default._index = 1
        for button in self.buttons:
            button.setEnabled(enable)

    def get(self, row: int, column: int):
        return self.board[row][column]

    def row(self, row: int):
        return self.board[row]

    @property
    def rows(self):
        return self.board

    def column(self, column: int):
        return [self.get(row, column) for row in range(3)]

    @property
    def columns(self):
        return [self.column(i) for i in range(3)]

    def diagonal(self, diagonal: int | bool):
        return (
            [self.get(i, 2 - i) for i in range(3)]
            if diagonal
            else [self.get(i, i) for i in range(3)]
        )

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

    def emit(self, button: Button):
        if self.gaming:
            if button in default.queue:
                return
            default.apply(button)
            group = self.steps.record()
            if Setting.online:
                self.net.send(group)
                default.index
                for button in self.buttons:
                    button.setEnabled(False)
            if self.judge():
                return
            index = default._index
            if Setting.ast(index):
                self.ai.choose(index)
        else:
            self.restart()

    def judge(self):
        for player in default.players:
            if sorted(player.queue, key=lambda b: (b.row, b.column)) in self.probables:
                self.gaming = False
                winner = default.player(player.index)
                for button in winner.queue:
                    button.setFlat(False)
                    button.sign = 3
                    super(Player, winner).apply(button)
                if Setting.ast(3):
                    self.restart()
                elif Setting.online:
                    for button in self.buttons:
                        button.setEnabled(True)
                return True
        return False

    def restart(self):
        self.steps.record([])
        self.gaming = True
        for button in self.buttons:
            button.setFlat(True)
        for player in default.players:
            player.queue.clear()
        if Setting.online:
            self.net.send([])
        default._index = 0
        if Setting.ast(2):
            self.ai.choose(0)


class Steps(list[list[list[tuple[int]]]]):
    pointer = -1

    def __init__(self, board: Board):
        self.board = board
        self.record([])

    @property
    def current(self):
        return self[self.pointer]

    def record(self, group: list[list[tuple[int]]] | None = None):
        if group is None:
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
        return group

    def occurent(self, group: list[list[tuple[int]]] | None = None):
        self.board.gaming = True
        index = default._index
        for button in self.board.buttons:
            button.setFlat(True)
        for i in range(2):
            default.player(i).queue.clear()
        group = self.current if group is None else group
        if group:
            for i in range(2):
                queue = group[i]
                for pos in queue:
                    default._index = i
                    default.apply(self.board.get(*pos))
        else:
            index = 0
        default._index = index
        self.board.judge()

    def pre(self):
        if self.pointer > 0:
            default.index
            self.pointer -= 1
            self.occurent()

    def next(self):
        if self.pointer < len(self) - 1:
            default.index
            self.pointer += 1
            self.occurent()


class Intelligence:

    def __init__(self, board: Board):
        self.board = board

    @property
    def probables(self):
        return self.board.probables

    @property
    def empty(self):
        return [b for b in self.board.buttons if not b.sign]

    @property
    def corner(self):
        return {self.board.get(r, c) for r in [0, 2] for c in [0, 2]}

    def choose(self, index: int):
        self.choice(index).animateClick()

    def choice(self, index: int) -> Button:
        result = None
        myqueue = default.player(index).queue
        opqueue = default.player(1 - index).queue
        mylen, oplen = len(myqueue), len(opqueue)
        print(mylen, oplen)
        if mylen > 1:
            result = self.choice_infront(myqueue[:2])
        if not result and oplen > 1:
            result = self.choice_infront(opqueue[:2])
        if not result and oplen > 2:
            result = self.choice_infront([opqueue[-1], myqueue[0]])
        if not result and mylen > 1:
            result = self.choice_infront([myqueue[1], opqueue[0]])
        if not result and oplen > 2:
            prolist = self.find_probables(opqueue[1])
            if prolist:
                result = self.choice_one(prolist)
        if not result:
            mypro = oppro = set()
            if myqueue:
                mypro = self.find_probables(myqueue[0])
            elif opqueue:
                oppro = self.find_probables(opqueue[0])
            same = mypro.intersection(oppro)
            if index:
                match oplen:
                    case 1:
                        op = opqueue[0]
                        row = op.row
                        col = op.column
                        if row == col == 1:
                            result = self.choice_one(self.corner)
                        elif op in self.corner:
                            result = self.board.get(1, 1)
                        else:
                            result = self.choice_one(self.corner.difference(oppro))
            else:
                match oplen:
                    case 0:
                        result = self.choice_one(self.empty)
            if not result:
                if same:
                    result = self.choice_one(same)
                elif mypro:
                    result = self.choice_one(mypro)
                elif oppro:
                    result = self.choice_one(oppro)
        return result

    def choice_one(self, buttons: list[Button]):
        return choice(list(buttons))

    def choice_infront(self, queue: list[Button]):
        front = set(queue)
        for p in self.probables:
            pro = set(p)
            if front.issubset(pro):
                result = (pro - front).pop()
                if result.sign:
                    continue
                return result

    def find_probables(self, button: Button):
        prolist = set()
        bset = {button}
        for p in self.probables:
            pset = set(p)
            if bset.issubset(pset):
                for button in pset - bset:
                    if not button.sign:
                        prolist.add(button)
                    else:
                        break
        return prolist


Board()
