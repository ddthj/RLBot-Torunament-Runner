import pygame

from gui.matchmaker_gui import Gui
from gui.utils import Globals


def start():
    pygame.init()
    window = pygame.display.set_mode((1920,1080))
    pygame.display.set_caption("TournamentRunner")
    boxBgImage = pygame.image.load('logo/5.png')
    return Globals(window, boxBgImage)


if __name__ == "__main__":
    globals = start()
    hype = Gui(globals)
