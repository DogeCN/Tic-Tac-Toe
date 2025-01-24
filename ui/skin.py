from sprites.player import PlayerGroup

default = PlayerGroup()
player1 = default.player(0)
player1.text = "〇"
player1.style = "font: 700 70px;"
player1.color = (0, 255, 0)

player2 = default.player(1)
player2.text = "⨯"
player2.style = "font-size: 100px; padding-bottom : 15px;"
player2.color = (255, 0, 0)
