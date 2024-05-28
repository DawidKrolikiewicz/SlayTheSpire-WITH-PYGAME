import random
import pygame.sprite
import playerFile


# ======================= Ongoing Icons (superclass) =======================

class Ongoing(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # GAME RELATED
        self.counter = None
        self.intensity = None
        self.duration = None
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/StrengthIcon.png")
        self.rect = self.image.get_rect()
        self.rect.centery = 400

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        if ((self.counter is not None and self.counter > 0) or (self.duration is not None and self.duration > 0) or
                (self.intensity is not None and self.intensity != 0)):
            self.rect.topleft = character.rect_ongoing.topleft
            self.rect.right = character.rect_ongoing.right - (character.ongoing_counter * self.rect.width)
            character.ongoing_counter -= 1
            screen.blit(self.image, self.rect.topleft)


# ============================= Strength =============================

class Strength(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.intensity = 0
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/StrengthIcon.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        super().update(character, screen)


# ============================ Dexterity =============================

class Dexterity(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.intensity = 0
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/DexterityIcon.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        super().update(character, screen)


# ============================== Frail ===============================

class Frail(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.duration = 0
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/FrailIcon.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        super().update(character, screen)


# ============================ Vulnerable ============================

class Vulnerable(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.duration = 0
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/VulnerableIcon.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        super().update(character, screen)


# ============================ Juggernaut ============================

class JuggernautEffect(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.intensity = 5
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/JuggernautIcon.png")

    def event_listener(self, ev, player, list_of_enemies):
        if ev.type == playerFile.ON_PLAYER_GAIN_BLOCK:
            enemy = random.choice(list_of_enemies)
            enemy.cur_health -= self.intensity

    def update(self, character, screen):
        super().update(character, screen)

