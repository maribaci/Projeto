from Code.Enemy import Enemy
from Code.Entity import Entity
from Code.Player import Player

class EntityMediator:
    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy) and ent.rect.right <= 0:
            ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1: Entity, ent2: Entity):
        if isinstance(ent1, Player) and isinstance(ent2, Enemy):
            if ent1.rect.colliderect(ent2.rect):
                #ent1.health -= ent2.damage
                #ent2.health -= ent1.damage
                EntityMediator.end_game()

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_dmg == 'Player':
            for ent in entity_list:
                if isinstance(ent, Player) and ent.name == 'Player1':
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i, entity1 in enumerate(entity_list):
            EntityMediator.__verify_collision_window(entity1)
            if entity1.name == "Player1":
                for entity2 in entity_list[i + 1:]:
                    EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        to_remove = [ent for ent in entity_list if ent.health <= 0]
        for ent in to_remove:
            if isinstance(ent, Enemy):
                EntityMediator.__give_score(ent, entity_list)
            entity_list.remove(ent)

    @staticmethod
    def end_game():
        print("Game Over!")
