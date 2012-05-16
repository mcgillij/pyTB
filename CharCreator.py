""" CharCreator, will house the character generator / creator allowing players to create custom chars """
import pygame
from pygame.locals import *  #IGNORE:W0614
from Player import Player
from random import randint
from pgu import gui
from pprint import pprint
from CombatLog import CombatLog
from ColorPicker import ColorPicker
from JobList import JobList
import os
from molecular import Molecule

class CharCreator(gui.Dialog):
    """ Base char creator class """
    def __init__(self, **params):
        self.running = True
        self.app = gui.App()
        title = gui.Label("Character Creator")
        self.main_list = []
        self.player_list_box = gui.List(width=200, height=100)
        self.player_list = []
        self.JL = JobList()
        job_list = self.JL.get_list()
        self.value = gui.Form()
        table = gui.Table()
        table.tr()
        table.td(gui.Label("Name"), align=1)
        self.name_input = gui.Input(name="name", size=20)
        self.name_input.value = namegen_orc_first() + " " + namegen_orc_second()
        table.td(self.name_input)
        table.tr()
        table.td(gui.Spacer(width=8, height=8))
        table.tr()
        table.td(gui.Label("Strength: "), align=1)
        self.str_input = gui.Input(name="strength", value=12, size=3)
        table.td(self.str_input )
        str_roll_button = gui.Button("Roll")
        str_roll_button.connect(gui.CLICK, self.roll_str)
        table.td(str_roll_button)
        table.tr()
        table.td(gui.Spacer(width=8, height=8))
        table.tr()
        table.td(gui.Label("Defense: "), align=1)
        self.def_input = gui.Input(name="defense", value=12, size=3)
        table.td(self.def_input)
        def_roll_button = gui.Button("Roll")
        def_roll_button.connect(gui.CLICK, self.roll_def)
        table.td(def_roll_button)
        table.tr()
        table.td(gui.Spacer(width=8, height=8))
        table.tr()
        table.td(gui.Label("View Range: "), align=1)
        table.td(gui.Input(name="view_range", value=5, size=2))
        table.tr()
        table.td(gui.Spacer(width=8, height=8))
        table.tr()
        table.td(gui.Label("Color: "), align=1)
        default_color = "#ffffff"
        color_square = gui.Color(default_color, width=60, height=20, name='color')
        picker = ColorPicker(default_color)
        color_square.connect(gui.CLICK, gui.action_open, {'container': table, 'window': picker})
        picker.connect(gui.CHANGE, gui.action_setvalue, (picker, color_square))
        table.td(color_square)
        table.tr()
        table.td(gui.Spacer(width=8, height=8))
        table.tr()
        table.td(gui.Label("Job: "), align=1)
        self.job_select = gui.Select(name="job_selection")
        for job in job_list:
            self.job_select.add(job.job_name, job.job_name)
        self.job_select.connect(gui.CHANGE, self.on_change_select)
        table.td(self.job_select)
        table.tr()
        table.td(gui.Spacer(width=8, height=8))
        table.tr()
        self.char_desc_box = CombatLog(width=400, height=200)
        table.td(self.char_desc_box, colspan=2)
        table.tr()
        ok_button = gui.Button("Okay")
        ok_button.connect(gui.CLICK, self.send, gui.CHANGE)
        table.td(ok_button)
        cancel_button = gui.Button("Cancel")
        cancel_button.connect(gui.CLICK, self.close, None)
        table.td(cancel_button)
        gui.Dialog.__init__(self, title, table)
    
    def on_change_select(self):
        """ update the text area with the specific class stats """
        job = self.JL.generate_job_for(self.job_select.value)
        text = "Job name: " + job.job_name + "\n"
        text += "Attack bonus: " + str(job.attack_bonus) + "\n"
        text += "Defense bonus: " + str(job.defense_bonus) + "\n"
        text += "View range bonus: " + str(job.view_range_bonus) + "\n"
        text += job.description
        self.char_desc_box.value = text
     
    def roll_def(self):
        """ roll defense stat """
        roll1 = roll_d_6()
        roll2 = roll_d_6()
        roll3 = roll_d_6()
        self.def_input.value = roll1 + roll2 + roll3
     
    def roll_str(self):
        """ roll strength stat """
        roll1 = roll_d_6()
        roll2 = roll_d_6()
        roll3 = roll_d_6()
        self.str_input.value = roll1 + roll2 + roll3
     
    def onchange(self, value):
        """ Called when the OK button is pressed to generate a new char """
        temp_dict = {}
        for key, v in value.value.items():
            temp_dict[key] = v
        value.close()
        temp_job = self.JL.generate_job_for(temp_dict['job_selection'])
        temp_player = Player(temp_dict['name'], temp_job )
        temp_player.defense = int(temp_dict['defense'])
        temp_player.str = int(temp_dict['strength'])
        temp_player.view_range = int(temp_dict['view_range'])
        player_color = temp_dict['color']
        temp_player.color = (player_color[0], player_color[1], player_color[2])
        self.player_list_box.add(temp_player.name, value=temp_player)
        self.main_list.append(temp_player)
        #setup a random name for the default next window.
        self.name_input.value = namegen_orc_first() + " " + namegen_orc_second()
        
    def fetch_player_list(self):
        """ returns the list of players to the main game and closes the char creator """
        self.running = False
        temp_list = []
        for p in self.player_list_box.items:
            temp_list.append(p.value)
        return temp_list
     
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
    
    def run(self, temp_screen):
        """ main function that gets executed by the main game """
        self.app.connect(gui.QUIT, self.app.quit, None)
        title_image = gui.Image(pygame.image.load(os.path.join('images', 'title.png')))
        container = gui.Table()
        self.connect(gui.CHANGE, self.onchange, self)
    # Buttons
        new_char = gui.Button("New Character")
        new_char.connect(gui.CLICK, self.open, None)
        remove = gui.Button("Remove")
        remove.connect(gui.CLICK, self.remove_from_list, None)
        clear = gui.Button("Clear")
        clear.connect(gui.CLICK, self.clear_player_list, None)
        container.tr()
        container.td(title_image, colspan=3, align=0)
        container.tr()
        container.td(new_char, align=-1)
        container.td(clear, align=-1)
        container.td(remove, align=-1)
        container.tr()
        container.td(gui.Label("Current Roster"), colspan=3)
        container.tr()
        container.td(self.player_list_box, colspan=3)
        container.tr()
        start_game_button = gui.Button('Start Game with current party')
        start_game_button.connect(gui.CLICK, self.fetch_player_list)
        container.td(start_game_button, colspan=3)
        self.app.init(container)
        
        running = True
        while running:
            temp_screen.fill((0, 0, 0))
            self.app.paint(temp_screen)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                self.app.event(event)
            pygame.display.update()
            if self.running == False:
                running = False

def namegen_orc_first():
    name = Molecule()
    name.load("namefiles/orcs_t.nam")
    return name.name()
    
def namegen_orc_second():
    name = Molecule()
    name.load("namefiles/orcs_wh.nam")
    return name.name()

     
def change_stuff(value):
    """ replace the values""" 
    s, doc = value
    doc.value = s.value
    
def roll_d_6():
    """ rolls a d6 """
    return randint(1, 6)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    CC = CharCreator()
    CC.run(screen)