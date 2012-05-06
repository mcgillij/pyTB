import pygame
import os
from pygame import sprite
from sets import Set
from uuid import uuid4
class Player(sprite.Sprite):
    '''
    Player Class
    '''
    def __init__(self, name, job, x, y, z):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'dorf.png'))
        self.rect = self.image.get_rect()
        self.portrait = pygame.image.load(os.path.join('images', 'portrait_player.png'))
        self.portrait_rect = self.portrait.get_rect()
        self.pathlines = None
        self.fov = Set()
        self.selected = False
        self.name = name
        self.job = job
        self.max_hp = 25
        self.hp = self.max_hp
        self.str = 9
        self.defense = 3
        self.x = x
        self.y = y
        self.z = z
        self.alive = True
        self.uuid = uuid4()
        self.view_range = 5
    
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
        