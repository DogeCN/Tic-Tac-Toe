from PySide6.QtWidgets import QMainWindow, QMenu, QInputDialog
from PySide6.QtGui import QIcon, QAction, QActionGroup
from PySide6.QtCore import Qt, Signal
from settings import Setting
from ui import res


class MainWindow(QMainWindow):
    send = Signal(str)
    psignal = Signal()
    nsignal = Signal()
    new = Signal()
    client = Signal()

    def __init__(self):
        super().__init__()
        res.Reg()
        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(100, 100, 400, 400)
        self.setFixedSize(400, 400)
        self.setWindowIcon(QIcon(":/img/favicon.ico"))
        self.initMenu()

    def initMenu(self):
        self.menu = QMenu(self)

        contexts = ["First Hand", "Last Hand", "Multiplayer", "Auto Play"]
        self.modea = QActionGroup(self)
        for i in range(len(contexts)):
            action = QAction(contexts[i], self)
            action.setCheckable(True)
            if i == Setting.mode:
                action.setChecked(True)
            action.toggled.connect(lambda *e, i=i: setattr(Setting, "mode", i))
            self.modea.addAction(action)
        self.menu.addActions(self.modea.actions())

        self.menu.addSeparator()

        self.control = QActionGroup(self)

        pre = QAction("Previous Step", self)
        pre.setShortcut(Qt.Key.Key_Left)
        pre.triggered.connect(self.psignal)
        self.control.addAction(pre)
        self.menu.addAction(pre)

        next = QAction("Next Step", self)
        next.setShortcut(Qt.Key.Key_Right)
        next.triggered.connect(self.nsignal)
        self.control.addAction(next)
        self.menu.addAction(next)

        new = QAction("New", self)
        new.triggered.connect(self.new)
        self.control.addAction(new)
        self.menu.addAction(new)

        self.menu.addSeparator()

        self.client_ = QAction("Connect to a Server", self)
        self.client_.triggered.connect(self.client)
        self.menu.addAction(self.client_)

        self.send_ = QAction("Send", self)
        self.send_.setShortcut(Qt.Key.Key_Return | Qt.Key.Key_Enter)
        self.send_.triggered.connect(self.send_msg)
        self.menu.addAction(self.send_)

        self.menu.addSeparator()

        quit = QAction("Quit", self)
        quit.setShortcut(Qt.Key.Key_Escape)
        quit.triggered.connect(self.close)
        self.menu.addAction(quit)

        self.menu.closeEvent = lambda *e: self.update()

    def send_msg(self):
        msg, choice = QInputDialog.getText(self, "Send", "Entry the message")
        if choice and msg:
            self.send.emit(msg)

    def keyPressEvent(self, event):
        key = event.key()
        if Setting.online:
            if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
                self.send_msg()
            elif key == Qt.Key.Key_Control | Qt.Key.Key_Q:
                self.client.emit()
        else:
            if key == Qt.Key.Key_Escape:
                self.close()
            elif key == Qt.Key.Key_Left or key == Qt.Key.Key_Up:
                self.psignal.emit()
            elif key == Qt.Key.Key_Right or key == Qt.Key.Key_Down:
                self.nsignal.emit()

    def wheelEvent(self, event):
        if not Setting.online:
            angle = event.angleDelta()
            angleY = angle.y()
            if angleY > 0:
                self.psignal.emit()
            else:
                self.nsignal.emit()

    def contextMenuEvent(self, event):
        pos = event.globalPos()

        if Setting.online:
            self.modea.setEnabled(False)
            self.control.setEnabled(False)
            self.client_.setText("Disconnect")
            self.send_.setEnabled(True)
        else:
            self.modea.setEnabled(True)
            self.control.setEnabled(True)
            self.client_.setText("Connect to a Server")
            self.send_.setEnabled(False)

        self.menu.popup(pos)
