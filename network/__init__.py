from PySide6.QtWidgets import QInputDialog, QMessageBox
from PySide6.QtCore import QObject, Signal
from settings import Setting
from threading import Thread
from socket import socket

class NetWork(QObject):
    received = Signal(list)
    connected = Signal(int)
    warning = Signal(str)
    conn = None #type: socket
    onconn = False

    def __init__(self, frame):
        super().__init__(frame)
        self.frame = frame
        self.warning.connect(self.warn)
        self.start_server()

    def start_server(self):
        try:
            self.server = socket()
            self.server.bind(('127.0.0.1', 25565))
            Thread(target=self.listenloop, daemon=True).start()
        except OSError:
            if not self.onconn and not Setting.online:
                self.warn('Port 25565 in use')

    def listenloop(self):
        while True:
            try:
                self.server.listen(1)
                self.conn, _ = self.server.accept()
                self.connected.emit(0)
                self.onconn = True
                self.recvloop()
            except OSError:
                if self.onconn:
                    self.start_server()
                    self.onconn = False
                break

    def start_client(self):
        if self.onconn:
            self.onconn = False
            self.conn.close()
            self.start_server()
        else:
            address, choice = QInputDialog.getText(self.frame, 'Connect to a Server', 'Entry the address')
            if choice:
                if address:
                    address = address.split(":")
                    host = ''.join(address[:-1])
                    port = int(address[-1])
                else:
                    host = '127.0.0.1'
                    port = 25565
                self.server.close()
                client = socket()
                try:
                    client.connect((host, port))
                except OSError:
                    self.warn('Connection Refused')
                    return
                self.onconn = True
                self.conn = client
                self.connected.emit(1)
                Thread(target=self.recvloop, daemon=True).start()
            
    def send(self, msg):
        data = repr(msg).encode()
        try:
            if self.conn:
                self.conn.send(data)
        except OSError:
            self.close_conn()

    def recvloop(self):
        while True:
            try:
                data = self.conn.recv(1024)
                if data:
                    msg = eval(data)
                    self.received.emit(msg)
            except OSError:
                self.close_conn()
                break

    def close_conn(self):
        if self.onconn:
            self.onconn = False
            self.conn.close()
            self.warning.emit('Connection Lost')
        self.connected.emit(0)

    def warn(self, msg:str):
        QMessageBox.warning(self.frame, 'Warning', msg)
        if Setting.online:
            self.received.emit([[],[]])
            Setting.online = False
