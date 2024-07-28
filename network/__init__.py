from PySide6.QtWidgets import QMessageBox, QInputDialog
from .base import Client, Server

class NetWork:
    socket = None

    def __init__(self, signal):
        self.received = signal

    def server(self, frame):
        self.socket = Server()
        self.socket.received.connect(self.received)
        QMessageBox.information(frame, 'Server Started', 'Port: 25565')

    def client(self, frame):
        address, choice = QInputDialog.getText(frame, 'Connect to a Server', 'Entry the address')
        if choice and address:
            self.socket = Client()
            self.socket.received.connect(self.received)
            self.socket.connect_(address)

    def send(self, *msg):
        if self.socket.conn:
            self.socket.send(msg)

    def close(self):
        if self.socket.conn:
            self.socket.close()
