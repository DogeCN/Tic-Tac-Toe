from PySide6.QtWidgets import QMainWindow, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, Signal
from settings import Setting
from ui import res


class MainWindow(QMainWindow):
    psignal = Signal()
    nsignal = Signal()
    new = Signal()

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
    
    def contextMenuEvent(self, event):
        pos = event.globalPos()

        menu = QMenu(self)
 
        modes = QMenu('Mode', self)

        contexts = ['First Hand', 'Last Hand', 'Multiplayer', 'Auto Play']
        for i in range(len(contexts)):
            action = QAction(contexts[i], self)
            action.setCheckable(True)
            if i == Setting.mode:
                action.setChecked(True)
            action.toggled.connect(lambda *e, i=i: self.setMode(i))
            modes.addAction(action)

        menu.addMenu(modes)
        
        new = QAction('New', self)
        new.triggered.connect(self.new)
        menu.addAction(new)

        quit = QAction('Quit', self)
        quit.triggered.connect(self.close)
        menu.addAction(quit)

        menu.closeEvent = lambda *e: self.update()
        menu.popup(pos)

    def setMode(self, mode:int):
        Setting.mode = mode
