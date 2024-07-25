from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QPushButton
from random import choice

class Button(QPushButton):
    style_sheet = ''
    color = (255, 255, 255)
    opacity = 0

    def __init__(self, parent, row, column):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setFlat(True)
        self.row = row
        self.column = column

    @property
    def sign(self):
        return self.opacity*3 // 255
    
    @sign.setter
    def sign(self, sign:int):
        self.opacity = sign*255 // 3
        self.style_update()

    def style_update(self):
        color = f'color: rgba{(*self.color, self.opacity)};'
        self.setStyleSheet(self.style_sheet + color)

class ButtonQueue(list[Button]):
    def __init__(self):
        super().__init__()
    
    def append(self, button:Button):
        super().insert(0, button)
        for i in range(len(self)):
            button = self[i]
            sign = 3 - i
            if not sign:
                Wrapper.clear(self.pop())
            else:
                button.sign = sign

class Wrapper:
    text = ''
    style = 'font-size: 40px;'
    color = (255, 255, 255)

    def apply(self, button:Button):
        button.setText(self.text)
        button.color = self.color
        button.style_sheet = self.style
        button.style_update()
    
    @staticmethod
    def clear(button:Button):
        Wrapper().apply(button)
        button.sign = 0

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



default = PlayerGroup()

player1 = default.player(0)
player1.text = '〇'
player1.style = 'font: 700 60px;'
player1.color = (0, 255, 0)

player2 = default.player(1)
player2.text = '⨯'
player2.style = 'font-size: 80px;'
player2.color = (255, 0, 0)



class Board:
    gaming = True
    broad = [[None for _ in range(3)] for _ in range(3)] #type: list[list[Button]]

    def __init__(self):
        app = QApplication()
        frame = QMainWindow()
        frame.setWindowTitle('Tic Tac Toe')
        frame.setGeometry(100, 100, 400, 400)
        center = QWidget(frame)
        frame.setCentralWidget(center)
        grid = QGridLayout(center)
        for row in range(3):
            for column in range(3):
                button = Button(frame, row, column)
                self.broad[row][column] = button
                button.clicked.connect(lambda *x, b=button: self.emit(b))
                grid.addWidget(button, row, column)
        frame.show()
        app.exec()

    def restart(self):
        self.gaming = True
        for button in self.buttons:
            button.setFlat(True)
            Wrapper.clear(button)
        for player in default.players:
            player.queue.clear()
        default._index = 0

    def get(self, row:int, column:int):
        return self.broad[row][column]

    def row(self, row:int):
        return self.broad[row]

    @property
    def rows(self):
        return self.broad

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
    def empty(self):
        return [b for b in self.buttons if not b.sign]

    @property
    def buttons(self) -> list[Button]:
        buttons = []
        for r in range(3):
            for b in self.row(r):
                buttons.append(b)
        return buttons

    def emit(self, button:Button):
        if self.gaming:
            if button in default.queue:
                return
            default.apply(button)
            if self.judge():
                return
            if default._index:
                self.choose().animateClick()
        else:
            self.restart()

    def choose(self) -> Button:
        queue = default.player(0).queue
        match len(queue):
            case 2|3:
                for p in self.probables:
                    fount = {b for b in queue if b.sign > 1}
                    pro = set(p)
                    if fount.issubset(pro):
                        result = (pro-fount).pop()
                        if result.sign:
                            continue
                        return result
            case 1:
                probables = set()
                bset = set(queue)
                for p in self.probables:
                    pset = set(p)
                    if bset.issubset(pset):
                        probables.update(pset-bset)
                return choice(list(probables))
        return choice(self.empty)

    def judge(self):
        for player in default.players:
            if sorted(player.queue, key=lambda b:(b.row, b.column)) in self.probables:
                self.gaming = False
                winner = default.player(player.index)
                for button in winner.queue:
                    button.setFlat(False)
                    button.sign = 3
                    super(Player, winner).apply(button)
                return True
        return False

Board()