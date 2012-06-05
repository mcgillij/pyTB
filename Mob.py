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
    def __init__(self, name, job, image, portrait, dead_image):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image_name = image
        self.image = pygame.image.load(os.path.join('images', self.image_name))
        self.rect = self.image.get_rect()
        self.portrait_name = portrait
        self.portrait = pygame.image.load(os.path.join('images', self.portrait_name))
        self.portrait_rect = self.portrait.get_rect()
        self.dead_image_name = dead_image
        self.dead_image = pygame.image.load(os.path.join('images', self.dead_image_name))
        self.pathlines = None
        self.selected = False
        self.fov = Set()
        self.name = name
        self.job = job
        self.x = None
        self.y = None
        self.z = None
        self.alive = True
        self.uuid = uuid4()
        self.view_range = 5
        self.experience = 250
        self.type = "monster"
        self.level = 1
        self.max_hp = self.job.hit_dice * self.level
        self.hp = self.max_hp
        
    def re_init_images(self):
        # required after loading the game
        self.image = pygame.image.load(os.path.join('images', self.image_name))
        self.rect = self.image.get_rect()
        self.portrait = pygame.image.load(os.path.join('images', self.portrait_name))
        self.portrait_rect = self.portrait.get_rect()
        self.dead_image = pygame.image.load(os.path.join('images', self.dead_image_name))
        
        
    def get_level(self):
        """ Levels for monsters are hard coded as they don't have xp to base it off """
        return self.level 
    
    def get_attack_bonus(self):
        """ get the attack bonus """
        return int(self.job.attack_bonus) + int(self.level * 0.5) + 1
    
    def get_defense_bonus(self):
        """ get the defense bonus """
        return 10 + int(self.job.defense_bonus) + int(self.level * 0.5) + 1
        
    def get_view_range(self):
        """ get the view range """
        return self.view_range + int(self.job.view_range_bonus)
    
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
        