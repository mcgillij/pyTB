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
    def __init__(self, player, **params):
        self.running = True
        self.app = gui.App()
        self.player = player
        self.item_list = []
        self.drop_list = []
        self.player_list_box = gui.List(width=200, height=100)
        for i in self.player.backpack:
            if i.equipped:
                item_label = "(E) " + i.name
            else:
                item_label = i.name
            self.item_list.append(i)
            self.player_list_box.add(item_label, value=i)
        self.player_list = []
        self.app.connect(gui.QUIT, self.app.quit, None)
        self.item_display = ItemDisplay(200, 200)
        container = gui.Table()
       
    # Buttons
        equip_button = gui.Button('Use / Equip')
        equip_button.connect(gui.CLICK, self.equip_or_use_item, None)
        remove = gui.Button("Drop selected item")
        remove.connect(gui.CLICK, self.remove_from_list, None)
        clear = gui.Button("Drop all items")
        clear.connect(gui.CLICK, self.clear_player_list, None)
        container.tr()
        container.td(equip_button, align=-1)
        container.td(clear, align=-1)
        container.td(remove, align=-1)
        container.tr()
        container.td(self.player_list_box, colspan=3)
        container.tr()
        start_game_button = gui.Button('exit')
        start_game_button.connect(gui.CLICK, self.exit_inventory)
        container.td(start_game_button, colspan=2)
        self.app.init(container)
        
        
        
    def equip_or_use_item(self, item):
        list_value = self.player_list_box.value
        
        if list_value:
            if list_value.slot != "None": # equipment
                if list_value.equipped:
                    list_value.equipped = False
                else:
                    list_value.equipped = True
            else: # consumables
                if 'heal' in list_value.effects:
                    self.player.heal(int(list_value.effects['heal']))
                    self.player.backpack.remove(list_value)        
            self.player_list_box.clear()
            for i in self.player.backpack:
                if i.equipped:
                    item_label = "(E) " + i.name
                else:
                    item_label = i.name
                self.item_list.append(i)
                self.player_list_box.add(item_label, value=i)
            self.player_list_box.resize()
            self.player_list_box.repaint() 
        
    def exit_inventory(self, load=False):
        """ exits the inventory """
        self.running = False
        
    def clear_player_list(self, item):
        """ Clear the player list """
        for i in self.item_list:
            i.equipped = False
            self.player.backpack.remove(i)
            self.drop_list.append(i)
        self.player_list_box.clear()
        self.player_list_box.resize()
        self.player_list_box.repaint()
    
    def remove_from_list(self, item):
        """ remove selected item from the list """
        list_value = self.player_list_box.value
        if list_value:
            item = list_value
            item.equipped = False
            self.player.backpack.remove(item)
            self.drop_list.append(item)
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
        return self.drop_list

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    inventory = Inventory()
    inventory.run(screen)
    