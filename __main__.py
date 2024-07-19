from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget

App = QApplication()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(100, 100, 400, 400)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a grid layout
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        # Create and add buttons to the grid layout
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = QPushButton("")
                button.setFixedSize(100, 100)
                button.setFlat(True)
                button.setStyleSheet("font-size: 40px;")
                grid_layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

Frame = MainWindow()
Frame.show()

App.exec()
