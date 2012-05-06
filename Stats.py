""" This will be for the statistics window """
import pygame
import os

class Stats(pygame.surface.Surface):
    """ Stats class """
    def __init__(self, height, width):
        pygame.surface.Surface.__init__(self,(width, height))
        self.height = height
        self.width = width
        pygame.surface.Surface.fill(self,(155, 111, 111))
        #self.fill((0, 0, 0))
        if not pygame.font.get_init():
            pygame.font.init()
        self.arial_font = pygame.font.SysFont('Arial', 16)
        self.images = [pygame.image.load(os.path.join('images', 'attack.png')),
                    pygame.image.load(os.path.join('images', 'defense.png'))
                    ]
        
    def update_stats(self, e):
        """ Show the stats """
        black = (0, 0, 0)
        gray = (115, 115, 115)
        white = (255, 255, 255)
        pygame.surface.Surface.fill(self, black)
        #rectangle = pygame.Rect((0, 0), (self.width, self.height))
        
        if e == None:
            #self.fill(gray, rectangle)
            #self.blit(portrait, portrait_rect ) 
            pygame.surface.Surface.blit(self, self.arial_font.render('Stats: ', True, white), (0, 0))
            #pygame.draw.rect(self, gray, rectangle, 5)
        else: 
            pygame.surface.Surface.blit(self, self.arial_font.render('Stats: ', True, white), (0, 0))
            name_hp = e.name + ": " + str(e.hp) + "/" + str(e.max_hp)
            strength = str(e.str)
            defense = str(e.defense)
            job = "Job: " + e.job
            pygame.surface.Surface.blit(self, self.arial_font.render(name_hp, True, white), (0, 20))
            pygame.surface.Surface.blit(self, self.images[0], (0, 40))
            pygame.surface.Surface.blit(self, self.arial_font.render(strength, True, white), (32, 40))
            pygame.surface.Surface.blit(self, self.images[1], (64, 40))
            pygame.surface.Surface.blit(self, self.arial_font.render(defense, True, white), (96, 40))
            pygame.surface.Surface.blit(self, self.arial_font.render(job, True, white), (0, 80))
            pygame.surface.Surface.blit(self, e.portrait, (0, 96))
           
            
        