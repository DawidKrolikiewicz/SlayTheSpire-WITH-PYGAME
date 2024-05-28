import pygame.sprite


# ======================= Ongoing (superclass) =======================

class Ongoing(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # GAME RELATED
        self.counter = None
        self.intensity = None
        self.duration = None
        # VISUAL RELATED
        self.image = pygame.image.load("Ongoing/Ongoing.png")
        self.rect = self.image.get_rect()
        self.rect.centery = 400

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.rect.center = (400, 400)
        screen.blit(self.image, self.rect.topleft)


# ============================= Strength =============================

class Strength(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.intensity = 0
        # VISUAL RELATED
        self.image = pygame.image.load("Ongoing/Strength.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        #super().update(screen)
        self.rect.center = (character.rect_sprite.centerx - 45, self.rect.centery)
        screen.blit(self.image, self.rect.topleft)


# ============================ Dexterity =============================

class Dexterity(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.intensity = 0
        # VISUAL RELATED
        self.image = pygame.image.load("Ongoing/Dexterity.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        #super().update(screen)
        self.rect.center = (character.rect_sprite.centerx - 15, self.rect.centery)
        screen.blit(self.image, self.rect.topleft)


# ============================== Frail ===============================

class Frail(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.duration = 0
        # VISUAL RELATED
        self.image = pygame.image.load("Ongoing/Frail.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        #super().update(screen)
        self.rect.center = (character.rect_sprite.centerx + 15, self.rect.centery)
        screen.blit(self.image, self.rect.topleft)


# ============================ Vulnerable ============================

class Vulnerable(Ongoing):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.duration = 0
        # VISUAL RELATED
        self.image = pygame.image.load("Ongoing/Vulnurable.png")

    def event_listener(self, ev, player, list_of_enemies):
        pass

    def update(self, character, screen):
        #super().update(screen)
        self.rect.center = (character.rect_sprite.centerx + 45, self.rect.centery)
        screen.blit(self.image, self.rect.topleft)








