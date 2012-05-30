""" This is the quit popup screen """
import pygame
from pgu import gui
from pygame.locals import * #IGNORE:W0614

class QuitDialogue(gui.Dialog):
    """ Base class for the Quit screen """
    def __init__(self, **params):
        self.running = True
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        container = gui.Table()
        container.tr()
        quit_button = gui.Button("Quit")
        quit_button.connect(gui.CLICK, self.exit_game)
        cancel_button = gui.Button("Cancel (esc)")
        cancel_button.connect(gui.CLICK, self.cancel_exit)
        container.td(quit_button)
        container.td(gui.Spacer(width=20, height=10))
        container.td(cancel_button)
    # Buttons
        self.app.init(container)
        title = gui.Label("Quit?")
        self.cancel = False
        gui.Dialog.__init__(self, title, container)

    def exit_game(self):
        """ exits the game """
        self.running = False
        
    def cancel_exit(self):
        """ Cancel quitting the game """
        self.running = False
        self.cancel = True

    def run(self, temp_screen):
        """ main function that gets executed by the main game """
        while self.running:
            temp_screen.fill((0, 0, 0))
            self.app.paint(temp_screen)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.cancel = True
                        self.running = False
                else:
                    self.app.event(event)
            pygame.display.update()
        # if they clicked cancel return True and don't end the program
        if self.cancel:
            return True
        else:
            return False
# debugging
if __name__ == '__main__':
    SCREEN = pygame.display.set_mode((800, 600))
    QD = QuitDialogue()
    val = QD.run(SCREEN)
    print val