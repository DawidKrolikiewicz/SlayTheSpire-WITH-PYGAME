import random
import pygame
import characterFile
import ongoingFile as o
import cardsFile
import declarationFile


# ========================================= Enemy (superclass) =========================================

class Enemy(characterFile.Character):
    def __init__(self, name="DEFAULT ENEMY", health=100):
        super().__init__(name, health)
        self.name = "Enemy"
        self.max_health = 1
        self.cur_health = self.max_health
        self.list_of_actions = []
        self.next_action = None

        #self.image_next_action = characterFile.text_font.render(f"{self.next_action}", True, (0, 0, 0))
        #self.rect_next_action = self.image_next_action.get_rect()
        #self.rect_next_action.centerx = self.rect_sprite.centerx
        #self.rect_next_action.top = self.rect_sprite.top - 4

        self.list_incoming = []

    def update(self, screen):
        super().update(screen)

        if self.next_action is not None:
            #self.image_next_action = characterFile.text_font.render(f"{self.next_action.__name__}", True, (0, 0, 0))
            #self.rect_next_action = self.image_next_action.get_rect()
            #self.rect_next_action.centerx = self.rect_sprite.centerx
            #self.rect_next_action.bottom = self.rect_sprite.top - 4

            #pygame.draw.rect(screen, (255, 0, 0), self.rect_next_action)
            #screen.blit(self.image_next_action, self.rect_next_action.topleft)

            outline = pygame.rect.Rect(0, 0, 30*len(self.list_incoming) + 8, 38)
            rect_for_actions = pygame.rect.Rect(0, 0, 30*len(self.list_incoming), 30)
            outline.bottom = self.rect_sprite.top - 2
            outline.centerx = self.rect_sprite.centerx
            rect_for_actions.center = outline.center
            pygame.draw.rect(screen, (148, 6, 30), outline)
            pygame.draw.rect(screen, (196, 194, 195), rect_for_actions)
            offset = 0

            for action_type in self.list_incoming:
                action_type.rect.topleft = rect_for_actions.topleft
                action_type.rect.left += offset
                offset += 30
                screen.blit(action_type.image, action_type.rect.topleft)
                if action_type.value is not None:
                    screen.blit(action_type.value_image, action_type.rect.topleft)
                    action_type.update(screen)

    def deal_damage(self, damage, target, is_attack=True, hit_block=True):
        super().deal_damage(damage, target, is_attack, hit_block)

        if target.__class__.__name__ == "Player" and damage > 0:
            if (o.Effect.FLAME_BARRIER in target.dict_of_ongoing
                    and target.dict_of_ongoing[o.Effect.FLAME_BARRIER].intensity > 0):
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
            self.list_incoming.clear()


# ========================================== Specific Characters ==========================================

