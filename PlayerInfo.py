""" Player Info class will probably be used when a player is selected and the user presses c"""
import os
import pygame
from pgu import gui
from pygame.locals import *  # IGNORE:W0614


class PlayerInfo(gui.Dialog):
    """Base class for the PlayerInfo screen"""

    def __init__(self, player, **params):
        self.player = player
        player_image = gui.Image(
            pygame.image.load(os.path.join("images", player.image_name))
        )
        portrait_image = gui.Image(
            pygame.image.load(os.path.join("images", player.portrait_name))
        )
        container = gui.Table()
        container.tr()
        container.td(gui.Label("Name: " + player.name), align=-1)
        container.td(player_image, rowspan=2, align=1)
        container.tr()
        container.td(
            gui.Label("Health: " + str(player.hp) + " / " + str(player.max_hp)),
            align=-1,
        )
        container.tr()
        container.td(gui.Label("Job: " + player.job.job_name), colspan=2, align=-1)
        container.tr()
        container.td(
            gui.Label("Attack Bonus: " + str(player.job.attack_bonus)),
            colspan=2,
            align=-1,
        )
        container.tr()
        container.td(
            gui.Label("Defense Bonus: " + str(player.job.defense_bonus)),
            colspan=2,
            align=-1,
        )
        container.tr()
        container.td(
            gui.Label("View Range Bonus: " + str(player.job.view_range_bonus)),
            colspan=2,
            align=-1,
        )
        container.tr()
        container.td(
            gui.Label("Hit Dice: d" + str(player.job.hit_dice)), colspan=2, align=-1
        )
        container.tr()
        container.td(
            gui.Label("Base Damage Roll: d" + str(player.job.damage)),
            colspan=2,
            align=-1,
        )
        container.tr()
        container.td(gui.Label("Job Description: "), colspan=2, align=-1)
        container.tr()
        TA = gui.TextArea(width=300, height=100)
        TA.value = player.job.description
        container.td(TA, colspan=2)
        container.tr()
        container.td(
            gui.Label("Level: " + str(player.get_level())), colspan=2, align=-1
        )
        container.tr()
        container.td(gui.Label("XP: " + str(player.experience)), colspan=2, align=-1)
        container.tr()
        container.td(gui.Label("Inventory:"), colspan=2, align=-1)
        container.tr()
        for item in player.backpack:
            container.td(gui.Spacer(width=8, height=8))
            container.td(gui.Label(item.name))
            container.tr()
        container.td(gui.Spacer(width=5, height=32), colspan=2)
        container.tr()
        exit_button = gui.Button("exit info")
        exit_button.connect(gui.CLICK, self.close, None)
        container.td(exit_button, colspan=2)
        title = gui.Label("Player Info")
        gui.Dialog.__init__(self, title, container)
