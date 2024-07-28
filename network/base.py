from PySide6.QtCore import QObject, Signal
from socket import socket
from threading import Thread


class SockBase(QObject):
    received = Signal(tuple)
    conn = None #type: socket

    def __init__(self):
        super().__init__()
        self.socket = socket()
        self.recvloop = Thread(target=self.recv, daemon=True)
        self.recvloop.start()

    def send(self, msg):
        data = bytes(msg)
        try:
            if self.conn:
                self.conn.send(data)
        except OSError as e:
            self.close(e)

    def recv(self):
        while True:
            try:
                if self.conn:
                    data = self.conn.recv(1024)
                    self.received.emit(tuple(data))
            except OSError as e:
                self.close(e)

    def close(self, exception=None):
        if exception:
            print(exception)
        self.conn.close()
        try:
            self.socket.close()
        except: ...


class Client(SockBase):

    def connect_(self, address:str):
        address = address.split(":")
        host = ''.join(address[:-1])
        port = int(address[-1])
        self.socket.connect((host, port))
        self.conn = self.socket

class Server(SockBase):

    def __init__(self):
        super().__init__()
        self.socket.bind(('127.0.0.1', 25565))
        self.connthread = Thread(target=self.connect_, daemon=True)
        self.connthread.start()

    def connect_(self):
        self.socket.listen(1)
        self.conn, _ = self.socket.accept()
