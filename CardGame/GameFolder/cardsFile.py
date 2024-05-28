import random
import enum
import pygame
import ongoingFile


def event_listener(ev, player, list_of_enemies, play_rect):
    # COMBAT ENCOUNTER EVENT LISTENER
    if player.current_room.__class__.__name__ == "CombatEncounter":
        pos = pygame.mouse.get_pos()
        if ev.type == pygame.MOUSEBUTTONDOWN and player.highlight is not None and player.drag is None:
            player.drag = player.highlight
            player.drag.image.set_alpha(200)
        if ev.type == pygame.MOUSEBUTTONUP and player.drag is not None:
            player.drag.image.set_alpha(255)
            if player.drag.target is Targeting.ANY:
                if play_rect.collidepoint(pos):
                    print(f"Playing {player.drag.name}!")
                    player.play_card(player, list_of_enemies, None, player.drag)
            elif player.drag.target is Targeting.ENEMY:
                for enemy in list_of_enemies:
                    if enemy.rect_sprite.collidepoint(pos):
                        print(f"Playing {player.drag.name} on {enemy.name}!")
                        player.play_card(player, list_of_enemies, enemy, player.drag)
            player.drag = None


# ====================== TARGETING =======================

class Targeting(enum.Enum):
    ANY = 1
    ENEMY = 2


# ====================== CARD TYPE =======================

class CardType(enum.Enum):
    ATTACK = 1
    SKILL = 2
    POWER = 3
    STATUS = 4
    CURSE = 5


# ======================= CardBase =======================
class CardBase(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # GAME RELATED
        self.name = self.__class__.__name__
        self.type = CardType.ATTACK
        self.cost = 99
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        self.exhaust = False

        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Steroids.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (1366, 440)

        self.place = pygame.Vector2(0, 0)
        self.move_speed = 20

        self.reset_card_position()

        # SHOP RELATED
        self.price_range = (0, 0)
        self.weight = 0

    def update(self, screen, player, index, hand_rect):
        # COMBAT ENCOUNTER UPDATE
        if player.current_room.__class__.__name__ == "CombatEncounter":
            pos = pygame.mouse.get_pos()
            if player.drag == self:
                # Follow mouse
                self.rect.center = (pos[0], pos[1])
            else:
                # Move to default position based on index in hand
                self.place = pygame.Vector2(hand_rect.left + (index * 140), 600)
                current = pygame.Vector2(self.rect.center)
                current.move_towards_ip(self.place, self.move_speed)
                self.rect.center = current

            self.draw(screen)

        if  player.current_room.__class__.__name__ == "Shop":
            pos = pygame.mouse.get_pos()
            if player.drag == self:
                # Follow mouse
                self.rect.center = (pos[0], pos[1])
            else:
                # Move to default position based on index in hand
                self.place = pygame.Vector2(hand_rect.left + (index * 140), 600)
                current = pygame.Vector2(self.rect.center)
                current.move_towards_ip(self.place, self.move_speed)
                self.rect.center = current

            self.draw(screen)


    def draw(self, screen):
        #pygame.draw.rect(screen, (255, 0, 0), self.rect)
        screen.blit(self.image, self.rect.topleft)

    def action(self, player, list_of_enemies, target):
        print(f"CardBase action executing!")

    def reset_card_position(self):
        self.rect.center = (1500, 600)


# ======================= Card1 =======================

class Draw2Heal3(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 2
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Covid19Vaccine.png")
        # SHOP RELATED
        self.price_range = (30, 40)
        self.weight = 1

    def action(self, player, list_of_enemies, target):
        player.heal(3, player)
        player.draw_card(2)


# ======================= Card2 =======================

class Deal5Damage(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ENEMY
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/GentlePush.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(5, target)


# ======================= Card3 =======================

class Draw1(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/PanicRoll.png")
        # SHOP RELATED
        self.price_range = (18, 25)
        self.weight = 2

    def action(self, player, list_of_enemies, target):
        player.draw_card(1)


# ======================= Card4 =======================

class Armor4(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/TinCanArmor.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.add_armor(4, player)


# ======================= Card5 =======================

class Buff(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 2
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/LevelUp.png")
        # SHOP RELATED
        self.price_range = (25, 35)
        self.weight = 1

    def action(self, player, list_of_enemies, target):
        player.add_dex(1, player)
        player.add_str(1, player)


# ======================= Card6 =======================

class Debuff(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ENEMY
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Covid19.png")
        # SHOP RELATED
        self.price_range = (18, 25)
        self.weight = 2

    def action(self, player, list_of_enemies, target):
        player.add_frai(1, target)
        player.add_vuln(1, target)


# ======================= Card6 =======================

class Depression(CardBase):  # UNPLAYABLE
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 9
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Depression.png")
        # SHOP RELATED
        self.price_range = (99, 99)
        self.weight = 0

    def action(self, player, list_of_enemies, target):
        player.deal_damage(5, player)

# ======================= Card7 =======================


class Juggernaut(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.POWER
        self.cost = 1
        self.text = "There is no text here!"
        self.text = Targeting.ANY
        self.exhaust = False
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/juggernaut (1).png")
        # SHOP RELATED
        self.price_range = (99, 99)
        self.weight = 0

    def action(self, player, list_of_enemies, target):
        for ongoing in player.list_of_ongoing:
            if isinstance(ongoing, ongoingFile.JuggernautEffect):
                ongoing.intensity += 5
                return
        player.list_of_ongoing.append(ongoingFile.JuggernautEffect())


class Ritual(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 3
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        self.image = pygame.image.load("Cards/Steroids.png")

    def action(self, player, list_of_enemies, target):
        player.deal_damage(3, list_of_enemies[0])
        player.add_str(3, player)


class Fireball(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 3
        self.text = "There is no text here!"
        self.target = Targeting.ENEMY
        self.image = pygame.image.load("Cards/NotSoGentlePush.png")

    def action(self, player, list_of_enemies, target):
        player.deal_damage(20, target)

