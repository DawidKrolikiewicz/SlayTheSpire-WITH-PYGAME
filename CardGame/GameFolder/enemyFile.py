import random
import pygame
import characterFile
import cardsFile


class Enemy(characterFile.Character):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.list_of_actions = []
        self.next_action = None

        self.image = pygame.image.load("Enemies/Don'tMakeInstancesOfBaseEnemyPLS.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = 370

        self.image_name = characterFile.text_font.render(self.name, True, (0, 0, 0))
        self.name_rect = self.image_name.get_rect()
        self.name_rect.top = self.rect.bottom + 4

        self.image_hp = characterFile.text_font.render(f"[{self.armor}] {self.cur_health} / {self.max_health} HP", True, (0, 0, 0))
        self.hp_rect = self.image_hp.get_rect()
        self.hp_rect.top = self.name_rect.bottom + 4

    def update(self, screen, player):
        # DRAWING ENEMY SPRITE
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        screen.blit(self.image, self.rect.topleft)

        # DRAWING ENEMY NAME
        self.name_rect.centerx = self.rect.centerx
        pygame.draw.rect(screen, (0, 100, 255), self.name_rect)
        screen.blit(self.image_name, self.name_rect.topleft)

        # DRAWING ENEMY HP
        self.image_hp = characterFile.text_font.render(f"[{self.armor}] {self.cur_health} / {self.max_health} HP", True, (0, 0, 0))
        self.hp_rect.centerx = self.rect.centerx
        pygame.draw.rect(screen, (0, 100, 255), self.hp_rect)
        screen.blit(self.image_hp, self.hp_rect.topleft)

    def declare_action(self, player, list_of_enemies):
        if self.list_of_actions:
            self.next_action = self.list_of_actions[random.randint(0, len(self.list_of_actions) - 1)]
            print(f">>  {self.name}'s Next Action: {self.next_action.__name__}")
        else:
            print(f">>  THIS ENEMY DOESNT HAVE ANY ACTIONS!!!")

    def play_action(self, player, list_of_enemies):
        if self.next_action is not None:
            self.next_action(player, list_of_enemies)


class Enemy1(Enemy):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.list_of_actions = [self.attack_6, self.gain_6_armor, self.give_1_vuln]

    def attack_6(self, player, list_of_enemies):
        print(f">>  {self.name} attacks!")
        self.deal_damage(6, player)

    def gain_6_armor(self, player, list_of_enemies):
        print(f">>  {self.name} puts up his defences!")
        self.add_armor(6, self)

    def give_1_vuln(self, player, list_of_enemies):
        print(f">>  {self.name} makes you more vulnerable!")
        self.add_vuln(1, player)


class Frog(Enemy):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.image = pygame.image.load("Enemies/frog.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = 370

        self.list_of_actions = [self.attack_7, self.attack_2_block_4, self.str_1_block_1]



    def attack_7(self, player, list_of_enemies):
        print(f">> {self.name} attacks!")
        self.deal_damage(7, player)
        player.add_card_to_deck(cardsFile.Depression())

    def attack_2_block_4(self, player, list_of_enemies):
        print(f">> {self.name} attacks and blocks!")
        self.deal_damage(2, player)
        self.add_armor(4, self)
        player.add_card_to_deck(cardsFile.Depression())

    def str_1_block_1(self, player, list_of_enemies):
        print(f">> {self.name} gains strength and blocks!")
        self.add_str(1, self)
        self.add_armor(1, self)
        player.add_card_to_deck(cardsFile.Depression())


class Worm(Enemy):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.image = pygame.image.load("Enemies/worm.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = 370

        self.list_of_actions = [self.attack_2_x2, self.heal_enemies_3]

    def attack_2_x2(self, player, list_of_enemies):
        print(f">> {self.name} attacks twice!")
        self.deal_damage(2, player)
        self.deal_damage(2, player)

    def heal_enemies_3(self, player, list_of_enemies):
        print(f">> {self.name} heal itself and it's allies!")
        for enemy in list_of_enemies:
            self.heal(3, enemy)




