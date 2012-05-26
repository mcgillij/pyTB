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
        if not pygame.font.get_init():
            pygame.font.init()
        self.arial_font = pygame.font.SysFont('Arial', 16)
        self.images = [pygame.image.load(os.path.join('images', 'attack.png')),
                    pygame.image.load(os.path.join('images', 'defense.png'))
                    ]
        
    def update_stats(self, e):
        """ Show the stats """
        black = (0, 0, 0)
        white = (255, 255, 255)
        pygame.surface.Surface.fill(self, black)
        if e == None:
            pass
        elif e.type == "player": 
            pygame.surface.Surface.blit(self, self.arial_font.render('Stats: ', True, white), (0, 0))
            health = "Health: " + str(e.hp) + "/" + str(e.max_hp)
            strength = str(e.get_attack_bonus())
            defense = str(e.get_defense_bonus())
            job = "Job: " + e.job.job_name
            experience = "XP: " + str(e.experience)
            level = "Level: " + str(e.get_level())
            pygame.surface.Surface.blit(self, self.arial_font.render(e.name, True, white), (0, 20))
            pygame.surface.Surface.blit(self, self.arial_font.render(health, True, white), (0, 40))
            pygame.surface.Surface.blit(self, self.images[0], (0, 60))
            pygame.surface.Surface.blit(self, self.arial_font.render(strength, True, white), (32, 60))
            pygame.surface.Surface.blit(self, self.images[1], (64, 60))
            pygame.surface.Surface.blit(self, self.arial_font.render(defense, True, white), (96, 60))
            pygame.surface.Surface.blit(self, self.arial_font.render(job, True, white), (0, 100))
            pygame.surface.Surface.blit(self, self.arial_font.render(experience, True, white), (0, 120))
            pygame.surface.Surface.blit(self, self.arial_font.render(level, True, white), (0, 140))
            pygame.surface.Surface.blit(self, e.portrait, (0, 156))
            
        elif e.type == "monster":
            pygame.surface.Surface.blit(self, self.arial_font.render('Stats: ', True, white), (0, 0))
            health = "Health: " + str(e.hp) + "/" + str(e.max_hp)
            strength = str(e.get_attack_bonus())
            defense = str(e.get_defense_bonus())
            job = "Job: " + e.job.job_name
            experience = "XP: " + str(e.experience)
            level = "Level: " + str(e.get_level())
            pygame.surface.Surface.blit(self, self.arial_font.render(e.name, True, white), (0, 20))
            pygame.surface.Surface.blit(self, self.arial_font.render(health, True, white), (0, 40))
            pygame.surface.Surface.blit(self, self.images[0], (0, 60))
            pygame.surface.Surface.blit(self, self.arial_font.render(strength, True, white), (32, 60))
            pygame.surface.Surface.blit(self, self.images[1], (64, 60))
            pygame.surface.Surface.blit(self, self.arial_font.render(defense, True, white), (96, 60))
            pygame.surface.Surface.blit(self, self.arial_font.render(job, True, white), (0, 100))
            pygame.surface.Surface.blit(self, self.arial_font.render(experience, True, white), (0, 120))
            pygame.surface.Surface.blit(self, self.arial_font.render(level, True, white), (0, 140))
            pygame.surface.Surface.blit(self, e.portrait, (0, 156))