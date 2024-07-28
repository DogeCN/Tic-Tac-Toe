from PySide6.QtWidgets import QMainWindow, QMenu
from PySide6.QtGui import QIcon, QAction, QActionGroup
from PySide6.QtCore import Qt, Signal
from settings import Setting
from ui import res


class MainWindow(QMainWindow):
    psignal = Signal()
    nsignal = Signal()
    new = Signal()
    server = Signal()
    client = Signal()

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
        self.modea = QActionGroup(self)
        for i in range(len(contexts)):
            action = QAction(contexts[i], self)
            action.setCheckable(True)
            if i == Setting.mode:
                action.setChecked(True)
            action.toggled.connect(lambda *e, i=i: setattr(Setting, 'mode', i))
            self.modea.addAction(action)
        self.menu.addActions(self.modea.actions())

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

        self.online = QActionGroup(self)

        server = QAction('Start a Server', self)
        server.triggered.connect(self.server)
        self.online.addAction(server)
        self.menu.addAction(server)

        client = QAction('Connect to a Server', self)
        client.triggered.connect(self.client)
        self.online.addAction(client)
        self.menu.addAction(client)

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

        if Setting.mode != 2:
            self.online.setEnabled(False)

        self.menu.popup(pos)
