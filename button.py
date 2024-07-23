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

class ButtonQueue(list[Button]):
    def __init__(self):
        super().__init__()
    
    def append(self, button:Button):
        super().insert(0, button)
        for i in range(len(self)):
            button = self[i]
            opacity = 255 - i*255//3
            if not opacity:
                Wrapper.clear(self.pop())
            else:
                button.opacity = opacity
                button.style_update()

class Wrapper:
    text = ''
    style = 'font-size: 40px;'
    color = (255, 255, 255)

    def apply(self, button:Button):
        button.setText(self.text)
        button.color = self.color
        button.style_sheet = self.style
        button.style_update()
    
    @staticmethod
    def clear(button:Button):
        Wrapper().apply(button)
