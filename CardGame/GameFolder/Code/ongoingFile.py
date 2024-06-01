import random
import pygame.sprite
import playerFile
import characterFile
import enum


class Effect(enum.Enum):
    # CORE
    STRENGTH = 1
    DEXTERITY = 2
    FRAIL = 3
    VULNERABLE = 4
    WEAK = 5
    # ENEMY
    RITUAL = 6
    CURLUP = 7
    # UNIQUE CARD EFFECTS
    JUGGERNAUT = 8
    STRENGTH_DOWN = 9
    NO_DRAW = 10
    COMBUST = 11
    DARK_EMBRACE = 12
    EVOLVE = 13
    FEEL_NO_PAIN = 14
    FIRE_BREATHING = 15
    FLAME_BARRIER = 16
    METALLICIZE = 17
    RAGE = 18
    RUPTURE = 19



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

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        if self.value is not None and self.value != 0:
            self.rect.topleft = character.rect_ongoing.topleft
            self.rect.right = character.rect_ongoing.right - (character.counter * self.rect.width)
            character.counter -= 1
            screen.blit(self.image, self.rect.topleft)
            self.image_value = characterFile.text_font.render(f"{self.value}", True, (0, 0, 0))
            screen.blit(self.image_value, self.rect.topleft)


# ============================= Strength =============================

class Strength(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/StrengthIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================ Dexterity =============================

class Dexterity(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/DexterityIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================== Frail ===============================

class Frail(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.duration = value
        self.value = self.duration
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/FrailIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.duration
        super().update(character, screen)


# ============================ Vulnerable ============================

class Vulnerable(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.duration = value
        self.value = self.duration
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/VulnerableIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.duration
        super().update(character, screen)


# =============================== Weak ===============================

class Weak(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.duration = value
        self.value = self.duration
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/WeakIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.duration
        super().update(character, screen)


# /////////////////////////// ENEMY EFFECTS ///////////////////////////

# ============================== Ritual ==============================

class Ritual(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/RitualIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_TURN_END:
            character.add_strength(self.intensity, character)
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================== CurlUp ==============================

class CurlUp(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/CurlUpIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)

    def action(self, character):
        character.add_block(self.intensity, character)
        character.dict_of_ongoing[Effect.CURLUP] = 0


# /////////////////////////// CARDS EFFECTS ///////////////////////////

# ============================ Juggernaut ============================

class Juggernaut(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/JuggernautIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_PLAYER_GAIN_BLOCK:
            enemy = random.choice(list_of_enemies)
            player.deal_damage(self.intensity, enemy, is_attack=False)

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# =========================== Strength Down ==========================

class StrengthDown(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/StrengthDownIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_TURN_END:
            if Effect.STRENGTH in character.dict_of_ongoing:
                character.dict_of_ongoing[Effect.STRENGTH].intensity -= self.intensity
                character.dict_of_ongoing[Effect.STRENGTH_DOWN].intensity = 0

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)
        pass


# ============================== No Draw =============================

class NoDraw(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.duration = value
        self.value = self.duration
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/NoDrawIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.duration
        super().update(character, screen)
        if self.duration > 1:
            self.duration = 1


# ============================== Combust =============================

class Combust(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/CombustIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_TURN_END:
            character.deal_damage(self.intensity // 5, character, is_attack=False, hit_block=False)
            for enemy in list_of_enemies:
                character.deal_damage(self.intensity, enemy)

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# =========================== Dark Embrace ===========================

class DarkEmbrace(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/DarkEmbraceIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_CARD_EXHAUSTED:
            player.draw_card(self.intensity)

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# =============================== Evolve =============================

class Evolve(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/EvolveIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_STATUS_CARD_DRAWN:
            player.draw_card(self.intensity)

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# =========================== Feel No Pain ===========================

class FeelNoPain(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/FeelNoPainIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_STATUS_CARD_DRAWN:
            player.add_block(self.intensity)

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ========================== Fire Breathing ==========================

class FireBreathing(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/FireBreathingIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_STATUS_CARD_DRAWN or ev.type == playerFile.ON_CURSE_CARD_DRAWN:
            for enemy in list_of_enemies:
                character.deal_damage(self.intensity, enemy)

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# =========================== Flame Barrier ==========================

class FlameBarrier(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/FlameBarrierIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_TURN_END:
            self.intensity = 0
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================ Metallicize ===========================

class Metallicize(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/MetallicizeIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        # EVENT DOESN'T PROCESS BETWEEN PLAYER ENDING TURN AND ENEMY STARTING THEIR ATTACK SO :^)
        # It's in Player.end_turn()
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# =============================== Rage ===============================

class Rage(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/RageIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_ATTACK_PLAYED:
            player.add_block(self.intensity, player)
        if ev.type == playerFile.ON_TURN_END:
            self.intensity = 0

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================== Rupture =============================

class Rupture(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/RuptureIcon.png")

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_PLAYER_LOSE_HP_FROM_CARD:
            player.add_strength(self.intensity, player)

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)
