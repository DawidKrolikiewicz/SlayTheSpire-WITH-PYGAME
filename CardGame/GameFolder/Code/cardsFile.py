import enum
import random
import pygame
import ongoingFile as o


def event_listener(ev, player, list_of_enemies, play_rect):
    # COMBAT ENCOUNTER EVENT LISTENER
    if player.current_room.__class__.__name__ == "CombatEncounter":
        pos = pygame.mouse.get_pos()
        if ev.type == pygame.MOUSEBUTTONDOWN and player.highlight is not None and player.drag is None:
            player.drag = player.highlight
            player.drag.image.set_alpha(200)
        if ev.type == pygame.MOUSEBUTTONUP and player.drag is not None:
            player.drag.image.set_alpha(255)
            if player.drag.target is Targeting.ANY:
                if play_rect.collidepoint(pos):
                    print(f"Playing {player.drag.name}!")
                    player.play_card(player, list_of_enemies, None, player.drag)
            elif player.drag.target is Targeting.ENEMY:
                for enemy in list_of_enemies:
                    if enemy.rect_sprite.collidepoint(pos):
                        print(f"Playing {player.drag.name} on {enemy.name}!")
                        player.play_card(player, list_of_enemies, enemy, player.drag)
            player.drag = None


# ====================== TARGETING =======================

class Targeting(enum.Enum):
    ANY = 1
    ENEMY = 2
    UNPLAYABLE = 3


# ====================== CARD TYPE =======================

class CardType(enum.Enum):
    ATTACK = 1
    SKILL = 2
    POWER = 3
    STATUS = 4
    CURSE = 5


# ======================= CardBase =======================
class CardBase(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # GAME RELATED
        self.name = self.__class__.__name__
        self.type = CardType.ATTACK
        self.target = Targeting.ANY
        self.cost = 99
        self.text = "There is no text here!"
        self.exhaust = False

        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Steroids.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (1366, 440)

        self.place = pygame.Vector2(0, 0)
        self.move_speed = 20

        self.reset_card_position()

        # SHOP RELATED
        self.price_range = (0, 0)
        self.weight = 0

    def update(self, screen, player, index, hand_rect):
        # COMBAT ENCOUNTER UPDATE
        if player.current_room.__class__.__name__ == "CombatEncounter":
            pos = pygame.mouse.get_pos()
            if player.drag == self:
                # Follow mouse
                self.rect.center = (pos[0], pos[1])
            else:
                # Move to default position based on index in hand
                self.place = pygame.Vector2(hand_rect.left + (index * 140), 600)
                current = pygame.Vector2(self.rect.center)
                current.move_towards_ip(self.place, self.move_speed)
                self.rect.center = current

            self.draw(screen)

        if player.current_room.__class__.__name__ == "Shop":
            spacing = (hand_rect.width - self.rect.width) / 3

            self.place = pygame.Vector2(
                hand_rect.left + (index + 0.335) * spacing,
                hand_rect.top + hand_rect.height / 3
            )
            current = pygame.Vector2(self.rect.center)
            current.move_towards_ip(self.place, self.move_speed)
            self.rect.center = current
            
            self.draw(screen)

        if player.current_room.__class__.__name__ == "Rewards":
            spacing = (hand_rect.width - self.rect.width) / 1.2

            self.place = pygame.Vector2(
                hand_rect.left + (index + 0.4) * spacing,
                hand_rect.top + hand_rect.height / 2.2
            )
            current = pygame.Vector2(self.rect.center)
            current.move_towards_ip(self.place, self.move_speed)
            self.rect.center = current

            self.draw(screen)

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 0, 0), self.rect)
        screen.blit(self.image, self.rect.topleft)

    def action(self, player, list_of_enemies, target):
        print(f"CardBase action executing!")

    def reset_card_position(self):
        self.rect.center = (1500, 600)


# ======================================== CARDS FROM HIT GAME SLAY THE SPIRE ======================================== #
# ==================================================================================================================== #

# ===================================================== STARTER ====================================================== #
# ==================================================================================================================== #

