from PySide6.QtWidgets import QMainWindow, QMenu
from PySide6.QtGui import QIcon, QAction, QActionGroup
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
        self.initMenu()
    
    def initMenu(self):
        self.menu = QMenu(self)

        contexts = ['First Hand', 'Last Hand', 'Multiplayer', 'Auto Play']
        actions = QActionGroup(self)
        for i in range(len(contexts)):
            action = QAction(contexts[i], self)
            action.setCheckable(True)
            if i == Setting.mode:
                action.setChecked(True)
            action.toggled.connect(lambda *e, i=i: setattr(Setting, 'mode', i))
            actions.addAction(action)
        self.menu.addActions(actions.actions())

        self.menu.addSeparator()
        
        pre = QAction('Previous Step', self)
        pre.setShortcut(Qt.Key.Key_Left)
        pre.triggered.connect(self.psignal)
        self.menu.addAction(pre)

        next = QAction('Next Step', self)
        next.setShortcut(Qt.Key.Key_Right)
        next.triggered.connect(self.nsignal)
        self.menu.addAction(next)

        new = QAction('New', self)
        new.triggered.connect(self.new)
        self.menu.addAction(new)

        self.menu.addSeparator()

        quit = QAction('Quit', self)
        quit.triggered.connect(self.close)
        self.menu.addAction(quit)

        self.menu.closeEvent = lambda *e: self.update()

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
        self.menu.popup(pos)
