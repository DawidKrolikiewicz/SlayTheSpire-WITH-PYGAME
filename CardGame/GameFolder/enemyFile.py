import random
import pygame
import characterFile
import cardsFile


# ========================================= Enemy (superclass) =========================================

class Enemy(characterFile.Character):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.list_of_actions = []
        self.next_action = None

        self.image_next_action = characterFile.text_font.render(f"{self.next_action}", True, (0, 0, 0))
        self.rect_next_action = self.image_next_action.get_rect()
        self.rect_next_action.centerx = self.rect_sprite.centerx
        self.rect_next_action.top = self.rect_sprite.top - 4

    def update(self, screen):
        super().update(screen)

        if self.next_action is not None:
            self.image_next_action = characterFile.text_font.render(f"{self.next_action.__name__}", True, (0, 0, 0))
            self.rect_next_action = self.image_next_action.get_rect()
            self.rect_next_action.centerx = self.rect_sprite.centerx
            self.rect_next_action.bottom = self.rect_sprite.top - 4

            pygame.draw.rect(screen, (255, 0, 0), self.rect_next_action)
            screen.blit(self.image_next_action, self.rect_next_action.topleft)

    def declare_action(self, player, list_of_enemies):
        if self.list_of_actions:
            self.next_action = self.list_of_actions[random.randint(0, len(self.list_of_actions) - 1)]
            print(f">>  {self.name}'s Next Action: {self.next_action.__name__}")
        else:
            print(f">>  THIS ENEMY DOESNT HAVE ANY ACTIONS!!!")

    def play_action(self, player, list_of_enemies):
        if self.next_action is not None:
            self.next_action(player, list_of_enemies)


# ========================================== Specific Enemies ==========================================

class Frog(Enemy):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.image_sprite = pygame.image.load("Enemies/frog.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 370

        self.list_of_actions = [self.attack_7, self.attack_2_block_4, self.str_1_block_1]

    def attack_7(self, player, list_of_enemies):
        print(f">> {self.name} attacks!")
        self.deal_damage(7, player)

    def attack_2_block_4(self, player, list_of_enemies):
        print(f">> {self.name} attacks and blocks!")
        self.deal_damage(2, player)
        self.add_armor(4, self)

    def str_1_block_1(self, player, list_of_enemies):
        print(f">> {self.name} gains strength and blocks!")
        self.add_str(1, self)
        self.add_armor(1, self)


class Worm(Enemy):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.image_sprite = pygame.image.load("Enemies/worm.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 370

        self.list_of_actions = [self.attack_2_x2, self.heal_enemies_3]

    def attack_2_x2(self, player, list_of_enemies):
        print(f">> {self.name} attacks twice!")
        self.deal_damage(2, player)
        self.deal_damage(2, player)

    def heal_enemies_3(self, player, list_of_enemies):
        print(f">> {self.name} heal itself and it's allies!")
        for enemy in list_of_enemies:
            self.heal(3, enemy)




