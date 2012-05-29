""" Player Info class will probably be used when a player is selected and the user presses c"""
import pygame
from pgu import gui
from pygame.locals import * #IGNORE:W0614
from pprint import pprint
from CombatLog import CombatLog
import os

class PlayerInfo(gui.Dialog):
    """ Base class for the PlayerInfo screen """
    def __init__(self, player, **params):
        self.running = True
        self.app = gui.Desktop()
        self.player = player
        self.app.connect(gui.QUIT, self.app.quit, None)
        container = gui.Table()
        container.tr()
        
        player_image = gui.Image(pygame.image.load(os.path.join('images', player.image_name)))
        portrait_image = gui.Image(pygame.image.load(os.path.join('images', player.portrait_name)))
        container.td(portrait_image)
        container.tr()
        container.td(player_image)
        container.tr()
        container.td(gui.Label("Name: " + player.name), colspan=2, align=-1)
        container.tr()
        container.td(gui.Label("Job: " + player.job.job_name), colspan=2, align=-1)
        container.tr()
        container.td(gui.Label("Attack Bonus: " + str(player.job.attack_bonus)), colspan=2, align=-1)
        container.tr()
        container.td(gui.Label("Defense Bonus: " + str(player.job.defense_bonus)), colspan=2, align=-1)
        container.tr()
        container.td(gui.Label("View Range Bonus: " + str(player.job.view_range_bonus)), colspan=2, align=-1)
        container.tr()
        container.td(gui.Label("Base Damage Roll: d" + str(player.job.damage)), colspan=2, align=-1)
        container.tr()
        container.td(gui.Label("Job Description: "), colspan=2, align=-1)
        container.tr()
        TA = gui.TextArea(width=300, height=100)
        TA.value = player.job.description
        container.td(TA, colspan=2)
        container.tr()
        container.td(gui.Label("Level: " + str(player.get_level())), colspan=2, align=-1)
        container.tr()
        container.td(gui.Label("XP: " + str(player.experience)), colspan=2, align=-1)
        container.tr()
        container.td(gui.Label("Inventory:"), colspan=2, align=-1)
        container.tr()
        for item in player.backpack:
            container.td(gui.Spacer(width=10, height=10))
            container.td(gui.Label(item.name))
            container.tr()
        exit_button = gui.Button('exit')
        exit_button.connect(gui.CLICK, self.exit_player_info)
        container.td(exit_button, colspan=2)
        self.app.init(container)
        title = gui.Label("Player Info")
        gui.Dialog.__init__(self, title, container)
    
    def exit_player_info(self):
        """ exits the player info screen """
        self.running = False

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
                self.app.event(event)
            pygame.display.update()
            
if __name__ == '__main__':
    from Player import Player
    from JobList import JobList
    JL = JobList()
    job = JL.pick_a_random_job()
    name = "test name"
    player = Player(name, job)
    SCREEN = pygame.display.set_mode((800, 600))
    PI = PlayerInfo(player)
    PI.run(SCREEN)