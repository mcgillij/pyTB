"""Generic button class"""
import pygame
import os


class Button(pygame.sprite.Sprite):
    """Class used to create a button, use set_coords to set
    position of topleft corner. Method pressed() returns
    a boolean and should be called inside the input loop."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("images", 'button.png'))
        self.rect = self.image.get_rect()
 
    def set_coords(self, x, y):
        """ Set the top left corner"""
        self.rect.topleft = x, y
        
    def pressed(self, mx, my):
        """ When the button is pressed """
        if mx > self.rect.topleft[0]:
            if my > self.rect.topleft[1]:
                if mx < self.rect.bottomright[0]:
                    if my < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
