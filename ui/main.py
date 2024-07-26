from ui import res


from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    psignal = Signal()
    nsignal = Signal()

    def __init__(self):
        super().__init__()
        res.Reg()
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(100, 100, 400, 400)
        self.setFixedSize(400, 400)
        self.setWindowIcon(QIcon(':/img/favicon.ico'))

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Left or key == Qt.Key.Key_Up:
            self.psignal.emit()
        elif key == Qt.Key.Key_Right or key == Qt.Key.Key_Down:
            self.nsignal.emit()

    def wheelEvent(self, event):
            angle = event.angleDelta()
            angleY = angle.y()
            if angleY > 0:
                self.psignal.emit()
            else:
                self.nsignal.emit()