class Frog(Enemy):
    def __init__(self, name="Frog", health=12):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Frog.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.list_of_actions = [self.attack_7, self.attack_2_block_4, self.gain_str_1_and_block_1]

    def declare_action(self, player, list_of_enemies):
        super().declare_action(player, list_of_enemies)
        if self.next_action == self.attack_7:
            self.list_incoming.append(declarationFile.Attack(7))
        elif self.next_action == self.attack_2_block_4:
            self.list_incoming.append(declarationFile.Attack(2))
            self.list_incoming.append(declarationFile.Block(4))
        elif self.next_action == self.gain_str_1_and_block_1:
            self.list_incoming.append(declarationFile.Block(1))
            self.list_incoming.append(declarationFile.Buff(1))

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
        self.rect_sprite.bottom = 350

        self.list_of_actions = [self.attack_2_x2, self.heal_enemies_3, self.give_2_vulnerable]

    def declare_action(self, player, list_of_enemies):
        super().declare_action(player, list_of_enemies)
        if self.next_action == self.attack_2_x2:
            self.list_incoming.append(declarationFile.MultiAttack(2, 2))
        elif self.next_action == self.heal_enemies_3:
            self.list_incoming.append(declarationFile.Buff(3))
        elif self.next_action == self.give_2_vulnerable:
            self.list_incoming.append(declarationFile.Debuff(2))

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
        self.rect_sprite.bottom = 350
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

        if self.next_action == self.shuffle_2_depression:
            self.list_incoming.append(declarationFile.Debuff(2))
        elif self.next_action == self.gain_1_dex_and_block_7:
            self.list_incoming.append(declarationFile.Buff(1))
            self.list_incoming.append(declarationFile.Block(7))
        elif self.next_action == self.attack_3_and_block_1:
            self.list_incoming.append(declarationFile.Attack(3))
            self.list_incoming.append(declarationFile.Block(1))
        elif self.next_action == self.deal_damage_equal_to_block:
            self.list_incoming.append(declarationFile.Attack("Block"))

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
        self.rect_sprite.bottom = 350
        self.state = 0

    def declare_action(self, player, list_of_enemies):
        if self.state == 0:
            self.next_action = self.gain_3_ritual
            self.list_incoming.append(declarationFile.Buff(3))
            self.state = 1
        else:
            self.next_action = self.attack_3
            self.list_incoming.append(declarationFile.Attack(3))

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
        self.rect_sprite.bottom = 350

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

        if self.next_action == self.attack_11:
            self.list_incoming.append(declarationFile.Attack(11))
        elif self.next_action == self.attack_7_block_5:
            self.list_incoming.append(declarationFile.Attack(7))
            self.list_incoming.append(declarationFile.Block(5))
        elif self.next_action == self.gain_3_strength_block_6:
            self.list_incoming.append(declarationFile.Block(6))
            self.list_incoming.append(declarationFile.Buff(3))

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
        self.rect_sprite.bottom = 350

        self.add_spore_cloud(2, self)

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

        if self.next_action == self.attack_6:
            self.list_incoming.append(declarationFile.Attack(6))
        elif self.next_action == self.gain_3_strength:
            self.list_incoming.append(declarationFile.Buff(3))

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
        self.rect_sprite.bottom = 350

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

        if self.next_action == self.attack_d:
            self.list_incoming.append(declarationFile.Attack(self.d))
        elif self.next_action == self.gain_3_strength:
            self.list_incoming.append(declarationFile.Buff(3))

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
        self.rect_sprite.bottom = 350

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

        if self.next_action == self.attack_d:
            self.list_incoming.append(declarationFile.Attack(self.d))
        elif self.next_action == self.apply_3_weak:
            self.list_incoming.append(declarationFile.Debuff(3))

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
        self.rect_sprite.bottom = 350
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

        if self.next_action == self.attack_12:
            self.list_incoming.append(declarationFile.Attack(12))
        elif self.next_action == self.attack_7_apply_2_weak:
            self.list_incoming.append(declarationFile.Attack(7))
            self.list_incoming.append(declarationFile.Debuff(2))

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
        self.rect_sprite.bottom = 350

        self.list_of_actions = [self.attack_13, self.attack_8_apply_2_vulnerable, self.apply_2_entangled]
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
                    self.next_action = self.apply_2_entangled
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

        if self.next_action == self.attack_13:
            self.list_incoming.append(declarationFile.Attack(13))
        elif self.next_action == self.attack_8_apply_2_vulnerable:
            self.list_incoming.append(declarationFile.Attack(8))
            self.list_incoming.append(declarationFile.Debuff(2))
        elif self.next_action == self.apply_2_entangled:
            self.list_incoming.append(declarationFile.SuperDebuff(2))

    def attack_13(self, player, list_of_enemies):
        self.deal_damage(13, player)

    def attack_8_apply_2_vulnerable(self, player, list_of_enemies):
        self.deal_damage(8, player)
        self.add_vulnerable(2, player)

    def apply_2_entangled(self, player, list_of_enemies):
        self.add_entangled(2, player)


