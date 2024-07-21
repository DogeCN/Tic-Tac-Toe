from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from board import Board

App = QApplication()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        board = Board(self)

        central_widget.setLayout(board.grid)

Frame = MainWindow()
Frame.show()

App.exec()
