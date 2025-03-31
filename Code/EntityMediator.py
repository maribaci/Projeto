import pygame
from Code.Enemy import Enemy
from Code.Entity import Entity
from Code.Player import Player

class EntityMediator:
    last_score_update = 0
    score_interval = 3000
    enemy_spawned = False

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
            collided = any(
                enemy.name in ("Enemy1", "Enemy2") and player.rect.colliderect(enemy.rect) for enemy in enemies)

            if collided:
                EntityMediator.show_game_over()
                return

            if EntityMediator.enemy_spawned:
                current_time = pygame.time.get_ticks()
                if current_time - EntityMediator.last_score_update >= EntityMediator.score_interval:
                    player.score += 10
                    EntityMediator.last_score_update = current_time

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
            pygame.time.delay(3000)

        EntityMediator.return_to_main()

    @staticmethod
    def return_to_main():
        from main import run_game
        run_game()
