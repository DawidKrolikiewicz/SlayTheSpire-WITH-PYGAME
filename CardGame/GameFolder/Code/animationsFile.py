# This is a lie, I can't do animations
import random
import pygame
from fontsFile import text_font_super_big


class Anim:
    def __init__(self, character, target, value):
        character.anim_list.append(self)
        self.target = target

        self.vertical = -10
        self.horizontal = random.randint(-6, 6)

        self.text_image = text_font_super_big.render(f"{value}", True, (255, 255, 255))
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = (self.target.rect_sprite.centerx + (random.randint(-75, 75)),
                                 self.target.rect_sprite.centery + (random.randint(-75, 75)))

        self.image = pygame.image.load("../Sprites/Characters/Don'tMakeInstancesOfBaseEnemyPLS.png")
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.center = self.text_rect.center

    def update(self, character, screen):
        if self.image.get_alpha() > 0:
            self.update_position()
            self.draw(screen)
        else:
            character.anim_list.remove(self)

    def update_position(self):
        if self.vertical < 10:
            self.vertical += 1

        self.rect.center = (self.rect.centerx + self.horizontal, self.rect.centery + self.vertical)
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        screen.blit(self.text_image, self.text_rect.topleft)
        self.image.set_alpha(self.image.get_alpha() - 5)
        self.text_image.set_alpha(self.text_image.get_alpha() - 5)


class DamageDealtAnim(Anim):
    def __init__(self, character, target, value):
        super().__init__(character, target, value)
        self.image = pygame.image.load("../Sprites/Misc/Star.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.text_rect.center


class BlockAddedAnim(Anim):
    def __init__(self, character, target, value):
        super().__init__(character, target, value)
        self.image = pygame.image.load("../Sprites/Misc/Shield.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.text_rect.center


class HealAnim(Anim):
    def __init__(self, character, target, value):
        super().__init__(character, target, value)
        self.image = pygame.image.load("../Sprites/Misc/Heal.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.text_rect.center




