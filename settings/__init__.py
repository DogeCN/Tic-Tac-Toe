from .iobase import load, dump
import os

datadir = os.getenv("AppData") + os.sep + "Tic-Tac-Toe"
if not os.path.exists(datadir):
    os.mkdir(datadir)
data = datadir + os.sep + "settings.dat"

ast = [
    [False, True, False, False],
    [True, False, True, False],
    [False, False, False, False],
    [True, True, True, True],
]


class Settings:
    def __init__(self, file):
        config = {"mode": 0, "online": False, "address": "127.0.0.1:25565"}
        try:
            config.update(load(file).__dict__)
        except:
            ...
        self.__dict__ = config

    @staticmethod
    def _load():
        global Setting
        Setting = Settings(data)

    @staticmethod
    def dump():
        try:
            dump(data, Setting)
        except:
            ...

    def ast(self, index):
        return ast[self.mode][index]


Settings._load()
