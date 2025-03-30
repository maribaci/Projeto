import sys

import pygame

from Code.Const import C_RED, WIN_WIDTH, C_YELLOW
from Code.Enemy import Enemy
from Code.Entity import Entity
from Code.Player import Player

class EntityMediator:
    game_over_bg = pygame.image.load("./asset/GameOver.png")

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
            bg_resized = pygame.transform.scale(EntityMediator.game_over_bg, screen.get_size())
            screen.blit(bg_resized, (0, 0))
            pygame.display.flip()
            pygame.time.delay(5000)

        EntityMediator.return_to_main()

    @staticmethod
    def return_to_main():
        import main
        main.run_game()