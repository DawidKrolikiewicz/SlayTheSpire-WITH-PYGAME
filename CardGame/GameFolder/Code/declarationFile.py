import pygame
from fontsFile import text_font


class Declaration:
    def __init__(self, value):
        self.value = value
        self.value_image = text_font.render(f"{self.value}", True, (0, 0, 0))
        self.image = pygame.image.load("../Sprites/Misc/AttackIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Info about what this enemy intent!", True, (0, 0, 0))

    def update(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[2]:
            screen.blit(self.text, (900 - self.text.get_width() // 2, 0))


class Attack(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/AttackIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Enemy intends to attack for X damage", True, (0, 0, 0))


class MultiAttack(Declaration):
    def __init__(self, how_many, value):
        super().__init__(value)
        self.value_image = text_font.render(f"{how_many}x{value}", True, (0, 0, 0))
        self.image = pygame.image.load("../Sprites/Misc/AttackIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Enemy intends to attack multiple times for X damage", True, (0, 0, 0))


class Block(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/BlockIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Enemy intends to give block to ally or themselves", True, (0, 0, 0))


class Buff(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/BuffIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Enemy intends to inflict a positive effect on ally or themselves", True, (0, 0, 0))


class Debuff(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/DebuffIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Enemy intends to inflict a negative effect on the player", True, (0, 0, 0))


class SuperDebuff(Declaration):
    def __init__(self, value):
        super().__init__(value)
        self.image = pygame.image.load("../Sprites/Misc/SuperDebuffIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Enemy intends to inflict a major negative effect on the player", True, (0, 0, 0))


class Sleep(Declaration):
    def __init__(self):
        super().__init__(None)
        self.image = pygame.image.load("../Sprites/Misc/SleepIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Enemy is sleeping - but they might wake up", True, (0, 0, 0))


class Escape(Declaration):
    def __init__(self):
        super().__init__(None)
        self.image = pygame.image.load("../Sprites/Misc/EscapeIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Enemy intends to flee the battlefield", True, (0, 0, 0))


class Unknown(Declaration):
    def __init__(self):
        super().__init__(None)
        self.image = pygame.image.load("../Sprites/Misc/UnknownIntent.png")
        self.rect = self.image.get_rect()
        self.text = text_font.render("Enemy intends... something for sure...", True, (0, 0, 0))
