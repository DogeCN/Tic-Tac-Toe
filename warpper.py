from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

class Button(QPushButton):
    style_sheet = ''
    color = (255, 255, 255)
    opacity = 255
    belong = None #type: Wrapper

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
        WrapperInstances.default.apply(self)

class ButtonQueue(list[Button]):
    def __init__(self):
        super().__init__()
    
    def append(self, button:Button):
        super().insert(0, button)
        for i in range(len(self)):
            button = self[i]
            opacity = 255 - i*255//3
            if not opacity:
                WrapperInstances.empty.apply(self.pop())
            else:
                button.opacity = opacity
                button.style_update()

class RawWrapper:
    name = ''
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

class Wrapper(RawWrapper):

    def __init__(self, index):
        self.index = index
        self.queue = ButtonQueue()

    def apply(self, button:Button):
        super().apply(button)
        self.queue.append(button)
        button.belong = self

class WrapperGroup:
    wrappers = (Wrapper(0), Wrapper(1))
    _index = 0

    def __init__(self):
        self.wrapper(self.index).name = 'First Player'
        self.wrapper(self.index).name = 'Second Player'
    
    @property
    def index(self):
        index = self._index
        self._index = 0 if index else 1
        return index

    @property
    def queue(self):
        return self.wrapper(0).queue + self.wrapper(1).queue

    def wrapper(self, index:int):
        return self.wrappers[index]

    def apply(self, button:Button):
        if button not in self.queue:
            wrapper = self.wrappers[self.index]
            wrapper.apply(button)

class WrapperInstances:

    default = WrapperGroup()

    wrapper1 = default.wrapper(0)
    wrapper1.text = '〇'
    wrapper1.style = 'font: 700 60px;'
    wrapper1.color = (0, 255, 0)

    wrapper2 = default.wrapper(1)
    wrapper2.text = '⨯'
    wrapper2.style = 'font-size: 80px;'
    wrapper2.color = (255, 0, 0)

    empty = RawWrapper()
