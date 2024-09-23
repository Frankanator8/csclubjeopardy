from text import Text
from textinput import TextInput


class Screen:
    BOARD = 0
    TEXT = 1
    TEXTANDINPUT = 2
    WIN = 3
    curr = BOARD

    drawText = ""
    input = None

    @classmethod
    def init(cls):
        Screen.input = TextInput(300, 400, Text("", ("Calibri", 100), (0, 0, 0), (300, 400)), 3)