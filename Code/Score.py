import sys
from datetime import datetime
import pygame
from pygame import Surface, Rect, KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from pygame.font import Font
from Code.Const import C_YELLOW, SCORE_POS, C_CYAN, MENU_OPTION
from Code.DBProxy import DBProxy


class Score:
    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(topleft=(0, 0))
        self.db_proxy = DBProxy('DBScore')

    def save(self, game_mode: str, player_score: list[int]):
        self._play_music()
        name = ''
        score = player_score[0] if game_mode == MENU_OPTION[0] else player_score[0]

        while True:
            self._render_background()
            self._display_text(60, 'YOU WIN!!', C_YELLOW, SCORE_POS['Title'])
            self._display_text(20, 'Enter your name (4 characters):', C_YELLOW, SCORE_POS['Label'])
            self._display_text(20, name, C_CYAN, SCORE_POS['Name'])
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        self.db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 4 and event.unicode.isprintable():
                        name += event.unicode

    def show(self):
        self._play_music()
        self._render_background()
        self._display_text(48, 'SCORE', C_YELLOW, SCORE_POS['Title'])
        self._display_text(20, 'NAME     SCORE           DATE      ', C_YELLOW, SCORE_POS['Label'])

        list_score = self.db_proxy.retrieve_top10()
        for index, (id_, name, score, date) in enumerate(list_score):
            self._display_text(20, f'{name}     {score:05d}     {date}', C_CYAN,
                               SCORE_POS.get(index, (100, 100 + index * 30)))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
            pygame.display.flip()

    def _display_text(self, size: int, text: str, color: tuple, position: tuple):
        font: Font = pygame.font.SysFont("Times New Roman", size)
        text_surf: Surface = font.render(text, True, color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=position)
        self.window.blit(text_surf, text_rect)

    def _render_background(self):
        self.window.blit(self.surf, self.rect)

    @staticmethod
    def _play_music():
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)

def get_formatted_date():
    return datetime.now().strftime("%H:%M - %d/%m/%y")