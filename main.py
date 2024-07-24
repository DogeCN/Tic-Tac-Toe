from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from game.board import Board
from q import QLearning

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(100, 100, 400, 400)
        Center = QWidget(self)
        self.setCentralWidget(Center)

        self.board = Board(Center, QLearning(self))
    
    def choose(self, index:int):
        self.board.buttons[index].animateClick()

    def get_board(self):
        board = [0 for _ in range(9)]
        players = self.board.group.players
        for i in range(2):
            for button in players[i].queue:
                sign = button.sign
                board[button.row * 3 + button.column] = sign if i else 256-sign
        return board

if __name__ == '__main__':
    App = QApplication()
    Frame = MainWindow()
    Frame.show()
    App.exec()
