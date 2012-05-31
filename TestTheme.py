#import pgu
from pgu import gui

class TestTheme(gui.Theme):
    def __init__(self, **params):
        theme = "test_theme"
        gui.Theme.__init__(self, dirs=theme, **params)