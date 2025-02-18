import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        #carrega a musica
        pygame.mixer_music.load('./asset/Menu.mp3')
        #toca indefinidamente com '-1'
        pygame.mixer_music.play(-1)

        while True:
            menu = Menu(self.window)
            menu.run()
            pass
            #Check for all events
            #for event in pygame.event.get():
            #    if event.type == pygame.QUIT:
            #        pygame.quit() #Close window
            #        quit()