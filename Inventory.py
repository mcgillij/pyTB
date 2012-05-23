""" Inventory class """
import pygame
import pgu #IGNORE:W0614
from pgu import gui
from ItemGenerator import ItemGenerator
from pygame.locals import * #IGNORE:W0614
from pprint import pprint
from ItemDisplay import ItemDisplay
class Inventory(gui.Dialog):
    """ Base class for the inventory screen """
    def __init__(self, **params):
        self.running = True
        self.app = gui.App()
        self.player_list_box = gui.List(width=200, height=100)
        self.player_list = []
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.item_display = ItemDisplay(200, 200)
        container = gui.Table()
       
    # Buttons
        add_button = gui.Button('Add')
        add_button.connect(gui.CLICK, self.add_item_to_list)
        remove = gui.Button("Remove")
        remove.connect(gui.CLICK, self.remove_from_list, None)
        clear = gui.Button("Clear")
        clear.connect(gui.CLICK, self.clear_player_list, None)
        container.tr()
        container.td(add_button, align=-1)
        container.td(clear, align=-1)
        container.td(remove, align=-1)
        container.tr()
        container.td(self.player_list_box, colspan=3)
        container.tr()
        start_game_button = gui.Button('exit')
        start_game_button.connect(gui.CLICK, self.exit_inventory)
        container.td(start_game_button, colspan=2)
        self.app.init(container)
        
        
        
    def add_item_to_list(self):
        #$pprint(item)
        ig = ItemGenerator()
        item = ig.generate_random_item()
        pprint(item)
        self.player_list_box.add(item.name, value=item)
        
    def exit_inventory(self, load=False):
        """ exits the inventory """
        self.running = False
        
    def clear_player_list(self, item):
        """ Clear the player list """
        self.player_list_box.clear()
        self.player_list_box.resize()
        self.player_list_box.repaint()
    
    def remove_from_list(self, item):
        """ remove selected item from the list """
        list_value = self.player_list_box.value
        if list_value:
            item = list_value
            self.player_list_box.remove(item)
            self.player_list_box.resize()
            self.player_list_box.repaint()
            
    def draw_selected_item(self, screen):
        if self.player_list_box.value:
            self.item_display.update_stats(self.player_list_box.value)
            screen.blit(self.item_display, (0, 0))
    def run(self, temp_screen):
        """ main function that gets executed by the main game """
        running = True
        while running:
            temp_screen.fill((0, 0, 0))
            self.app.paint(temp_screen)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                self.app.event(event)
            self.draw_selected_item(temp_screen)
            pygame.display.update()
            if self.running == False:
                running = False

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    inventory = Inventory()
    inventory.run(screen)
    