class AcidSlimeL(Enemy):
    def __init__(self, name="Acid Slime", health=random.randint(65, 69)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Acid Slime (L).png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.list_of_actions = [self.attack_11_shuffle_2_slimed, self.apply_3_weak, self.attack_16]
        self.last_actions = []
        self.split_triggered = False

    def declare_action(self, player, list_of_enemies):
        #if self.cur_health <= self.max_health / 2 and not self.split_triggered:
        #self.next_action = self.split
        #return

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

        if self.next_action == self.attack_11_shuffle_2_slimed:
            self.list_incoming.append(declarationFile.Attack(13))
            self.list_incoming.append(declarationFile.Debuff(2))
        elif self.next_action == self.attack_16:
            self.list_incoming.append(declarationFile.Attack(16))
        elif self.next_action == self.apply_3_weak:
            self.list_incoming.append(declarationFile.Debuff(3))
        elif self.next_action == self.split:
            self.list_incoming.append(declarationFile.Unknown())

    def attack_11_shuffle_2_slimed(self, player, list_of_enemies):
        self.deal_damage(11, player)
        player.add_card_to_discard(cardsFile.Slimed())
        player.add_card_to_discard(cardsFile.Slimed())

    def attack_16(self, player, list_of_enemies):
        self.deal_damage(16, player)

    def apply_3_weak(self, player, list_of_enemies):
        self.add_weak(3, player)

    def split(self, player, list_of_enemies):
        self.split_triggered = True

        new_slime_1 = AcidSlimeM(health=self.cur_health)
        new_slime_2 = AcidSlimeM(health=self.cur_health)

        list_of_enemies.remove(self)
        list_of_enemies.append(new_slime_1)
        list_of_enemies.append(new_slime_2)


class AcidSlimeM(Enemy):
    def __init__(self, name="Acid Slime", health=random.randint(28, 32)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Acid Slime (M).png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.list_of_actions = [self.attack_7_shuffle_1_slimed, self.apply_2_weak, self.attack_10]
        self.last_actions = []

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

        if self.next_action == self.attack_7_shuffle_1_slimed:
            self.list_incoming.append(declarationFile.Attack(7))
            self.list_incoming.append(declarationFile.Debuff(1))
        elif self.next_action == self.attack_10:
            self.list_incoming.append(declarationFile.Attack(10))
        elif self.next_action == self.apply_2_weak:
            self.list_incoming.append(declarationFile.Debuff(2))

    def attack_7_shuffle_1_slimed(self, player, list_of_enemies):
        self.deal_damage(7, player)
        player.add_card_to_discard(cardsFile.Slimed())

    def attack_10(self, player, list_of_enemies):
        self.deal_damage(10, player)

    def apply_2_weak(self, player, list_of_enemies):
        self.add_weak(2, player)


class AcidSlimeS(Enemy):
    def __init__(self, name="Acid Slime", health=random.randint(8, 12)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Acid Slime (S).png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.list_of_actions = [self.apply_2_weak, self.attack_3]
        self.turn_counter = 0

    def declare_action(self, player, list_of_enemies):
        if self.turn_counter == 0:
            self.next_action = random.choice(self.list_of_actions)
        else:
            self.next_action = self.list_of_actions[self.turn_counter % 2]

        self.turn_counter += 1

        if self.next_action == self.attack_3:
            self.list_incoming.append(declarationFile.Attack(3))
            self.list_incoming.append(declarationFile.Debuff(1))
        elif self.next_action == self.apply_2_weak:
            self.list_incoming.append(declarationFile.Debuff(2))

    def attack_3(self, player, list_of_enemies):
        self.deal_damage(3, player)

    def apply_2_weak(self, player, list_of_enemies):
        self.add_weak(2, player)


class SpikeSlimeL(Enemy):
    def __init__(self, name="Spike Slime", health=random.randint(64, 70)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Spike Slime (L).png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.list_of_actions = [self.attack_16_shuffle_2_slimed, self.apply_3_frail]
        self.last_actions = []
        self.split_triggered = False

    def declare_action(self, player, list_of_enemies):
        #if self.cur_health <= self.max_health / 2 and not self.split_triggered:
        #self.next_action = self.split
        #return

        actions_weights = {
            self.attack_16_shuffle_2_slimed: 30,
            self.apply_3_frail: 70
        }

        if len(self.last_actions) >= 2 and self.last_actions[-1] == self.last_actions[-2]:
            if self.last_actions[-1] == self.attack_16_shuffle_2_slimed:
                actions_weights[self.attack_16_shuffle_2_slimed] = 0
            else:
                actions_weights[self.apply_3_frail] = 0

        total_weight = sum(actions_weights.values())

        if total_weight == 0:
            self.next_action = random.choice(
                [action for action in self.list_of_actions if action != self.last_actions[-1]])
        else:
            self.next_action = \
                random.choices(list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

        self.last_actions.append(self.next_action)
        if len(self.last_actions) > 3:
            self.last_actions.pop(0)

        if self.next_action == self.attack_16_shuffle_2_slimed:
            self.list_incoming.append(declarationFile.Attack(16))
            self.list_incoming.append(declarationFile.Debuff(2))
        elif self.next_action == self.apply_3_frail:
            self.list_incoming.append(declarationFile.Debuff(3))
        elif self.next_action == self.split:
            self.list_incoming.append(declarationFile.Unknown())

    def attack_16_shuffle_2_slimed(self, player, list_of_enemies):
        self.deal_damage(16, player)
        player.add_card_to_discard(cardsFile.Slimed())
        player.add_card_to_discard(cardsFile.Slimed())

    def apply_3_frail(self, player, list_of_enemies):
        self.add_frail(3, player)

    def split(self, player, list_of_enemies):
        self.split_triggered = True

        new_slime_1 = SpikeSlimeM(health=self.cur_health)
        new_slime_2 = SpikeSlimeM(health=self.cur_health)

        list_of_enemies.remove(self)
        list_of_enemies.append(new_slime_1)
        list_of_enemies.append(new_slime_2)


class SpikeSlimeM(Enemy):
    def __init__(self, name="Spike Slime", health=random.randint(28, 32)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Spike Slime (M).png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.list_of_actions = [self.attack_8_shuffle_1_slimed, self.apply_2_frail]
        self.last_actions = []

    def declare_action(self, player, list_of_enemies):
        actions_weights = {
            self.attack_8_shuffle_1_slimed: 30,
            self.apply_2_frail: 70
        }

        if len(self.last_actions) >= 2 and self.last_actions[-1] == self.last_actions[-2]:
            if self.last_actions[-1] == self.attack_8_shuffle_1_slimed:
                actions_weights[self.attack_8_shuffle_1_slimed] = 0
            else:
                actions_weights[self.apply_2_frail] = 0

        total_weight = sum(actions_weights.values())

        if total_weight == 0:
            self.next_action = random.choice(
                [action for action in self.list_of_actions if action != self.last_actions[-1]])
        else:
            self.next_action = \
                random.choices(list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

        self.last_actions.append(self.next_action)
        if len(self.last_actions) > 3:
            self.last_actions.pop(0)

        if self.next_action == self.attack_8_shuffle_1_slimed:
            self.list_incoming.append(declarationFile.Attack(8))
            self.list_incoming.append(declarationFile.Debuff(1))
        elif self.next_action == self.apply_2_frail:
            self.list_incoming.append(declarationFile.Debuff(2))

    def attack_8_shuffle_1_slimed(self, player, list_of_enemies):
        self.deal_damage(8, player)
        player.add_card_to_discard(cardsFile.Slimed())

    def apply_2_frail(self, player, list_of_enemies):
        self.add_frail(2, player)


class SpikeSlimeS(Enemy):
    def __init__(self, name="Spike Slime", health=random.randint(10, 14)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Spike Slime (S).png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

    def declare_action(self, player, list_of_enemies):
        self.next_action = self.attack_5
        self.list_incoming.append(declarationFile.Attack(5))

    def attack_5(self, player, list_of_enemies):
        self.deal_damage(5, player)


class FatGremlin(Enemy):
    def __init__(self, name="Fat Gremlin", health=random.randint(13, 17)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Fat Gremlin.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

    def declare_action(self, player, list_of_enemies):
        self.next_action = self.attack_4_add_2_weak
        self.list_incoming.append(declarationFile.Attack(4))
        self.list_incoming.append(declarationFile.Debuff(2))

    def attack_4_add_2_weak(self, player, list_of_enemies):
        self.deal_damage(4, player)
        self.add_weak(2, player)


class MadGremlin(Enemy):
    def __init__(self, name="Mad Gremlin", health=random.randint(20, 24)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Mad Gremlin.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.add_angry(1, self)

    def declare_action(self, player, list_of_enemies):
        self.next_action = self.attack_4
        self.list_incoming.append(declarationFile.Attack(4))

    def attack_4(self, player, list_of_enemies):
        self.deal_damage(4, player)


class SneakyGremlin(Enemy):
    def __init__(self, name="Sneaky Gremlin", health=random.randint(10, 14)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Sneaky Gremlin.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

    def declare_action(self, player, list_of_enemies):
        self.next_action = self.attack_9
        self.list_incoming.append(declarationFile.Attack(9))

    def attack_9(self, player, list_of_enemies):
        self.deal_damage(9, player)


class GremlinWizard(Enemy):
    def __init__(self, name="Gremlin Wizard", health=random.randint(23, 25)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Gremlin Wizard.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350
        self.charge_up_count = 0
        self.charge_up_required = 2

        self.list_of_actions = [self.attack_25, self.charge_up]

    def declare_action(self, player, list_of_enemies):
        if self.charge_up_count < self.charge_up_required:
            self.next_action = self.charge_up
            self.list_incoming.append(declarationFile.Unknown())
        else:
            self.next_action = self.attack_25
            self.charge_up_count = 0
            self.charge_up_required = 3
            self.list_incoming.append(declarationFile.Attack(25))

    def attack_25(self, player, list_of_enemies):
        self.deal_damage(25, player)

    def charge_up(self, player, list_of_enemies):
        self.charge_up_count += 1


class ShieldGremlin(Enemy):
    def __init__(self, name="Shield Gremlin", health=random.randint(12, 15)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Shield Gremlin.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350
        self.target = self

        self.list_of_actions = [self.add_armor_7, self.attack_6]

    def declare_action(self, player, list_of_enemies):
        if len(list_of_enemies) > 1:
            self.next_action = self.add_armor_7
        else:
            self.next_action = random.choice(self.list_of_actions)

        if self.next_action == self.add_armor_7:
            self.list_incoming.append(declarationFile.Block(7))
        elif self.next_action == self.attack_6:
            self.list_incoming.append(declarationFile.Attack(6))

    def choose_target(self, list_of_enemies):
        if len(list_of_enemies) > 1:
            self.target = random.choice([enemy for enemy in list_of_enemies if enemy is not self])
        else:
            self.target = self

    def add_armor_7(self, player, list_of_enemies):
        self.choose_target(list_of_enemies)
        self.add_block(7, self.target)

    def attack_6(self, player, list_of_enemies):
        self.deal_damage(6, player)


class Looter(Enemy):
    def __init__(self, name="Looter", health=random.randint(44, 48)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Looter.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.add_thievery(15, self)
        self.stolen_gold = 0

        self.turn_counter = 0
        self.has_lunged = False

    def deal_damage(self, damage, target, is_attack=True, hit_block=True):
        super().deal_damage(damage, target, is_attack, hit_block)
        if o.Effect.THIEVERY in self.dict_of_ongoing:
            target.coins -= self.dict_of_ongoing[o.Effect.THIEVERY].intensity
            self.stolen_gold += self.dict_of_ongoing[o.Effect.THIEVERY].intensity

    def declare_action(self, player, list_of_enemies):
        self.turn_counter += 1

        if self.turn_counter == 1 or self.turn_counter == 2:
            self.next_action = self.attack_10
        elif self.turn_counter == 3:
            self.next_action = random.choice([self.attack_12, self.gain_6_armor])
            if self.next_action == self.attack_12:
                self.has_lunged = True
        else:
            if self.has_lunged:
                self.next_action = self.gain_6_armor
                self.has_lunged = False
            else:
                self.next_action = self.escape

        if self.next_action == self.attack_10:
            self.list_incoming.append(declarationFile.Attack(10))
        elif self.next_action == self.attack_12:
            self.list_incoming.append(declarationFile.Attack(12))
        elif self.next_action == self.gain_6_armor:
            self.list_incoming.append(declarationFile.Block(6))
        elif self.next_action == self.escape:
            self.list_incoming.append(declarationFile.Escape())

    def attack_10(self, player, list_of_enemies):
        self.deal_damage(10, player)

    def attack_12(self, player, list_of_enemies):
        self.deal_damage(12, player)

    def gain_6_armor(self, player, list_of_enemies):
        self.add_block(6, self)

    def escape(self, player, list_of_enemies):
        list_of_enemies.remove(self)


class GremlinNob(Enemy):
    def __init__(self, name="Gremlin Nob", health=random.randint(82, 86)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Gremlin Nob.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.list_of_actions = [self.attack_14, self.attack_6_apply_3_vulnerable, self.gain_2_enrage]
        self.state = 0
        self.last_actions = []

    def declare_action(self, player, list_of_enemies):
        if self.state == 0:
            self.next_action = self.gain_2_enrage
            self.state = 1
        else:

            actions_weights = {
                self.attack_14: 67,
                self.attack_6_apply_3_vulnerable: 33
            }

            if len(self.last_actions) >= 2 and self.last_actions[-1] == self.last_actions[-2] and self.last_actions[
                -1] == self.attack_14:
                actions_weights[self.attack_14] = 0

            total_weight = sum(actions_weights.values())
            if total_weight == 0:
                self.next_action = self.attack_14 if self.last_actions[
                                                         -1] == self.attack_6_apply_3_vulnerable else self.attack_6_apply_3_vulnerable
            else:
                self.next_action = random.choices(
                    list(actions_weights.keys()), weights=list(actions_weights.values()), k=1)[0]

            self.last_actions.append(self.next_action)
            if len(self.last_actions) > 2:
                self.last_actions.pop(0)

    def attack_14(self, player, list_of_enemies):
        self.deal_damage(14, player)

    def attack_6_apply_3_vulnerable(self, player, list_of_enemies):
        self.deal_damage(6, player)
        self.add_vulnerable(3, player)

    def gain_2_enrage(self, player, list_of_enemies):
        self.add_enrage(2, self)


class Lagavulin(Enemy):
    def __init__(self, name="Legavulin", health=random.randint(109, 111)):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Lagavulin Asleep.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350

        self.add_metallicize(8, self)

        self.list_of_actions = [self.attack_18, self.lose_1_dex_1_str]
        self.state = 0
        self.sleep_count = 0
        self.attack_count = 0

    def declare_action(self, player, list_of_enemies):
        if self.sleep_count >= 3 or self.cur_health < self.max_health:
            self.state = 1
            self.image_sprite = pygame.image.load("../Sprites/Characters/Lagavulin Awake.png")
            self.add_metallicize(-8, self)

        if self.state == 0:
            self.next_action = self.sleep
            self.sleep_count += 1
        else:
            if self.attack_count < 2:
                self.next_action = self.attack_18
                self.attack_count += 1
            else:
                self.next_action = self.lose_1_dex_1_str
                self.attack_count = 0

    def attack_18(self, player, list_of_enemies):
        self.deal_damage(18, player)

    def lose_1_dex_1_str(self, player, list_of_enemies):
        self.add_strength(-1, player)
        self.add_dexterity(-1, player)

    def sleep(self, player, list_of_enemies):
        pass


class Sentry(Enemy):
    def __init__(self, name="Sentry", health=random.randint(38, 42), position=1):
        super().__init__(name, health)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.image_sprite = pygame.image.load("../Sprites/Characters/Sentry.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350
        self.position = position

        self.list_of_actions = [self.attack_9, self.shuffle_2_dazed]
        self.move_index = 0

        if self.position == 2:
            self.list_of_actions = [self.shuffle_2_dazed, self.attack_9]
        else:
            self.list_of_actions = [self.attack_9, self.shuffle_2_dazed]

    def declare_action(self, player, list_of_enemies):
        self.next_action = self.list_of_actions[self.move_index % len(self.list_of_actions)]
        self.move_index += 1

    def attack_9(self, player, list_of_enemies):
        self.deal_damage(9, player)

    def shuffle_2_dazed(self, player, list_of_enemies):
        player.add_card_to_discard(cardsFile.Dazed())
        player.add_card_to_discard(cardsFile.Dazed())

