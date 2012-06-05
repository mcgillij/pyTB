""" Inventory class """
import pygame
from pgu import gui
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
        self.item_display = ItemDisplay(300, 600)
        container = gui.Table()

    # Buttons
        equip_button = gui.Button('Use / Equip')
        equip_button.connect(gui.CLICK, self.equip_or_use_item, None)
        remove = gui.Button("Drop selected item")
        remove.connect(gui.CLICK, self.remove_from_list, None)
        container.tr()
        container.td(equip_button, align=-1)
        container.td(remove, align=-1)
        container.tr()
        container.td(self.player_list_box, colspan=3)
        container.tr()
        start_game_button = gui.Button('exit (esc)')
        start_game_button.connect(gui.CLICK, self.exit_inventory)
        container.td(start_game_button, colspan=2)
        self.app.init(container)
        title = gui.Label("Inventory")
        gui.Dialog.__init__(self, title, container)
        
    def equip_or_use_item(self, item):
        """ use or equip the passed in item """
        list_value = self.player_list_box.value
        if list_value:
            if list_value.slot != "None": # equipment
                if list_value.equipped: # if the items already equipped unequip it.
                    list_value.equipped = False
                else: # check to make sure there's not another item in the same slot already.
                    filtered = filter(is_equipped, self.player.backpack)
                    for equipped_item in filtered:
                        if equipped_item.slot == list_value.slot:
                            equipped_item.equipped = False
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

    def exit_inventory(self):
        """ exits the inventory """
        self.running = False

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
        """ Draws the selected itembox to the screen with its info """
        if self.player_list_box.value:
            self.item_display.update_stats(self.player_list_box.value)
            screen.blit(self.item_display, (0, 0))

    def run(self, temp_screen):
        """ main function that gets executed by the main game """
        while self.running:
            temp_screen.fill((0, 0, 0))
            self.app.paint(temp_screen)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                else:
                    self.app.event(event)
            self.draw_selected_item(temp_screen)
            pygame.display.update()
        return self.drop_list
    
def is_equipped(item):
    """ checks if the item is equipped """
    return item.equipped