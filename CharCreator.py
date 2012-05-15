""" CharCreator, will house the character generator / creator allowing players to create custom chars """
import pygame
from pygame.locals import *  #IGNORE:W0614
from Player import Player
from random import randint
from pgu import gui
from pprint import pprint
from Job import Job
from JobList import JobList
from CombatLog import CombatLog
from ColorPicker import ColorPicker
import os
class CharCreator(gui.Dialog):
    """ Base char creator class """
    def __init__(self,**params):
        #self.app = gui.Desktop(width=800, height=600)
        self.running = True
        self.app = gui.App()
        title = gui.Label("Character Creator")
        self.main_list = []
        self.player_list_box = gui.List(width=200, height=100)
        self.player_list = []
        self.JL = JobList()
        job_list = self.JL.get_list()
        self.value = gui.Form()
        
        t = gui.Table()
      
        t.tr()
        t.td(gui.Label("Name"),align=0,colspan=3)
        t.td(gui.Input(name="name",value='your name here',size=20))
        t.tr()
        t.td(gui.Spacer(width=8,height=8))
        t.tr()
        t.td(gui.Label("Strength: "),align=1)
        self.str_input = gui.Input(name="strength", value=12, size=3)
        t.td(self.str_input )
        b = gui.Button("Roll")
        b.connect(gui.CLICK, self.roll_str)
        t.td(b)
        t.tr()
        t.tr()
        t.td(gui.Label("Defense: "),align=1)
        self.def_input = gui.Input(name="defense", value=12, size=3)
        t.td(self.def_input)
        d = gui.Button("Roll")
        d.connect(gui.CLICK, self.roll_def)
        t.td(d)
        t.tr()
        t.td(gui.Label("View Range: "),align=1)
        t.td(gui.Input(name="view_range", value=5, size=2))
        t.tr()
        
        t.td(gui.Label("Job: "),align=1)
        self.job_select = gui.Select(name="job_selection")
        for job in job_list:
            self.job_select.add(job.job_name, job.job_name)
        self.job_select.connect(gui.CHANGE, self.on_change_select)
        t.td(self.job_select)
        t.tr()
        t.td(gui.Spacer(width=8,height=8))
        t.tr()
        self.ta = CombatLog(width=400, height=200)
        t.td(self.ta, colspan=2)
        t.tr()
        t.td(gui.Label("Color: "))
        default_color = "#ffffff"
        color = gui.Color(default_color, width=60, height=20, name='color')
        picker = ColorPicker(default_color)
        color.connect(gui.CLICK, gui.action_open, {'container': t, 'window': picker})
        picker.connect(gui.CHANGE, gui.action_setvalue, (picker, color))
        t.td(color)
        t.tr()
        e = gui.Button("Okay")
        e.connect(gui.CLICK,self.send,gui.CHANGE)
        t.td(e)
        
        e = gui.Button("Cancel")
        e.connect(gui.CLICK,self.close,None)
        t.td(e)
        
        gui.Dialog.__init__(self,title,t)
    
    def on_change_select(self):
        
        job = self.JL.generate_job_for(self.job_select.value)
        text = "Job name: " + job.job_name + "\n"
        text += "Attack bonus: " + str(job.attack_bonus) + "\n"
        text += "Defense bonus: " + str(job.defense_bonus) + "\n"
        text += "View range bonus: " + str(job.view_range_bonus) + "\n"
        text += job.description
        self.ta.value = text
        #pprint(self.job_select.value)
        
    
    def roll_def(self):
        roll1 = roll_d_6()
        roll2 = roll_d_6()
        roll3 = roll_d_6()
        self.def_input.value = roll1 + roll2 + roll3
        #self.repaint()
    
    def roll_str(self):
        roll1 = roll_d_6()
        roll2 = roll_d_6()
        roll3 = roll_d_6()
        self.str_input.value = roll1 + roll2 + roll3
        #self.repaint()

    def onchange(self, value):
        print('-----------')
        temp_dict = {}
        for k,v in value.value.items():
            print(k,v)
            temp_dict[k] = v
        value.close()
        #pprint(temp_dict)
        temp_job = self.JL.generate_job_for(temp_dict['job_selection'])
        temp_player = Player(temp_dict['name'], temp_job )
        self.player_list_box.add(temp_player.name, value=temp_player)
        self.main_list.append(temp_player)
        #self.player_list.append(temp_player)
        
    def fetch_player_list(self):
        self.running = False
        print "Am I gettin called?"
        temp_list = []
        for p in self.player_list_box.items:
            temp_list.append(p.value)
            #pprint(p.value)
        #self.app.quit()
        print "Templist"
        pprint(temp_list)
        return temp_list
        #pprint(self.main_list)
        #return self.main_list
    def get_player_list(self):
        print "LIST GOD DAMN IT?"
        self.running = False
        temp_list = []
        for p in self.player_list_box.items:
            temp_list.append(p.value)
            #pprint(p.value)
        return temp_list
        #self.app.quit()
        
            
    def clear_player_list(self, item):
        self.player_list_box.clear()
        self.player_list_box.resize()
        self.player_list_box.repaint()
    
    def remove_from_list(self, item):
        list_value = self.player_list_box.value
        if list_value:
            item = list_value
            self.player_list_box.remove(item)
            self.player_list_box.resize()
            self.player_list_box.repaint()
    
    def run(self, temp_screen):
        self.app.connect(gui.QUIT,self.app.quit,None)
        title_image = gui.Image(pygame.image.load(os.path.join('images', 'title.png')))
        c = gui.Table()
        #dialog = CharCreator()
        self.connect(gui.CHANGE,self.onchange,self)
    # Buttons
        new_char = gui.Button("New Character")
        new_char.connect(gui.CLICK, self.open, None)
        remove = gui.Button("Remove")
        remove.connect(gui.CLICK, self.remove_from_list, None)
        clear = gui.Button("Clear")
        clear.connect(gui.CLICK, self.clear_player_list, None)
        c.tr()
        c.td(title_image, colspan=3, align=0)
        c.tr()
        c.td(new_char, align=-1)
        c.td(clear, align=-1)
        c.td(remove, align=-1)
        c.tr()
        c.td(gui.Label("Current Roster"), colspan=3)
        c.tr()
        c.td(self.player_list_box, colspan=3)
        c.tr()
        d = gui.Button('Start Game with current party')
        d.connect(gui.CLICK, self.fetch_player_list)
        #d.connect(gui.CLICK, self.app.quit)
        c.td(d, colspan=3)
        self.app.init(c)
        
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
        pprint(self.player_list_box.items)
        print "Done"
        
            
        
        

def change_stuff(value):
    s, doc = value
    doc.value = s.value
    
def roll_d_6():
    return randint(1, 6)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    CC = CharCreator()
    CC.run(screen)