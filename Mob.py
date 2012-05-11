""" Basic Mob class """
import pygame 
import os
from pygame import sprite
from sets import Set
from uuid import uuid4
import math
class Mob(sprite.Sprite):
    '''
    Mob Class
    '''
    def __init__(self, name, image, portrait):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', image))
        self.rect = self.image.get_rect()
        self.portrait = pygame.image.load(os.path.join('images', portrait))
        self.portrait_rect = self.portrait.get_rect()
        self.pathlines = None
        self.selected = False
        self.fov = Set()
        self.name = name
        self.job = None
        self.max_hp = 20
        self.hp = self.max_hp
        self.str = 7
        self.defense = 3
        self.x = None
        self.y = None
        self.z = None
        self.alive = True
        self.uuid = uuid4()
        self.view_range = 5
        self.experience = 250
        self.type = "monster"
        self.level = 1
        
    def get_level(self):
        return self.level 
        
    def take_damage(self, damage):
        """ ouch """
        if damage <= 0:
            #print "Damage absorbed"
            pass
        else:
            self.hp = self.hp - damage
        if self.hp <= 0:
            #print "Monster is dead"
            return False
        return True
        
    def pressed_portrait(self, mx, my):
        """ Was my picture clicked """
        if mx > self.portrait_rect.topleft[0]:
            if my > self.portrait_rect.topleft[1]:
                if mx < self.portrait_rect.bottomright[0]:
                    if my < self.portrait_rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
        