import random
import pygame
import characterFile
import ongoingFile as o
import cardsFile


# ========================================= Enemy (superclass) =========================================

class Enemy(characterFile.Character):
    def __init__(self, name="DEFAULT ENEMY", health=100):
        super().__init__(name, health)
        self.name = "Enemy"
        self.max_health = 1
        self.cur_health = self.max_health
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

    def deal_damage(self, damage, target, is_attack=True, hit_block=True):
        super().deal_damage(damage, target, is_attack, hit_block)
        if target.__class__.__name__ == "Player" and damage > 0:
            if o.Effect.FLAME_BARRIER in target.dict_of_ongoing and target.dict_of_ongoing[o.Effect.FLAME_BARRIER].intensity > 0:
                target.deal_damage(target.dict_of_ongoing[o.Effect.FLAME_BARRIER].intensity, self)

    def declare_action(self, player, list_of_enemies):
        if self.list_of_actions:
            self.next_action = self.list_of_actions[random.randint(0, len(self.list_of_actions) - 1)]
            print(f">>  {self.name}'s Next Action: {self.next_action.__name__}")
        else:
            print(f">>  THIS ENEMY DOESNT HAVE ANY ACTIONS!!!")

    def play_action(self, player, list_of_enemies):
        if self.next_action is not None:
            self.next_action(player, list_of_enemies)


# ========================================== Specific Characters ==========================================

class Frog(Enemy):
    def __init__(self, name="Frog", health=12):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Frog.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.list_of_actions = [self.attack_7, self.attack_2_block_4, self.gain_str_1_and_block_1]

    def attack_7(self, player, list_of_enemies):
        print(f">> {self.name} attacks!")
        self.deal_damage(7, player)

    def attack_2_block_4(self, player, list_of_enemies):
        print(f">> {self.name} attacks and blocks!")
        self.deal_damage(2, player)
        self.add_block(4, self)

    def gain_str_1_and_block_1(self, player, list_of_enemies):
        print(f">> {self.name} gains strength and blocks!")
        self.add_strength(1, self)
        self.add_block(1, self)


class Worm(Enemy):
    def __init__(self, name="Worm", health=11):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Worm.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.list_of_actions = [self.attack_2_x2, self.heal_enemies_3, self.give_2_vulnerable]

    def attack_2_x2(self, player, list_of_enemies):
        print(f">> {self.name} attacks twice!")
        self.deal_damage(2, player)
        self.deal_damage(2, player)

    def heal_enemies_3(self, player, list_of_enemies):
        print(f">> {self.name} heal itself and it's allies!")
        for enemy in list_of_enemies:
            self.heal(3, enemy)

    def give_2_vulnerable(self, player, list_of_enemies):
        print(f">> {self.name} weakens player's defences!")
        self.add_vulnerable(2, player)


class Icecream(Enemy):
    def __init__(self, name="EVIL ICECREAM", health=30):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Icecream.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340
        self.rage = False

        self.list_of_actions = [self.shuffle_2_depression, self.attack_3_and_block_1]

    def declare_action(self, player, list_of_enemies):
        if player.cur_health <= self.block:
            self.next_action = self.deal_damage_equal_to_block
        elif self.cur_health <= (self.max_health // 2) or self.rage:
            self.rage = True
            self.next_action = self.gain_1_dex_and_block_7
        else:
            self.next_action = self.list_of_actions[random.randint(0, len(self.list_of_actions) - 1)]

    def shuffle_2_depression(self, player, list_of_enemies):
        player.add_card_to_discard(cardsFile.Depression())
        player.add_card_to_discard(cardsFile.Depression())

    def gain_1_dex_and_block_7(self, player, list_of_enemies):
        self.add_dexterity(1, self)
        self.add_block(7, self)

    def attack_3_and_block_1(self, player, list_of_enemies):
        self.deal_damage(3, player)
        self.add_block(1, self)

    def deal_damage_equal_to_block(self, player, list_of_enemies):
        self.deal_damage(self.block, player)


class Cultist(Enemy):
    def __init__(self, name="Cultist", health=random.randint(48, 54)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Cultist.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340
        self.state = 0

    def declare_action(self, player, list_of_enemies):
        if self.state == 0:
            self.next_action = self.gain_3_ritual
            self.state = 1
        else:
            self.next_action = self.attack_6

    def gain_3_ritual(self, player, list_of_enemies):
        self.add_ritual(3, self)

    def attack_6(self, player, list_of_enemies):
        self.deal_damage(6, player)


class JawWorm(Enemy):
    def __init__(self, name="Jaw Worm", health=random.randint(40, 44)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Jaw Worm.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.list_of_actions = [self.attack_11, self.attack_7_block_5, self.gain_3_strength_block_6]
        self.state = 0

    def declare_action(self, player, list_of_enemies):
        if self.state == 0:
            self.next_action = self.attack_11
            self.state = 1
        else:
            # IDK HOW TO DO IT :(
            # WEIGHTED + REPEATABLE PREVENTION
            self.next_action = random.choice(self.list_of_actions)
            pass

    def attack_11(self, player, list_of_enemies):
        self.deal_damage(11, player)

    def attack_7_block_5(self, player, list_of_enemies):
        self.deal_damage(7, player)
        self.add_block(5, self)

    def gain_3_strength_block_6(self, player, list_of_enemies):
        self.add_strength(3, self)
        self.add_block(6, self)
