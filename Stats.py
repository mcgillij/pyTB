""" This will be for the statistics window """
import pygame

class Stats(pygame.surface.Surface):
    """ Stats class """
    def __init__(self, height, width):
        pygame.surface.Surface.__init__(self,(width, height))
        self.height = height
        self.width = width
        pygame.surface.Surface.fill(self,(111, 111, 111))
        #self.fill((0, 0, 0))
        
    def display_stats_for(self, e):
        """ Show the stats """
        rectangle = pygame.Rect((0, 0), (self.width, self.height))
        gray = (115, 115, 115)
        #self.fill(gray, rectangle)
        #self.blit(portrait, portrait_rect ) 
        pygame.draw.rect(self, gray, rectangle, 5)
            
        