class Strike(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Strike.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(6, target)


# ==================================================================================================================== #

class Defend(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.SKILL
        self.target = Targeting.ANY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Defend.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.add_block(5, player)


# ==================================================================================================================== #

class Bash(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 2
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Bash.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(8, target)
        player.add_vulnerable(2, target)


# ===================================================== COMMONS ====================================================== #
# ==================================================================================================================== #

class Anger(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 0
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Anger.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(6, target)
        player.add_card_to_discard(Anger())


# ==================================================================================================================== #

class Armements(CardBase):
    # UPGRADE A CARD IN HAND FOR THE REST OF COMBAT (Upgrade for EVERY card needed and then some ._.)
    pass


# ==================================================================================================================== #

class BodySlam(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/BodySlam.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(player.block, target)


# ==================================================================================================================== #

class Clash(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 0
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Clash.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def update(self, screen, player, index, hand_rect):
        super().update(screen, player, index, hand_rect)
        if all(card.type == CardType.ATTACK for card in player.hand):
            self.target = Targeting.ENEMY
        else:
            self.target = Targeting.UNPLAYABLE

    def action(self, player, list_of_enemies, target):
        player.deal_damage(14, target)


# ==================================================================================================================== #

class Cleave(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ANY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Cleave.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        for enemy in list_of_enemies:
            player.deal_damage(8, enemy)


# ==================================================================================================================== #

class Clothesline(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 2
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Clothesline.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(12, target)
        player.add_weak(2, target)


# ==================================================================================================================== #

class Flex(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.SKILL
        self.target = Targeting.ANY
        self.cost = 0
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Flex.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.add_strength(2, player)
        player.add_strength_down(2, player)


# ==================================================================================================================== #

class Havoc(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.SKILL
        self.target = Targeting.ANY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Havoc.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        card = player.draw_card(1)
        card.exhaust = True
        player.play_card(player, list_of_enemies, random.choice(list_of_enemies), card, use_mana=False)
        print(card.name)


# ==================================================================================================================== #

class Headbutt(CardBase):
    # PUT A CARD FROM YOUR DISCARD PILE ON TOP OF YOUR DRAW PILE (Deck browsing needed)
    pass


# ==================================================================================================================== #

class HeavyBlade(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 2
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/HeavyBlade.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        damage = 14
        if o.Effect.STRENGTH in player.dict_of_ongoing:
            damage += (player.dict_of_ongoing[o.Effect.STRENGTH].intensity * 2)

        player.deal_damage(damage, target)


# ==================================================================================================================== #

class IronWave(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/IronWave.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(5, target)
        player.add_block(5, player)


# ==================================================================================================================== #

class PommelStrike(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/PommelStrike.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(9, target)
        player.draw_card(1)


# ==================================================================================================================== #

class ShrugItOff(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.SKILL
        self.target = Targeting.ANY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/ShrugItOff.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.add_block(8, player)
        player.draw_card(1)


# ==================================================================================================================== #

class SwordBoomerang(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ANY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/SwordBoomerang.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        for i in range(3):
            player.deal_damage(3, random.choice(list_of_enemies))


# ==================================================================================================================== #

class Thunderclap(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ANY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Thunderclap.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        for enemy in list_of_enemies:
            player.deal_damage(4, enemy)
            player.add_vulnerable(1, enemy)


# ==================================================================================================================== #

class TrueGrit(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.SKILL
        self.target = Targeting.ANY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/TrueGrit.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.add_block(7, player)
        card = random.choice(player.hand)
        player.exhaust_card(card)


# ==================================================================================================================== #

class TwinStrike(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/TwinStrike.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        for i in range(2):
            player.deal_damage(5, target)


# ==================================================================================================================== #

class Warcry(CardBase):
    # PUT A CARD FROM YOUR HAND ON TOP OF YOUR DRAW PILE (Hand Browsing needed)
    pass


# ==================================================================================================================== #

class WildStrike(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.ATTACK
        self.target = Targeting.ENEMY
        self.cost = 1
        self.text = "There is no text here!"
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/WildStrike.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(12, target)
        player.add_card_to_deck(Wound())

# ==================================================== UNCOMMONS ===================================================== #
# ==================================================================================================================== #


# ====================================================== RARES ======================================================= #
# ==================================================================================================================== #

class Juggernaut(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.POWER
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Juggernaut.png")
        # SHOP RELATED
        self.price_range = (99, 99)
        self.weight = 0

    def action(self, player, list_of_enemies, target):
        player.add_juggernaut(5, player)


# ====================================================== STATUS ====================================================== #
# ==================================================================================================================== #

class Wound(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.type = CardType.STATUS
        self.cost = 99
        self.text = "There is no text here!"
        self.target = Targeting.UNPLAYABLE
        self.exhaust = False
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Wound.png")
        # SHOP RELATED
        self.price_range = (99, 99)
        self.weight = 0


# ============================================ MEME TESTING CARDS AREA :) ============================================ #
# ==================================================================================================================== #

class Covid19Vaccine(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 2
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Covid19Vaccine.png")
        # SHOP RELATED
        self.price_range = (30, 40)
        self.weight = 1

    def action(self, player, list_of_enemies, target):
        player.heal(3, player)
        player.draw_card(2)


# ==========================================================================

class Bonk(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ENEMY
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Bonk.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.deal_damage(6, target)


# ==========================================================================

class PanicRoll(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/PanicRoll.png")
        # SHOP RELATED
        self.price_range = (18, 25)
        self.weight = 2

    def action(self, player, list_of_enemies, target):
        player.draw_card(1)


# ==========================================================================

class TinCanArmor(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/TinCanArmor.png")
        # SHOP RELATED
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies, target):
        player.add_block(4, player)


# ==========================================================================

class A100pNatural(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 2
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/100%Natural.png")
        # SHOP RELATED
        self.price_range = (25, 35)
        self.weight = 1

    def action(self, player, list_of_enemies, target):
        player.add_dexterity(1, player)
        player.add_strength(1, player)


# ==========================================================================

class Covid19(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ENEMY
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Covid19.png")
        # SHOP RELATED
        self.price_range = (18, 25)
        self.weight = 2

    def action(self, player, list_of_enemies, target):
        player.add_frail(1, target)
        player.add_vulnerable(1, target)


# ==========================================================================

class Depression(CardBase):
    def __init__(self):
        super().__init__()
        # GAME RELATED
        self.cost = 1
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        # VISUAL RELATED
        self.image = pygame.image.load("../Sprites/Cards/Depression.png")
        # SHOP RELATED
        self.price_range = (99, 99)
        self.weight = 0

    def action(self, player, list_of_enemies, target):
        player.deal_damage(5, player)


# ==========================================================================

class Ritual(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 3
        self.text = "There is no text here!"
        self.target = Targeting.ANY
        self.image = pygame.image.load("../Sprites/Cards/Steroids.png")

    def action(self, player, list_of_enemies, target):
        player.deal_damage(3, list_of_enemies[0])
        player.add_strength(3, player)


# ==========================================================================

class Fireball(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 3
        self.text = "There is no text here!"
        self.target = Targeting.ENEMY
        self.image = pygame.image.load("../Sprites/Cards/NotSoGentlePush.png")

    def action(self, player, list_of_enemies, target):
        player.deal_damage(20, target)


# ==========================================================================