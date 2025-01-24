from PySide6.QtWidgets import QPushButton


class Button(QPushButton):
    style_sheet = ""
    color = (255, 255, 255)
    opacity = 0

    def __init__(self, parent, row, column):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setFlat(True)
        self.row = row
        self.column = column

    @property
    def sign(self):
        return self.opacity * 3 // 255

    @sign.setter
    def sign(self, sign: int):
        self.opacity = sign * 255 // 3
        self.style_update()

    def style_update(self):
        color = f"color: rgba{(*self.color, self.opacity)};"
        self.setStyleSheet(self.style_sheet + color)


class Wrapper:
    text = ""
    style = "font-size: 40px;"
    color = (255, 255, 255)

    def apply(self, button: Button):
        button.setText(self.text)
        button.color = self.color
        button.style_sheet = self.style
        button.style_update()

    @staticmethod
    def clear(button: Button):
        Wrapper().apply(button)
        button.sign = 0


class ButtonQueue(list[Button]):
    def __init__(self):
        super().__init__()

    def append(self, button: Button):
        super().insert(0, button)
        for i in range(len(self)):
            button = self[i]
            sign = 3 - i
            if not sign:
                Wrapper.clear(self.pop())
            else:
                button.sign = sign

    def clear(self):
        for button in self:
            Wrapper.clear(button)
        super().clear()
