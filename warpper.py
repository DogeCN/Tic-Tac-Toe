from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

class Button(QPushButton):
    style_sheet = ''
    color = (255, 255, 255)
    opacity = 255

    def __init__(self, parent, row, column):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setFlat(True)
        self.row = row
        self.column = column
    
    def style_update(self):
        color = f'color: rgba{(*self.color, self.opacity)};'
        self.setStyleSheet(self.style_sheet + color)

    def react(self):
        WapperInstances.default.apply(self)

class ButtonStack(list[Button]):
    def __init__(self):
        super().__init__()
    
    def append(self, button:Button):
        super().insert(0, button)
        for i in range(len(self)):
            button = self[i]
            opacity = 255 - i*255//6
            if not opacity:
                WapperInstances.empty.apply(self.pop(i))
            else:
                button.opacity = opacity
                button.style_update()

class RawWapper:
    text = ''
    icon = None #type: QIcon
    style = 'font-size: 40px;'
    color = (255, 255, 255)

    def apply(self, button:Button):
        button.setText(self.text)
        if self.icon:
            button.setIcon(self.icon)
        button.color = self.color
        button.style_sheet = self.style
        button.style_update()

class Warpper(RawWapper):
    stack = ButtonStack()

    def apply(self, button:Button):
        super().apply(button)
        self.stack.append(button)

class WapperGroup:
    wappers = (Warpper(), Warpper())
    _index = 0
    
    @property
    def index(self):
        index = self._index
        self._index = 0 if index else 1
        return index

    @property
    def stack(self):
        return self.wapper(0).stack + self.wapper(1).stack

    def wapper(self, index:int):
        return self.wappers[index]

    def apply(self, button:Button):
        if button not in self.stack:
            wapper = self.wappers[self.index]
            wapper.apply(button)

class WapperInstances:

    default = WapperGroup()

    wapper1 = default.wapper(0)
    wapper1.text = '〇'
    wapper1.style = 'font: 700 60px;'
    wapper1.color = (0, 255, 0)

    wapper2 = default.wapper(1)
    wapper2.text = '⨯'
    wapper2.style = 'font-size: 80px;'
    wapper2.color = (255, 0, 0)

    empty = RawWapper()
