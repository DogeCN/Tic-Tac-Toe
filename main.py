from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from game.board import Board

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(100, 100, 400, 400)

        Center = QWidget(self)
        self.setCentralWidget(Center)

        self.broad = Board(Center)

if __name__ == '__main__':
    Frame = MainWindow()
    App = QApplication()
    Frame.show()
    App.exec()
