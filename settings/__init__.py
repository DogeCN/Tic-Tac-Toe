from .iobase import load, dump
import os

data = os.getenv('AppData') + os.sep + 'Tic-Tac-Toe'

class Settings:
    def __init__(self, file):
        try:
            self.__dict__ = load(file).__dict__
        except:
            self.mode = 0

    @staticmethod
    def _load():
        global Setting
        Setting = Settings(data)

    @staticmethod
    def _dump():
        try:
            dump(data, Setting)
        except: ...

    def __getattr__(self, name):
        self._load()
        return super().__getattr__(self, name)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        self._dump()

Settings._load()
