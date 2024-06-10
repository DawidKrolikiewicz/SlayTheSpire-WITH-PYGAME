import pygame
from fontsFile import text_font


class Declaration:
    def __init__(self, value):
        self.value = value
        self.value_image = text_font.render(f"{self.value}", True, (0, 0, 0))
        self.image = pygame.image.load("../Sprites/Misc/AttackIntent.png")
        self.rect = self.image.get_rect()


class Attack(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/AttackIntent.png")
        self.rect = self.image.get_rect()


class MultiAttack(Declaration):
    def __init__(self, how_many, value):
        super().__init__(value)
        self.value_image = text_font.render(f"{how_many}x{value}", True, (0, 0, 0))
        self.image = pygame.image.load("../Sprites/Misc/AttackIntent.png")
        self.rect = self.image.get_rect()


class Block(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/BlockIntent.png")
        self.rect = self.image.get_rect()


class Buff(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/BuffIntent.png")
        self.rect = self.image.get_rect()


class Debuff(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/DebuffIntent.png")
        self.rect = self.image.get_rect()


class SuperDebuff(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/SuperDebuffIntent.png")
        self.rect = self.image.get_rect()


class Sleep(Declaration):
    def __init__(self):
        super().__init__(None)
        self.image = pygame.image.load("../Sprites/Misc/SleepIntent.png")
        self.rect = self.image.get_rect()


class Escape(Declaration):
    def __init__(self):
        super().__init__(None)
        self.image = pygame.image.load("../Sprites/Misc/EscapeIntent.png")
        self.rect = self.image.get_rect()


class Unknown(Declaration):
    def __init__(self):
        super().__init__(None)
        self.image = pygame.image.load("../Sprites/Misc/UnknownIntent.png")
        self.rect = self.image.get_rect()
