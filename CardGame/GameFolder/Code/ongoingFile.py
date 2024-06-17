import random
import pygame.sprite
import playerFile
import characterFile
import enum
from fontsFile import text_font


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
    BARRICADE = 20
    BERSERK = 21
    BRUTALITY = 22
    CORRUPTION = 23
    DEMON_FORM = 24
    DOUBLE_TAP = 25
    # ENEMY 2
    ENTANGLED = 26
    ANGRY = 27
    SPORE_CLOUD = 28
    THIEVERY = 29
    ENRAGE = 30
    MADNESS = 31


# ======================= Ongoing Icons (superclass) =======================

class Ongoing(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # GAME RELATED
        self.counter = None
        self.intensity = None
        self.duration = None
        self.no_stack = False
        self.value = None
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/StrengthIcon.png")
        self.image_value = None
        self.rect = self.image.get_rect()
        self.rect.centery = 400
        self.text = text_font.render("Info about what this ongoing effect does!", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        if self.value is not None and self.value != 0:
            self.rect.topleft = character.rect_ongoing.topleft
            self.rect.right = character.rect_ongoing.right - (character.counter * self.rect.width)
            character.counter -= 1
            screen.blit(self.image, self.rect.topleft)
            if self.no_stack is False:
                self.image_value = characterFile.text_font.render(f"{self.value}", True, (0, 0, 0))
                screen.blit(self.image_value, self.rect.topleft)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[2]:
            screen.blit(self.text, (900 - self.text.get_width() // 2, 0))


# ============================= Strength =============================

class Strength(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/StrengthIcon.png")
        self.text = text_font.render("Attacks deal X more damage", True, (0, 0, 0))

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
        self.text = text_font.render("Gain X extra block whenever you gain block", True, (0, 0, 0))

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
        self.text = text_font.render("Gain 25% less block for X turns", True, (0, 0, 0))

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
        self.text = text_font.render("Take 50% damage for X turns", True, (0, 0, 0))

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
        self.text = text_font.render("Deal 25% less damage for X turns", True, (0, 0, 0))

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
        self.text = text_font.render("Gain X strength at the end of turns", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
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
        self.text = text_font.render("Taking damage for the first time gives X block", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)

    def action(self, character):
        character.add_block(self.intensity, character)
        character.dict_of_ongoing[Effect.CURLUP].intensity = 0


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
        self.text = text_font.render("Gaining block deal X damage", True, (0, 0, 0))

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
        self.text = text_font.render("At the end of the turn, lose X strength", True, (0, 0, 0))

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
        self.text = text_font.render("Can't draw cards until the end of the turn", True, (0, 0, 0))

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
        self.text = text_font.render("Lose X/5 hp and deal X damage to enemies at the end of turns", True, (0, 0, 0))

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
        self.text = text_font.render("When you exhaust a card, draw X", True, (0, 0, 0))

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
        self.text = text_font.render("Whenever you draw status card, draw X", True, (0, 0, 0))

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
        self.text = text_font.render("Whenever you exhaust a card, gain X block", True, (0, 0, 0))

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
        self.text = text_font.render("Whenever you draw status or curse, deal X damage to enemies", True, (0, 0, 0))

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
        self.text = text_font.render("Whenever you take damage this turn, deal X damage back", True, (0, 0, 0))

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
        self.text = text_font.render("Gain X block at the end of turns", True, (0, 0, 0))

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
        self.text = text_font.render("Whenever you play an attack this turn, gain X block", True, (0, 0, 0))

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
        self.text = text_font.render("Whenever you lose hp from a card, gain X strength", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_PLAYER_LOSE_HP_FROM_CARD:
            player.add_strength(self.intensity, player)

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================= Barricade ============================

class Barricade(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.no_stack = True
        self.value = 1
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/BarricadeIcon.png")
        self.text = text_font.render("Don't lose block at the start of turns", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = 1
        super().update(character, screen)


# ============================== Berserk =============================

class Berserk(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/BerserkIcon.png")
        self.text = text_font.render("Gain X mana at the start of your turns", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================= Brutality ============================

class Brutality(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/BrutalityIcon.png")
        self.text = text_font.render("Lose X health and draw X cards at the start of turns", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================= Corruption ============================

class Corruption(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.no_stack = True
        self.value = 1
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/CorruptionIcon.png")
        self.text = text_font.render("Skill cost 0 and exhaust when played", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = 1
        super().update(character, screen)


# ============================= Demon Form ============================

class DemonForm(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/DemonFormIcon.png")
        self.text = text_font.render("Gain X strength at the start of turns", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


# ============================= Double Tap ============================

class DoubleTap(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.counter = value
        self.value = self.counter
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/DoubleTapIcon.png")
        self.text = text_font.render("Next attack is played twice", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        if ev.type == playerFile.ON_TURN_END:
            self.counter = 0
        pass

    def update(self, character, screen):
        self.value = self.counter
        super().update(character, screen)


class Entangled(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.duration = value
        self.value = self.duration
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/EntangledIcon.png")
        self.text = text_font.render("You can't play attacks for X turns", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.duration
        super().update(character, screen)


class Angry(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/RageIcon.png")
        self.text = text_font.render("On damage taken, gain X strength", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)

    def action(self, character):
        character.add_strength(self.intensity, character)


class SporeCloud(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/SporeCloudIcon.png")
        self.text = text_font.render("On death, make opponent Vulnurable for X turns", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


class Thievery(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/ThieveryIcon.png")
        self.text = text_font.render("On damage dealt, steals X gold", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


class Enrage(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/RageIcon.png")
        self.text = text_font.render("Whenever skill is played, gain X strength", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)


class Madness(Ongoing):
    def __init__(self, value=0):
        super().__init__()
        # GAME RELATED
        self.intensity = value
        self.value = self.intensity
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Ongoing Icons/MadnessIcon.png")
        self.text = text_font.render("Whenever card is played, gain X strength and dexterity but lose them when used", True, (0, 0, 0))

    def event_listener(self, ev, character, player, list_of_enemies):
        pass

    def update(self, character, screen):
        self.value = self.intensity
        super().update(character, screen)