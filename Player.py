import pygame
import os
from pygame import sprite
from sets import Set
from uuid import uuid4
import math
class Player(sprite.Sprite):
    '''
    Player Class
    '''
    def __init__(self, name, job):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image_name = 'dorf.png'
        self.image = pygame.image.load(os.path.join('images', self.image_name))
        self.rect = self.image.get_rect()
        self.portrait_name = 'portrait_player.png'
        self.portrait = pygame.image.load(os.path.join('images', self.portrait_name))
        self.portrait_rect = self.portrait.get_rect()
        self.pathlines = None
        self.fov = Set()
        self.selected = False
        self.name = name
        self.job = job
        self.max_hp = 125
        self.hp = self.max_hp
        self.str = 9
        self.defense = 3
        self.x = 0
        self.y = 0
        self.z = 0
        self.color = (255, 255, 255)
        self.alive = True
        self.uuid = uuid4()
        self.view_range = 5
        self.experience = 0
        self.type = "player"
        
    def re_init_images(self):
        # this has to be done to reload the sprite after loading a game
        self.image = pygame.image.load(os.path.join('images', self.image_name))
        self.rect = self.image.get_rect()
        self.portrait = pygame.image.load(os.path.join('images', self.portrait_name))
        self.portrait_rect = self.portrait.get_rect()
        
        
    def get_level(self):
        """ return the level based on the xp recieved so far """
        return int(math.floor((1 + math.sqrt(self.experience / 125 + 1)) / 2))
    
    def get_attack_bonus(self):
        """ return the job attack bonus + the str bonus that's not implemented yet :) """
        #would add effects from items here.
        return int(self.job.attack_bonus) + self.get_level()
        
    def get_defense_bonus(self):
        """ return the job defense bonus and the level bonus till I get the stats bonus's worked out """
        return self.get_level() + int(self.job.defense_bonus)
    
    def get_view_range(self):
        """ return the view range with bonuses """
        return self.view_range + int(self.job.view_range_bonus)
    
    def gain_xp(self, num):
        """ Gain some Xp """
        self.experience = self.experience + num
    
    def take_damage(self, damage):
        """ Ouch """
        if damage <= 0:
            pass
            #print "Damage absorbed"
        else:
            self.hp = self.hp - damage
        if self.hp <= 0:
            #print "Monster is dead"
            return False
        return True
    
    def heal(self, num):
        """ heals the player for num """
        if self.hp + num >= self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = self.hp + num
        
    def pressed_portrait(self, mx, my):
        """ portrait was clicked """
        if mx > self.portrait_rect.topleft[0]:
            if my > self.portrait_rect.topleft[1]:
                if mx < self.portrait_rect.bottomright[0]:
                    if my < self.portrait_rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
        