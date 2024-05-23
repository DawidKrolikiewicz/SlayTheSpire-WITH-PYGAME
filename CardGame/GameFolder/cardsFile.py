import random
import pygame


# ======================= CardBase =======================
class CardBase(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # GAME RELATED
        self.name = self.__class__.__name__
        self.cost = 99
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.x = random.randint(0, 1116)
        self.y = random.randint(0, 443)
        self.move_speed = 2
        self.move_x = self.move_speed
        self.move_y = self.move_speed
        self.image = pygame.image.load("Cards/Steroids.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))
        # SHOP RELATED
        self.price_range = (0, 0)
        self.weight = 0

    def event_listener(self, ev, player):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) and player.drag is None:
                print(self.name)
                player.drag = self
        if ev.type == pygame.MOUSEBUTTONUP and player.drag is not None:
            player.drag = None

    def update(self, screen, player):
        # Bouncing around screen-saver style
        if self.rect.top <= 0:
            self.move_y = self.move_speed
        if self.rect.bottom >= screen.get_height():
            self.move_y = -self.move_speed
        if self.rect.left <= 0:
            self.move_x = self.move_speed
        if self.rect.right >= screen.get_width():
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

    def action(self, player, list_of_enemies):
        print(f"CardBase action executing!")


# ======================= Card1 =======================

class Draw2Heal3(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 2
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Covid19Vaccine.png")
        # SHOP RELATED
        self.price_range = (30, 40)
        self.weight = 1

    def action(self, player, list_of_enemies):
        player.heal(3, player)
        player.draw_card(2)


# ======================= Card2 =======================

class Deal5Damage(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/GentlePush.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies):
        # TEMP SOLUTION: ALWAYS TARGETS FIRST ENEMY RN (Should be able to choose in future)
        player.deal_damage(5, list_of_enemies[0])


# ======================= Card3 =======================

class Draw1(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/PanicRoll.png")
        # SHOP RELATED
        self.price_range = (18, 25)
        self.weight = 2

    def action(self, player, list_of_enemies):
        player.draw_card(1)


# ======================= Card4 =======================

class Armor4(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/TinCanArmor.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies):
        player.add_armor(4, player)


# ======================= Card5 =======================

class Buff(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 2
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Steroids.png")
        # SHOP RELATED
        self.price_range = (25, 35)
        self.weight = 1

    def action(self, player, list_of_enemies):
        player.add_dex(1, player)
        player.add_str(1, player)


# ======================= Card6 =======================

class Debuff(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Covid19.png")
        # SHOP RELATED
        self.price_range = (18, 25)
        self.weight = 2

    def action(self, player, list_of_enemies):
        # TEMP SOLUTION: ALWAYS TARGETS FIRST ENEMY RN (Should be able to choose in future)
        player.add_frag(1, list_of_enemies[0])
        player.add_vuln(1, list_of_enemies[0])


# ======================= Card6 =======================

class Depression(CardBase):  # Testing purposes card
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("Cards/Depression.png")
        # SHOP RELATED
        self.price_range = (99, 99)
        self.weight = 0

    def action(self, player, list_of_enemies):
        player.deal_damage(5, player)


