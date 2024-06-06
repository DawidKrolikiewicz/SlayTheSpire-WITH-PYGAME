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
            if o.Effect.FLAME_BARRIER in target.dict_of_ongoing and target.dict_of_ongoing[
                o.Effect.FLAME_BARRIER].intensity > 0:
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
            self.next_action = self.attack_3

    def gain_3_ritual(self, player, list_of_enemies):
        self.add_ritual(3, self)

    def attack_3(self, player, list_of_enemies):
        self.deal_damage(3, player)


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
        self.last_action = None
        self.thrash_count = 0

    def declare_action(self, player, list_of_enemies):
        if self.state == 0:
            self.next_action = self.attack_11
            self.state = 1
            self.last_action = self.attack_11
            self.thrash_count = 0
        else:
            actions_weights = {
                self.attack_11: 25,
                self.attack_7_block_5: 30,
                self.gain_3_strength_block_6: 45
            }

            if self.last_action == self.gain_3_strength_block_6:
                actions_weights[self.gain_3_strength_block_6] = 0
            if self.last_action == self.attack_11:
                actions_weights[self.attack_11] = 0
            if self.thrash_count >= 2:
                actions_weights[self.attack_7_block_5] = 0

            total_weight = sum(actions_weights.values())
            if total_weight == 0:
                self.next_action = self.attack_11
            else:
                self.next_action = \
                random.choices(list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

            if self.next_action == self.attack_7_block_5:
                self.thrash_count += 1
            else:
                self.thrash_count = 0

            self.last_action = self.next_action

    def attack_11(self, player, list_of_enemies):
        self.deal_damage(11, player)

    def attack_7_block_5(self, player, list_of_enemies):
        self.deal_damage(7, player)
        self.add_block(5, self)

    def gain_3_strength_block_6(self, player, list_of_enemies):
        self.add_strength(3, self)
        self.add_block(6, self)


class FungiBeast(Enemy):
    def __init__(self, name="Fungi Beast", health=random.randint(22, 28)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Fungi Beast.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.list_of_actions = [self.attack_6, self.gain_3_strength]
        self.last_action = None
        self.bite_count = 0

    def declare_action(self, player, list_of_enemies):
        actions_weights = {
            self.attack_6: 60,
            self.gain_3_strength: 40
        }

        if self.last_action == self.gain_3_strength:
            actions_weights[self.gain_3_strength] = 0
        if self.bite_count >= 2:
            actions_weights[self.attack_6] = 0

        total_weight = sum(actions_weights.values())
        if total_weight == 0:
            self.next_action = self.gain_3_strength if self.bite_count >= 2 else self.attack_6
        else:
            self.next_action = random.choices(
                list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

        if self.next_action == self.attack_6:
            self.bite_count += 1
        else:
            self.bite_count = 0

        self.last_action = self.next_action

    def attack_6(self, player, list_of_enemies):
        self.deal_damage(6, player)

    def gain_3_strength(self, player, list_of_enemies):
        self.add_strength(3, self)


class RedLouse(Enemy):
    def __init__(self, name="Red Louse", health=random.randint(10, 15), d=random.randint(5, 7)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.d = d
        self.add_curlup(random.randint(3, 7), self)
        self.image_sprite = pygame.image.load("../Sprites/Characters/Red Louse.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.list_of_actions = [self.attack_d, self.gain_3_strength]
        self.last_actions = []

    def declare_action(self, player, list_of_enemies):
        actions_weights = {
            self.attack_d: 75,
            self.gain_3_strength: 25
        }

        if len(self.last_actions) >= 2 and self.last_actions[-1] == self.last_actions[-2]:
            if self.last_actions[-1] == self.attack_d:
                actions_weights[self.attack_d] = 0
            else:
                actions_weights[self.gain_3_strength] = 0

        total_weight = sum(actions_weights.values())
        if total_weight == 0:
            self.next_action = self.attack_d if self.last_actions[-1] == self.gain_3_strength else self.gain_3_strength
        else:
            self.next_action = random.choices(
                list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

        self.last_actions.append(self.next_action)
        if len(self.last_actions) > 2:
            self.last_actions.pop(0)

    def attack_d(self, player, list_of_enemies):
        self.deal_damage(self.d, player)

    def gain_3_strength(self, player, list_of_enemies):
        self.add_strength(3, self)


class GreenLouse(Enemy):
    def __init__(self, name="Green Louse", health=random.randint(11, 17), d=random.randint(5, 7)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.d = d
        self.add_curlup(random.randint(3, 7), self)
        self.image_sprite = pygame.image.load("../Sprites/Characters/Green Louse.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.list_of_actions = [self.attack_d, self.apply_3_weak]
        self.last_actions = []

    def declare_action(self, player, list_of_enemies):
        actions_weights = {
            self.attack_d: 75,
            self.apply_3_weak: 25
        }

        if len(self.last_actions) >= 2 and self.last_actions[-1] == self.last_actions[-2]:
            if self.last_actions[-1] == self.attack_d:
                actions_weights[self.attack_d] = 0
            else:
                actions_weights[self.apply_3_weak] = 0

        total_weight = sum(actions_weights.values())
        if total_weight == 0:
            self.next_action = self.attack_d if self.last_actions[-1] == self.apply_3_weak else self.apply_3_weak
        else:
            self.next_action = random.choices(
                list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

        self.last_actions.append(self.next_action)
        if len(self.last_actions) > 2:
            self.last_actions.pop(0)

    def attack_d(self, player, list_of_enemies):
        self.deal_damage(self.d, player)

    def apply_3_weak(self, player, list_of_enemies):
        self.add_weak(3, player)


class BlueSlaver(Enemy):
    def __init__(self, name="Blue Slaver", health=random.randint(46, 50)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Blue Slaver.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340
        self.last_actions = []

        self.list_of_actions = [self.attack_12, self.attack_7_apply_2_weak]
        self.state = 0

    def declare_action(self, player, list_of_enemies):
        actions_weights = {
            self.attack_12: 60,
            self.attack_7_apply_2_weak: 40
        }

        if len(self.last_actions) >= 2 and self.last_actions[-1] == self.last_actions[-2]:
            if self.last_actions[-1] == self.attack_12:
                actions_weights[self.attack_12] = 0
            else:
                actions_weights[self.attack_7_apply_2_weak] = 0

        total_weight = sum(actions_weights.values())
        if total_weight == 0:
            self.next_action = self.attack_12 if self.last_actions[
                                                     -1] == self.attack_7_apply_2_weak else self.attack_7_apply_2_weak
        else:
            self.next_action = random.choices(
                list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

        self.last_actions.append(self.next_action)
        if len(self.last_actions) > 2:
            self.last_actions.pop(0)

    def attack_12(self, player, list_of_enemies):
        self.deal_damage(12, player)

    def attack_7_apply_2_weak(self, player, list_of_enemies):
        self.deal_damage(7, player)
        self.add_weak(2, player)


class RedSlaver(Enemy):
    def __init__(self, name="Red Slaver", health=random.randint(46, 50), d=random.randint(5, 7)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Red Slaver.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.list_of_actions = [self.attack_13, self.attack_8_apply_2_vulnerable, self.apply_1_entangled]
        self.state = 0
        self.last_actions = []
        self.entangle_used = False
        self.scrape_count = 0

    def declare_action(self, player, list_of_enemies):
        if self.state == 0:
            self.next_action = self.attack_13
            self.state = 1
        else:
            if not self.entangle_used:
                if random.random() < 0.25:
                    self.next_action = self.apply_1_entangled
                    self.entangle_used = True
                    self.scrape_count = 0
                else:
                    if self.scrape_count < 2:
                        self.next_action = self.attack_8_apply_2_vulnerable
                        self.scrape_count += 1
                    else:
                        self.next_action = self.attack_13
                        self.scrape_count = 0
            else:
                actions_weights = {
                    self.attack_13: 45,
                    self.attack_8_apply_2_vulnerable: 55
                }

                if len(self.last_actions) >= 2 and self.last_actions[-1] == self.last_actions[-2]:
                    if self.last_actions[-1] == self.attack_13:
                        actions_weights[self.attack_13] = 0
                    else:
                        actions_weights[self.attack_8_apply_2_vulnerable] = 0

                total_weight = sum(actions_weights.values())
                if total_weight == 0:
                    self.next_action = self.attack_13 if self.last_actions[
                                                             -1] == self.attack_8_apply_2_vulnerable else self.attack_8_apply_2_vulnerable
                else:
                    self.next_action = random.choices(
                        list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

        self.last_actions.append(self.next_action)
        if len(self.last_actions) > 2:
            self.last_actions.pop(0)

    def attack_13(self, player, list_of_enemies):
        self.deal_damage(13, player)

    def attack_8_apply_2_vulnerable(self, player, list_of_enemies):
        self.deal_damage(8, player)
        self.add_vulnerable(2, player)

    def apply_1_entangled(self, player, list_of_enemies):
        self.add_entangled(1, player)


class AcidSlimeL(Enemy):
    def __init__(self, name="Acid Slime", health=random.randint(65, 69)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Acid Slime (L).png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.list_of_actions = [self.attack_11_shuffle_2_slimed, self.apply_3_weak, self.attack_16]
        self.state = 0
        self.last_actions = []
        self.split_triggered = False

    def declare_action(self, player, list_of_enemies):
        if self.cur_health <= self.max_health / 2 and not self.split_triggered:
            self.next_action = self.split
            return

        actions_weights = {
            self.attack_11_shuffle_2_slimed: 30,
            self.apply_3_weak: 40,
            self.attack_16: 30
            }

        if len(self.last_actions) >= 1 and self.last_actions[-1] in [self.attack_16, self.apply_3_weak]:
            actions_weights[self.last_actions[-1]] = 0

        if len(self.last_actions) >= 2 and self.last_actions[-1] == self.last_actions[-2]:
            for action in self.list_of_actions:
                if action != self.last_actions[-1]:
                    actions_weights[action] = actions_weights.get(action, 0)

        total_weight = sum(actions_weights.values())
        if total_weight == 0:
            self.next_action = random.choice(
                [action for action in self.list_of_actions if action != self.last_actions[-1]])
        else:
            self.next_action = random.choices(
                list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

        self.last_actions.append(self.next_action)
        if len(self.last_actions) > 3:
            self.last_actions.pop(0)

    def attack_11_shuffle_2_slimed(self, player, list_of_enemies):
        self.deal_damage(11, player)
        # placeholder dopoki slimed nie dodam
        player.add_card_to_discard(cardsFile.Wound())
        player.add_card_to_discard(cardsFile.Wound())

    def attack_16(self, player, list_of_enemies):
        self.deal_damage(16, player)

    def apply_3_weak(self, player, list_of_enemies):
        self.add_weak(3, player)

    def split(self, player, list_of_enemies):
        self.split_triggered = True

        new_slime_1 = AcidSlimeM(health=self.cur_health)
        new_slime_2 = AcidSlimeM(health=self.cur_health)

        list_of_enemies.append(new_slime_1)
        list_of_enemies.append(new_slime_2)
        list_of_enemies.remove(self)


class AcidSlimeM(Enemy):
    def __init__(self, name="Acid Slime", health=random.randint(28, 32)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Acid Slime (M).png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.list_of_actions = [self.attack_7_shuffle_1_slimed, self.apply_2_weak, self.attack_10]
        self.state = 0
        self.last_actions = []
        self.split_triggered = False

    def declare_action(self, player, list_of_enemies):
        actions_weights = {
            self.attack_7_shuffle_1_slimed: 30,
            self.apply_2_weak: 40,
            self.attack_10: 30
        }

        if len(self.last_actions) >= 1 and self.last_actions[-1] in [self.attack_10, self.apply_2_weak]:
            actions_weights[self.last_actions[-1]] = 0

        if len(self.last_actions) >= 2 and self.last_actions[-1] == self.last_actions[-2]:
            for action in self.list_of_actions:
                if action != self.last_actions[-1]:
                    actions_weights[action] = actions_weights.get(action, 0)

        total_weight = sum(actions_weights.values())
        if total_weight == 0:
            self.next_action = random.choice(
                [action for action in self.list_of_actions if action != self.last_actions[-1]])
        else:
            self.next_action = random.choices(
                list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

        self.last_actions.append(self.next_action)
        if len(self.last_actions) > 3:
            self.last_actions.pop(0)

    def attack_7_shuffle_1_slimed(self, player, list_of_enemies):
        self.deal_damage(7, player)
        # placeholder dopoki slimed nie dodam
        player.add_card_to_discard(cardsFile.Wound())

    def attack_10(self, player, list_of_enemies):
        self.deal_damage(10, player)

    def apply_2_weak(self, player, list_of_enemies):
        self.add_weak(2, player)