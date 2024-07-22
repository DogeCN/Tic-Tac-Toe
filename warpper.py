from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

class Button(QPushButton):
    _sign = 0

    def __init__(self, parent, row, column):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setFlat(True)
        self.row = row
        self.column = column

    def react(self):
        WapperInstances.default.apply(self)

class RawWapper:
    text = ''
    icon = None #type: QIcon
    style = 'font-size: 40px;'
    custom_style = ''

    def apply(self, button:Button):
        button.setText(self.text)
        if self.icon:
            button.setIcon(self.icon)
        button.setStyleSheet(self.style + self.custom_style)

class Warpper(RawWapper):
    stack = [] #type: list[Button]

    def __init__(self, index):
        self.index = index

    def apply(self, button:Button):
        super().apply(button)
        for b in self.stack:
            b.sign -= 1
            if b.sign == 0:
                self.stack.remove(b)
        self.stack.append(button)
        print(self.index, button.row, button.column, button.sign)
        button.sign = 3

class WapperGroup:
    skins = (Warpper(0), Warpper(1))
    _index = 0
    
    @property
    def index(self):
        index = self._index
        self._index = 0 if index else 1
        return index

    def wapper(self, index:int):
        return self.skins[index]

    def apply(self, button:Button):
        skin = self.skins[self.index]
        skin.apply(button)

class WapperInstances:

    default = WapperGroup()

    wapper1 = default.wapper(0)
    wapper1.text = '〇'
    wapper1.style = 'font: 700 60px; color: green;'

    wapper2 = default.wapper(1)
    wapper2.text = '⨯'
    wapper2.style = 'font-size: 80px; color: red;'

    empty = RawWapper()
