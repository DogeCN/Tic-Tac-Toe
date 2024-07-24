from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Signal
from game.board import Board
from q import QLearning

class MainWindow(QMainWindow):
    choose = Signal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(100, 100, 400, 400)
        Center = QWidget(self)
        self.setCentralWidget(Center)

        self.board = Board(Center, QLearning(self))
        self.board.model.choice()

        self.choose.connect(self.choose_)
    
    def choose_(self, index:int):
        self.board.buttons[index].animateClick()

    def get_board(self):
        board = [0 for _ in range(9)]
        for player in self.board.group.players:
            for button in player.queue:
                sign = button.sign
                board[button.row * 3 + button.column] = sign
        return bytes(board)

if __name__ == '__main__':
    App = QApplication()
    Frame = MainWindow()
    Frame.show()
    App.exec()
