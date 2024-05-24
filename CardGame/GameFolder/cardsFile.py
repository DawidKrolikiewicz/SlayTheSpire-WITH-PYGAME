import random
import enum
import pygame


# ====================== TARGETING =======================
class Targeting(enum.Enum):
    ANY = 1
    ENEMY = 2
    PLAYER = 3


# ======================= CardBase =======================
class CardBase(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # GAME RELATED
        self.name = self.__class__.__name__
        self.cost = 99
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Steroids.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(0, 1366)
        self.y = random.randint(528, 768)
        self.move_speed = 0
        self.move_x = self.move_speed
        self.move_y = self.move_speed
        self.rect = pygame.Rect((0, 0, self.width, self.height))
        self.rect.center = (self.x, self.y)
        # SHOP RELATED
        self.price_range = (0, 0)
        self.weight = 0

    def event_listener(self, ev, player, list_of_enemies, play_rect):
        pos = pygame.mouse.get_pos()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pos) and player.drag is None:
                print(self.name)
                player.drag = self
                player.drag.image.set_alpha(200)
        if ev.type == pygame.MOUSEBUTTONUP and player.drag is not None:
            player.drag.image.set_alpha(255)
            print(player.drag.target)
            if player.drag.target is Targeting.ANY:
                if play_rect.collidepoint(pos):
                    print(f"Playing {player.drag.name}!")
                    player.play_card(player, list_of_enemies, None, player.drag)
            elif player.drag.target is Targeting.ENEMY:
                for enemy in list_of_enemies:
                    if enemy.rect.collidepoint(pos):
                        print(f"Playing {player.drag.name} on {enemy.name}!")
                        player.play_card(player, list_of_enemies, enemy, player.drag)
            player.drag = None

    def update(self, screen, player, hand_rect):
        # Bouncing around screen-saver style
        if self.rect.centery <= hand_rect.top:
            self.move_y = self.move_speed
        if self.rect.bottom >= hand_rect.bottom:
            self.move_y = -self.move_speed
        if self.rect.centerx <= hand_rect.left:
            self.move_x = self.move_speed
        if self.rect.centerx >= hand_rect.right:
            self.move_x = -self.move_speed

        if player.drag == self:
            pos = pygame.mouse.get_pos()
            self.x = pos[0]
            self.y = pos[1]
        else:
            self.x = self.x + self.move_x
            self.y = self.y + self.move_y

        self.rect.center = (self.x, self.y)

        self.draw(screen)

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 0, 0), self.rect)
        screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))

    def action(self, player, list_of_enemies, target):
        print(f"CardBase action executing!")


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
        self.image = pygame.image.load("Cards/Steroids.png")
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
        player.add_frag(1, target)
        player.add_vuln(1, target)


# ======================= Card6 =======================

class Depression(CardBase):  # Testing purposes card
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Depression.png")
        # SHOP RELATED
        self.price_range = (99, 99)
        self.weight = 0

    def action(self, player, list_of_enemies, target):
        player.deal_damage(5, player)


