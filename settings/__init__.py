from .iobase import load, dump
import os

data = os.getenv('AppData') + os.sep + 'Tic-Tac-Toe'

ast = [
    [False, True, False, False],
    [True, False, True, False],
    [False, False, False, False],
    [True, True, True, True],
]

class Settings:
    def __init__(self, file):
        try:
            self.__dict__ = load(file).__dict__
        except:
            self.mode = 0
            self.online = False
            self.address = '127.0.0.1:25565'

    @staticmethod
    def _load():
        global Setting
        Setting = Settings(data)

    @staticmethod
    def _dump():
        try:
            dump(data, Setting)
        except: ...

    def ast(self, index):
        return ast[self.mode][index]

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        self._dump()

Settings._load()
