import random
import pygame.sprite
import playerFile
import characterFile


# ======================= Ongoing Icons (superclass) =======================

class Ongoing(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # GAME RELATED
        self.counter = None
        self.intensity = None
        self.duration = None
        self.value = None
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/StrengthIcon.png")
        self.image_value = None
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
            self.image_value = characterFile.text_font.render(f"{self.value}", True, (0, 0, 0))
            screen.blit(self.image_value, self.rect.topleft)


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
        self.value = self.intensity
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
        self.value = self.intensity
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
        self.value = self.duration
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
        self.value = self.duration
        super().update(character, screen)


# =============================== Weak ===============================

class Weak(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.duration = 0
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/WeakIcon.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.duration
        super().update(character, screen)


# /////////////////////////// ENEMY EFFECTS ///////////////////////////

# ============================== Ritual ==============================

class Ritual(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.intensity = 0
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/RitualIcon.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================== CurlUp ==============================

class CurlUp(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.intensity = 0
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/CurlUpIcon.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# /////////////////////////// CARDS EFFECTS ///////////////////////////

# ============================ Juggernaut ============================

class JuggernautEffect(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.intensity = 5
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/JuggernautIcon.png")

    def event_listener(self, ev, player, list_of_enemies):
        if ev.type == playerFile.ON_PLAYER_GAIN_BLOCK:
            enemy = random.choice(list_of_enemies)
            player.deal_damage(self.intensity, enemy, is_attack=False)

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


