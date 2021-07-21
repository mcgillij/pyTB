""" This will be for the item display window """
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class ItemDisplay(pygame.surface.Surface):
    """ItemDisplay class"""

    def __init__(self, height, width):
        pygame.surface.Surface.__init__(self, (width, height))
        self.height = height
        self.width = width
        pygame.surface.Surface.fill(self, (155, 111, 111))
        if not pygame.font.get_init():
            pygame.font.init()
        self.arial_font = pygame.font.SysFont("Arial", 16)

    def update_stats(self, item):
        """Show the item stats"""
        pygame.surface.Surface.fill(self, BLACK)
        pygame.surface.Surface.blit(
            self, self.arial_font.render("Item: " + item.name, True, WHITE), (0, 0)
        )
        pygame.surface.Surface.blit(self, item.image, (0, 20))
        pygame.surface.Surface.blit(
            self,
            self.arial_font.render("Description: " + item.desc, True, WHITE),
            (0, 60),
        )
        pygame.surface.Surface.blit(
            self, self.arial_font.render("Slot: " + item.slot, True, WHITE), (0, 80)
        )
        pygame.surface.Surface.blit(
            self,
            self.arial_font.render("Effects: " + str(item.effects), True, WHITE),
            (0, 100),
        )
