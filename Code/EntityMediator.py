import sys

import pygame

from Code.Const import C_RED, WIN_WIDTH
from Code.Enemy import Enemy
from Code.Entity import Entity
from Code.Player import Player

class EntityMediator:

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for entity in entity_list:
            EntityMediator.__handle_window_collision(entity)

        players = [e for e in entity_list if isinstance(e, Player)]
        enemies = [e for e in entity_list if isinstance(e, Enemy)]

        for player in players:
            collided = False
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    EntityMediator.show_game_over()
                    return
                else:
                    collided = True

            if collided:
                player.score += 1

    @staticmethod
    def __handle_window_collision(entity: Entity):
        if isinstance(entity, Enemy) and entity.rect.right <= 0:
            entity.score = 0


    @staticmethod
    def show_game_over():
        pygame.mixer_music.load('./asset/over.mp3')
        pygame.mixer_music.play(-1)
        screen = pygame.display.get_surface()
        if screen:
            screen.fill((0, 0, 0))
            EntityMediator.__draw_text(screen, 80, "Game Over", C_RED, ((WIN_WIDTH //2), 100))
            pygame.display.flip()
            pygame.time.delay(5000)

        EntityMediator.quit_game()

    @staticmethod
    def __draw_text(surface, size: int, text: str, color: tuple, position: tuple):
        font = pygame.font.SysFont("Comic Sans MS", size)
        text_surface = font.render(text, True, color).convert_alpha()
        text_rect = text_surface.get_rect(center=position)
        surface.blit(text_surface, text_rect)

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()




