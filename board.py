from PySide6.QtWidgets import QGridLayout
from typing import overload
from warpper import Button

class Board:
    broad = [[None for _ in range(3)] for _ in range(3)] #type: list[list[Button]]

    def __init__(self, parent):
        grid = QGridLayout(parent)
        for row in range(3):
            for column in range(3):
                button = Button(parent, row, column)
                self.broad[row][column] = button
                button.clicked.connect(lambda *x, b=button: self.emit(b))
                grid.addWidget(button, row, column)

    def get(self, row:int, column:int):
        return self.broad[row][column]

    def row(self, row:int):
        return self.broad[row]

    def column(self, column:int):
        return [self.get(row, column) for row in range(3)]

    def diagonal(self, diagonal:int):
        return [self.get(i, 2 - i) for i in range(3)] if diagonal else [self.get(i, i) for i in range(3)]

    @property
    def buttons(self):
        for r in range(3):
            for b in self.row(r):
                yield b

    @overload
    def emit(self, row:int, column:int):
        button = self.get(row, column)
        self.emit(button)

    def emit(self, button:Button):
        button.react()
