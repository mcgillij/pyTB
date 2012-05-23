""" ItemGenerator used to get a random item, or a specific item created. """
import ConfigParser
from Item import Item
import os
from random import choice

# load up the items into a list of config files, will be read by the __init__ of the ItemGenerator class
ITEMS_DIR = 'items'
DIR_PATH = os.path.join(os.getcwd(), ITEMS_DIR)
FILES_IN_DIR = os.listdir(DIR_PATH)
FILE_LIST = []
for filename in FILES_IN_DIR:
    FILE_LIST.append(os.path.join(DIR_PATH, filename))


class ItemGenerator():
    """ ItemGenerator Class """
    def __init__(self):
        self.item_list = []
        for file_ref in FILE_LIST:
            config = ConfigParser.ConfigParser()
            config.readfp(open(file_ref))
            name = config.get('item', 'name')
            image = config.get('item', 'image')
            special = config.getboolean('item', 'special')
            desc = config.get('item', 'desc')
            effect = config.get('item', 'effect')
            slot = config.get('item', 'slot')
            item = Item(name, image, special)
            item.slot = slot
            item.desc = desc
            if effect != "None":
                effect_list = effect.split(',')
                for e in effect_list:
                    key, value = e.split(':')
                    item.effects[key] = value
            self.item_list.append(item)
        
    def generate_random_item(self):
        """ generates a random item, that isn't "special" like stairs """
        attempts = 0
        while attempts <= 100:
            item_choice = choice(self.item_list)
            if item_choice.special == False:
                return item_choice
        return None #random's really bad at this point or we have no items that aren't special
    
    def generate_specific_item(self, name):
        # used to fetch stairs and the likes 
        for item in self.item_list:
            if item.name == name:
                return item
        return None # could not find the specified item
    
    
if __name__ == '__main__':
    #debugging
    IG = ItemGenerator()
    for x in range(10):
        temp_item = IG.generate_random_item()
        print temp_item.name
        print temp_item.slot
        print str(temp_item.effects)
    