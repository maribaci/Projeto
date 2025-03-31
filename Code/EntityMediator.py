import pygame
from Code.Enemy import Enemy
from Code.Entity import Entity
from Code.Player import Player

class EntityMediator:

    @staticmethod
    def game_over_bg():
        return pygame.image.load("./asset/GameOver.png")

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

            if not collided:
                player.score += 10

    @staticmethod
    def __handle_window_collision(entity: Entity):
        if isinstance(entity, Enemy) and entity.rect.right <= 0:
            entity.health = 0

    @staticmethod
    def show_game_over():
        pygame.mixer_music.load('./asset/over.mp3')
        pygame.mixer_music.play(-1)

        screen = pygame.display.get_surface()
        if screen:
            bg_image = EntityMediator.game_over_bg()
            bg_width, bg_height = bg_image.get_size()
            screen_width, screen_height = screen.get_size()

            bg_x = (screen_width - bg_width) // 2
            bg_y = (screen_height - bg_height) // 2

            screen.fill((0, 0, 0))
            screen.blit(bg_image, (bg_x, bg_y))

            pygame.display.flip()
            pygame.time.delay(5000)

        EntityMediator.return_to_main()

    @staticmethod
    def return_to_main():
        from main import run_game
        run_game()
