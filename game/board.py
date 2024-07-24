from PySide6.QtWidgets import QGridLayout
from skins.default import default
from game.button import Button, Wrapper
from game.player import Player

class Board:
    gaming = True
    group = default
    broad = [[None for _ in range(3)] for _ in range(3)] #type: list[list[Button]]

    def __init__(self, parent):
        grid = QGridLayout(parent)
        for row in range(3):
            for column in range(3):
                button = Button(parent, row, column)
                self.broad[row][column] = button
                button.clicked.connect(lambda *x, b=button: self.emit(b))
                grid.addWidget(button, row, column)

    def restart(self):
        self.gaming = True
        for button in self.buttons:
            button.setFlat(True)
            Wrapper.clear(button)
        for player in self.group.players:
            player.queue.clear()

    def get(self, row:int, column:int):
        return self.broad[row][column]

    def row(self, row:int):
        return self.broad[row]

    def column(self, column:int):
        return [self.row(row)[column] for row in range(3)]

    def diagonal(self, diagonal:int|bool):
        return [self.get(i, 2 - i) for i in range(3)] if diagonal else [self.get(i, i) for i in range(3)]

    @property
    def buttons(self) -> list[Button]:
        buttons = []
        for r in range(3):
            for b in self.row(r):
                buttons.append(b)
        return buttons

    def emit(self, button:Button):
        if self.gaming:
            self.group.apply(button)
            for i in range(3):
                rowj = self.judge(self.row(i))
                if rowj != -1:
                    self.win(rowj)
                    break
                colj = self.judge(self.column(i))
                if colj != -1:
                    self.win(colj)
                    break
                diaj = self.judge(self.diagonal(bool(i)))
                if diaj != -1:
                    self.win(diaj)
                    break
        else:
            self.restart()

    def judge(self, buttons:list[Button]):
        for player in self.group.players:
            queue = player.queue
            if set(queue).issuperset(set(buttons)):
                return player.index
        return -1
    
    def win(self, index:int):
        self.gaming = False
        winner = self.group.player(index)
        for button in winner.queue:
            button.opacity = 255
            button.setFlat(False)
            super(Player, winner).apply(button)
