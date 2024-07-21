from PySide6.QtWidgets import QPushButton, QGridLayout

class Button(QPushButton):
    def __init__(self, parent, row, column):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setFlat(True)
        self.setStyleSheet('font-size: 40px;')
        self.row = row
        self.column = column
        self.clicked.connect(self.react)
    
    def react(self):
        print('Clicked Button:', self.row, self.column)

class Board:
    broad = [[None for _ in range(3)] for _ in range(3)] #type: list[list[Button]]

    def __init__(self, parent):
        self.grid = QGridLayout(parent)
        for row in range(3):
            for column in range(3):
                button = Button(parent, row, column)
                self.broad[row][column] = button
                self.grid.addWidget(button, row, column)

    def row(self, row:int) -> list[Button]:
        return self.broad[row]

    def column(self, column:int) -> list[Button]:
        return [self.broad[row][column] for row in range(3)]

    def diagonal(self, diagonal:int) -> list[Button]:
        return [self.broad[i][2 - i] for i in range(3)] if diagonal else [self.broad[i][i] for i in range(3)]
