import sys

import pygame

from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Code.Level import Level
from Code.Menu import Menu
from Code.Score import Score


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [MENU_OPTION[0]]:
                player_score = [0]
                level = Level(self.window, 'Level1', menu_return, player_score)
                collided = level.run(player_score)
                if collided:
                    score.save(menu_return, player_score)

            elif menu_return == MENU_OPTION[1]:
                score.show()
            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                quit()
            else:
                pygame.quit()
                sys.exit()