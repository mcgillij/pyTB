"""This is a helper class to create a color picker for the players pathlines"""
import pygame
from pygame.locals import * #IGNORE:W0614
from pgu import gui

class ColorPicker(gui.Dialog):
    """ creates a color picker """ 
    def __init__(self, value, **params):
        self.value = list(gui.parse_color(value))
        title = gui.Label("Color Picker")
        table = gui.Table()
        table.tr()
        
        self.color = gui.Color(self.value, width=64, height=64)
        table.td(self.color, rowspan=3, colspan=1)
        
        table.td(gui.Label(' Red: '), 1, 0)
        h_slider_red = gui.HSlider(value=self.value[0], min=0, max=255, size=32, width=128, height=16)
        h_slider_red.connect(gui.CHANGE, self.adjust, (0, h_slider_red))
        table.td(h_slider_red, 2, 0)
        
        table.td(gui.Label(' Green: '), 1, 1)
        h_slider_green = gui.HSlider(value=self.value[1], min=0, max=255, size=32, width=128, height=16)
        h_slider_green.connect(gui.CHANGE, self.adjust, (1, h_slider_green))
        table.td(h_slider_green, 2, 1)

        table.td(gui.Label(' Blue: '), 1, 2)
        h_slider_blue = gui.HSlider(value=self.value[2], min=0, max=255, size=32, width=128, height=16)
        h_slider_blue.connect(gui.CHANGE, self.adjust, (2, h_slider_blue))
        table.td(h_slider_blue, 2, 2)
                        
        gui.Dialog.__init__(self, title, table)
        
    def adjust(self, value):
        """ adjust the slider values """
        (num, slider) = value
        self.value[num] = slider.value
        self.color.repaint()
        self.send(gui.CHANGE)

# Debugging 
if __name__ == '__main__':
    
    app = gui.Desktop()
    app.connect(gui.QUIT, app.quit, None)
    c = gui.Table(width=640, height=480)
    dialog = ColorPicker("#00ffff")
    e = gui.Button("Color")
    e.connect(gui.CLICK, dialog.open, None)
    c.tr()
    c.td(e)
    app.run(c)