import pygame
import os
from pygame import sprite
from sets import Set
from uuid import uuid4
class Player(sprite.Sprite):
    '''
    Player Class
    '''
    def __init__(self,name,job,x,y,z):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images','dorf.png'))
        self.rect = self.image.get_rect()
        self.portrait = pygame.image.load(os.path.join('images','portrait_player.png'))
        self.portrait_rect = self.portrait.get_rect()
        self.pathlines = None
        self.fov = Set()
        self.selected = False
        self.name = name
        self.job = job
        self.hp = 20
        self.str = 10
        self.defense = 2
        self.x = x
        self.y = y
        self.z = z
        self.alive = True
        self.uuid = uuid4()
    
    def take_damage(self, damage):
        if damage <= 0:
            pass
            #print "Damage absorbed"
        else:
            self.hp = self.hp - damage
        if self.hp <= 0:
            #print "Monster is dead"
            return False
        return True
        
    def pressed_portrait(self,mx,my):
        if mx > self.portrait_rect.topleft[0]:
            if my > self.portrait_rect.topleft[1]:
                if mx < self.portrait_rect.bottomright[0]:
                    if my < self.portrait_rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
        