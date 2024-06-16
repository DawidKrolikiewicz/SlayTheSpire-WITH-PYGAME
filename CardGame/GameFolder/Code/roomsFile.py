import pygame
import random
import enemyFile
import cardsFile
from fontsFile import text_font, text_font_big, text_font_bigger
import inspect
import enum
import ongoingFile as o
import time
import playerFile

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (150, 0, 250)
GOLD = (219, 172, 52)

SLIDER_WIDTH = 20
SLIDER_HEIGHT = 668
SLIDER_X = 588
SLIDER_Y = 50


# > Room   (superclass)
# - Menu
# > InGame (superclass)
# - CombatEncounter
# - Shop


class RewardsLevel(enum.Enum):
    NO_REWARDS = 1
    EASY_FIGHT = 2
    NORMAL_FIGHT = 3
    ELITE_FIGHT = 4


class CombatDifficulty(enum.Enum):
    EASY = 1
    NORMAL = 2
    ELITE = 3
    BOSS = 4


def multi_text_render(text, screen):
    rendered_fonts = []
    for i, line in enumerate(text.split('\n')):
        txt_surf = text_font.render(line, True, (255, 255, 255))
        txt_rect = txt_surf.get_rect()
        txt_rect.topleft = (600, 240 + i * 24)
        rendered_fonts.append((txt_surf, txt_rect))
    for txt_surf, txt_rect in rendered_fonts:
        screen.blit(txt_surf, txt_rect)


def button_caption(text, rect, screen):
    rend_text = text_font.render(text, True,
                                 (0, 0, 0))
    rect_text = rend_text.get_rect()
    outline = pygame.rect.Rect(0, 0, rect_text.width + 4, rect_text.height + 4)
    text_pos = pygame.Vector2(
        rect.centerx - rect_text.width / 2,
        rect.bottom + 5
    )
    outline.center = text_pos + pygame.Vector2(rect_text.width / 2, rect_text.height / 2)
    pygame.draw.rect(screen, (70, 130, 180), outline)
    screen.blit(rend_text, text_pos)


class Slider:
    def __init__(self, x, y, width, height, total_items, visible_items):
        self.rect = pygame.Rect(x, y, width, height)
        self.total_items = total_items
        self.visible_items = visible_items
        self.item_width = width / total_items
        self.visible_width = width / visible_items
        self.slider_rect = pygame.Rect(x, y, self.visible_width, height)
        self.dragging = False
        self.offset_x = 0

    def event_listener(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
                self.offset_x = event.pos[0] - self.slider_rect.x
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.slider_rect.x = event.pos[0] - self.offset_x
                self.slider_rect.x = max(self.rect.x, min(self.slider_rect.x,
                                                          self.rect.x + self.rect.width - self.slider_rect.width))

    def get_offset(self):
        max_offset = self.total_items - self.visible_items
        if max_offset <= 0:
            return 0
        return (self.slider_rect.x - self.rect.x) / (self.rect.width - self.slider_rect.width) * max_offset

    def update(self, screen):
        pygame.draw.rect(screen, (180, 180, 180), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.slider_rect)


# ======================================================================================================================

class Room:
    # Should be superclass only - never instantiated!
    def __init__(self):
        self.bg_color = RED
        self.state = 0
        self.name = self.__class__.__name__
        pygame.display.set_caption('ROOM (superclass)')

    def event_listener(self, ev, player):
        pass

    def update(self, screen, player):
        pass


# ======================================================================================================================

class Menu(Room):
    def __init__(self, last_room):
        super().__init__()
        self.bg_image = pygame.image.load("../Sprites/Backgrounds/MenuBG.png")
        self.bg_color = WHITE
        self.button_colors = (140, 197, 245)
        self.menu_button_1_rect = pygame.Rect((50, 360, 300, 80))
        self.menu_button_2_rect = pygame.Rect((50, 460, 300, 80))
        self.menu_button_3_rect = pygame.Rect((50, 560, 300, 80))
        self.menu_button_4_rect = pygame.Rect((50, 660, 300, 80))

        self.last_room = last_room
        pygame.display.set_caption("MENU")

    def event_listener(self, ev, player):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.menu_button_1_rect.collidepoint(pos):
                # Start Button
                if player.floor == 0 or player.cur_health <= 0:
                    # Start New Run
                    print("Start New Run!!!")
                    player.floor = 1
                    player.cur_health = player.max_health
                    STARTING_DECK = [cardsFile.Strike, cardsFile.Strike, cardsFile.Strike, cardsFile.Strike,
                                     cardsFile.Strike,
                                     cardsFile.Defend, cardsFile.Defend, cardsFile.Defend, cardsFile.Defend,
                                     cardsFile.Bash]
                    player.run_deck = [card() for card in STARTING_DECK]
                    player.current_room = CombatEncounter(player)

                else:
                    # Continue Current Run
                    print("Cont from last room")
                    player.current_room = self.last_room

                pass
            elif self.menu_button_2_rect.collidepoint(pos):
                player.current_room = Shop(player)
                pass
            elif self.menu_button_3_rect.collidepoint(pos):
                list_of_encounters = [Ritual(), Beggar(), Bridge()]
                player.current_room = random.choice(list_of_encounters)
            elif self.menu_button_4_rect.collidepoint(pos):
                player.current_room = RestRoom(player)

    def update(self, screen, player):
        screen.blit(self.bg_image, (0, 0))

        pygame.draw.rect(screen, self.button_colors, self.menu_button_1_rect)
        pygame.draw.rect(screen, self.button_colors, self.menu_button_2_rect)
        pygame.draw.rect(screen, self.button_colors, self.menu_button_3_rect)
        pygame.draw.rect(screen, self.button_colors, self.menu_button_4_rect)

        if player.floor == 0 or player.cur_health <= 0:
            button_1_text = text_font_big.render("BEGIN", True, (0, 0, 0))
        else:
            button_1_text = text_font_big.render(f"CONTINUE - FLOOR {player.floor}", True, (0, 0, 0))

        button_1_text_rect = button_1_text.get_rect()
        button_1_text_rect.center = self.menu_button_1_rect.center

        screen.blit(button_1_text, button_1_text_rect)


# ======================================================================================================================

class InGame(Room):
    # Should be superclass only - never instantiated!
    def __init__(self):
        super().__init__()
        self.menu_button_image = pygame.image.load("../Sprites/Misc/MenuIcon.png")
        self.menu_button_rect = self.menu_button_image.get_rect()
        self.menu_button_rect.topright = (1366, 0)

        self.info_bar = pygame.rect.Rect(0, 0, 1366, 25)
        self.info_bar.topleft = (0, 0)

        pygame.display.set_caption("IN GAME")

    def draw_info_bar(self, screen, player):
        floor_count_text = text_font.render(f"Floor: {player.floor}", True, (0, 0, 0))
        player_health_text = text_font.render(f"Health: {player.cur_health}/{player.max_health}", True, (0, 0, 0))
        money_amount_text = text_font.render(f"${player.coins}", True, (0, 0, 0))

        pygame.draw.rect(screen, (184, 183, 182), self.info_bar
                         )
        screen.blit(floor_count_text, (100 - (floor_count_text.get_width() // 2), 0))
        screen.blit(player_health_text, (250 - (player_health_text.get_width() // 2), 0))
        screen.blit(money_amount_text, (400 - (money_amount_text.get_width() // 2), 0))

        screen.blit(self.menu_button_image, self.menu_button_rect.topleft)

    def event_listener(self, ev, player):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.menu_button_rect.collidepoint(pos):
                last_room = player.current_room
                player.current_room = Menu(last_room)
                print(last_room.state)

    def update(self, screen, player):
        self.draw_info_bar(screen, player)


# ======================================================================================================================

class CombatEncounter(InGame):
    def __init__(self, player, custom_list_of_enemies=None,
                 custom_combat_difficulty=None):
        super().__init__()
        self.name = "Combat Encounter"

        self.list_of_enemies = []
        if player.fight_count < 3:
            self.combat_difficulty = CombatDifficulty.EASY
        elif player.floor < 7:
            self.combat_difficulty = CombatDifficulty.NORMAL
        elif player.floor == 16:
            self.combat_difficulty = CombatDifficulty.BOSS
        else:
            self.combat_difficulty = random.choices([CombatDifficulty.NORMAL, CombatDifficulty.ELITE], weights= [0.80, 0.20], k=1)[0]

        if custom_list_of_enemies is not None and custom_combat_difficulty is not None:
            self.list_of_enemies = custom_list_of_enemies
            self.combat_difficulty = custom_combat_difficulty
        else:
            self._get_random_combat(self.combat_difficulty)

        pygame.display.set_caption("COMBAT ENCOUNTER")
        self.bg_play_color = BLUE
        self.bg_play_rect = pygame.Rect((0, 0, 1366, 528))
        self.bg_enemy_color = GREEN
        self.bg_enemy_rect = pygame.Rect((500, 0, 866, 528))
        self.bg_hand_color = PURPLE
        self.bg_hand_rect = pygame.Rect((125, 528, 1116, 240))
        self.bg_image = pygame.image.load("../Sprites/Backgrounds/FightBG.png")
        self.bg_hand_image = pygame.image.load("../Sprites/Backgrounds/WoodBG.png")

        self.end_turn_color = BLACK
        self.end_turn_rect = pygame.Rect((1266, 668, 100, 100))
        self.end_turn_image = pygame.image.load("../Sprites/Misc/EndTurnButton.png")

        self._position_enemies()
        self.number_of_enemies = len(self.list_of_enemies)

    def event_listener(self, ev, player):
        super().event_listener(ev, player)
        if self.state == 2:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_i:
                    player.info()
                    for enemy in self.list_of_enemies:
                        enemy.info()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.end_turn_rect.collidepoint(pos):
                    print(f"END TURN")
                    self.state = 3
        cardsFile.event_listener(ev, player, self.list_of_enemies, self.bg_play_rect)
        player.event_listener(ev, player, self.list_of_enemies)
        for enemy in self.list_of_enemies:
            enemy.event_listener(ev, player, self.list_of_enemies)

    def update(self, screen, player):
        # Draw backgrounds Rects
        #pygame.draw.rect(screen, self.bg_play_color, self.bg_play_rect)
        #pygame.draw.rect(screen, self.bg_enemy_color, self.bg_enemy_rect)
        #pygame.draw.rect(screen, self.bg_hand_color, self.bg_hand_rect)
        screen.blit(self.bg_hand_image, (0, 30))
        screen.blit(self.bg_image, (0, -250))

        # Draw Go-To-Menu Rect
        super().update(screen, player)

        # Draw End-of-turn Rect
        #pygame.draw.rect(screen, self.end_turn_color, self.end_turn_rect)
        screen.blit(self.end_turn_image, self.end_turn_rect.topleft)

        # Update player
        player.update(screen)

        # Update every enemy
        for enemy in self.list_of_enemies:
            enemy.update(screen)

        # Update every card in hand + draw non-highlighted
        self.bg_hand_rect.update(0, 528, 140 * len(player.hand) - 140, 240)
        self.bg_hand_rect.centerx = 683
        for index, card in enumerate(player.hand):
            card.update(screen, player, index, self.bg_hand_rect)
        self._handle_highlight(player, screen)

        # Update animated 'particles' for actions taken
        for anim in player.anim_list:
            anim.update(player, screen)

        for enemy in self.list_of_enemies:
            for anim in enemy.anim_list:
                anim.update(enemy, screen)

        if self.state == 0:
            # COMBAT START
            player.start_combat()
            self.state = 1

        if self.state == 1:
            # ROUND START
            player.start_turn()
            for enemy in self.list_of_enemies:
                enemy.start_turn()
                enemy.declare_action(player, self.list_of_enemies)
            print(f">>--------------------------------------------------------------------------<<")
            player.info()
            for enemy in self.list_of_enemies:
                enemy.info()
            self.state = 2

        if self.state == 2:
            # PLAYER ACTIONS TURN
            for enemy in self.list_of_enemies:
                if enemy.cur_health <= 0:
                    if o.Effect.SPORE_CLOUD in enemy.dict_of_ongoing:
                        enemy.add_vulnerable(2, player)
                    if o.Effect.THIEVERY in enemy.dict_of_ongoing:
                        player.coins += enemy.stolen_gold
                    self.list_of_enemies.remove(enemy)
                    print(f"Enemy {enemy.name} is DEAD!")

            if player.cur_health <= 0:
                print(f">> (((  LOSE  )))")
                player.end_combat()
                player.current_room = Menu(None)  # LOSE
            elif all(enemy.cur_health <= 0 for enemy in self.list_of_enemies):
                print(f">> (((  WIN!  )))")
                player.end_combat()
                player.floor += 5
                player.current_room = Rewards(RewardsLevel.NORMAL_FIGHT, player)

        if self.state == 3:
            # END TURN
            print(f">>--------------------------------------------------------------------------<<")
            player.end_turn()

            for enemy in self.list_of_enemies:
                if o.Effect.METALLICIZE in enemy.dict_of_ongoing:
                    enemy.add_block(enemy.dict_of_ongoing[o.Effect.METALLICIZE].intensity, enemy)
                enemy.play_action(player, self.list_of_enemies)
                enemy.end_turn()
            print(f">>--------------------------------------------------------------------------<<")
            self.state = 1

    def _get_random_combat(self, combat_difficulty):
        # Get random combat encounter from the list
        fights = ()
        gremlin_list = random.choices(
            [enemyFile.FatGremlin, enemyFile.MadGremlin, enemyFile.ShieldGremlin, enemyFile.GremlinWizard,
             enemyFile.SneakyGremlin], k=4)

        if combat_difficulty == CombatDifficulty.EASY:
            fights = ([enemyFile.Cultist()],
                      [enemyFile.JawWorm()],
                      [enemyFile.Frog(), enemyFile.Frog(), enemyFile.Worm()],
                      [enemyFile.Worm(), enemyFile.Icecream(), enemyFile.Worm()],
                      [enemyFile.RedLouse(), enemyFile.GreenLouse()],
                      [enemyFile.AcidSlimeM(), enemyFile.SpikeSlimeS()],
                      [enemyFile.SpikeSlimeM(), enemyFile.AcidSlimeS()]
                      )

        elif combat_difficulty == CombatDifficulty.NORMAL:
            fights = ([gremlin() for gremlin in gremlin_list],
                      [enemyFile.SpikeSlimeL()],
                      [enemyFile.AcidSlimeL()],
                      [enemyFile.SpikeSlimeS(), enemyFile.SpikeSlimeS(), enemyFile.SpikeSlimeS(),
                       enemyFile.AcidSlimeS(), enemyFile.AcidSlimeS()],
                      [enemyFile.BlueSlaver()],
                      [enemyFile.RedSlaver()],
                      [enemyFile.RedLouse(), enemyFile.GreenLouse(), enemyFile.RedLouse()],
                      [enemyFile.GreenLouse(), enemyFile.RedLouse(), enemyFile.GreenLouse()],
                      [enemyFile.FungiBeast(), enemyFile.FungiBeast()],
                      [enemyFile.AcidSlimeM(), enemyFile.Looter()],
                      [enemyFile.AcidSlimeM(), enemyFile.RedSlaver()],
                      [enemyFile.SpikeSlimeM(), enemyFile.Cultist()],
                      [enemyFile.SpikeSlimeM(), enemyFile.BlueSlaver()],
                      [enemyFile.FungiBeast(), enemyFile.SpikeSlimeM()],
                      [enemyFile.JawWorm(), enemyFile.RedLouse(), enemyFile.GreenLouse()],
                      [enemyFile.JawWorm(), enemyFile.AcidSlimeM()],
                      [enemyFile.Looter()]
                      )
        elif combat_difficulty == CombatDifficulty.ELITE:
            fights = ([enemyFile.GremlinNob()],
                      [enemyFile.Lagavulin()],
                      [enemyFile.Sentry(position=1), enemyFile.Sentry(position=2), enemyFile.Sentry(position=3)]
                      )

        self.list_of_enemies += random.choice(fights)

    def _position_enemies(self):
        free_space = 866  # width of enemy area

        for enemy in self.list_of_enemies:
            free_space -= enemy.rect_sprite.width

        free_space /= (len(self.list_of_enemies) + 1)
        x = self.bg_enemy_rect.left

        for enemy in self.list_of_enemies:
            x += free_space
            enemy.rect_sprite.left = x
            x = enemy.rect_sprite.right

    def _handle_highlight(self, player, screen):
        pos = pygame.mouse.get_pos()
        if player.highlight is not None and player.highlight.rect.collidepoint(pos):
            # Keep highlight on card as long as it's hovered
            pass
        else:
            player.highlight = None
            for card in player.hand:
                if card.rect.collidepoint(pos):
                    player.highlight = card

        if player.highlight is not None:
            player.highlight.draw(screen)


# ======================================================================================================================


class Shop(InGame):
    def __init__(self, player):
        super().__init__()
        self.bg_color = GREEN
        pygame.display.set_caption("SHOP")
        self.available_cards = cardsFile.ALL_CARDS

        self.list_of_cards = []
        self.card_prices = []
        self.remove_price = random.randint(30, 50)
        self.card_sold = 0

        self.create_shop_items()

        self.bg_img = pygame.image.load("../Sprites/Backgrounds/planks.png")
        self.bg_rect = self.bg_img.get_rect()

        self.remove_card_img = pygame.image.load("../Sprites/Misc/RemoveButton.png")
        self.remove_card_rect = pygame.Rect((50, 60, 100, 100))

        self.leave_img = pygame.image.load("../Sprites/Misc/LeaveButton.png")
        self.leave_rect = pygame.Rect((1220, 640, 100, 100))

        self.bg_cards_img = pygame.image.load("../Sprites/Backgrounds/stone_bg.png")
        self.bg_cards_rect = self.bg_cards_img.get_rect()

        self.slider = Slider(220, 700, 926, 20, len(player.run_deck), 4)

    def create_shop_items(self):
        cards_weights = []
        for card in self.available_cards:
            if card().rarity == cardsFile.Rarity.COMMON:
                cards_weights.append(45)
            elif card().rarity == cardsFile.Rarity.UNCOMMON:
                cards_weights.append(35)
            elif card().rarity == cardsFile.Rarity.RARE:
                cards_weights.append(20)
            else:
                cards_weights.append(0)

        self.list_of_cards = [random.choices(self.available_cards, cards_weights)[0]() for _ in range(4)]
        self._set_prices()

    def _set_prices(self):
        for card in self.list_of_cards:
            if card.rarity == cardsFile.Rarity.COMMON:
                self.card_prices.append(random.randint(15, 25))
            elif card.rarity == cardsFile.Rarity.UNCOMMON:
                self.card_prices.append(random.randint(18, 30))
            elif card.rarity == cardsFile.Rarity.RARE:
                self.card_prices.append(random.randint(25, 40))
            else:
                self.card_prices.append(0)

    def _buy_card(self, card_index, player):
        if self.card_prices[card_index] <= player.coins:
            player.coins -= self.card_prices[card_index]
            player.add_card_to_run_deck(self.list_of_cards[card_index])
            print(f"You bought {self.list_of_cards[card_index].name} for {self.card_prices[card_index]} coins!")

            self.list_of_cards.pop(card_index)
            self.card_prices.pop(card_index)
        else:
            print("You don't have enough coins!")

    def event_listener(self, ev, player):
        self.slider.event_listener(ev)
        super().event_listener(ev, player)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.state == 0:
                if self.leave_rect.collidepoint(pos):
                    print(f"LEAVING SHOP")
                    player.floor += 1
                    player.current_room = Rewards(RewardsLevel.NO_REWARDS, player)
                elif self.remove_card_rect.collidepoint(pos) and not self.card_sold:
                    if player.coins >= self.remove_price:
                        self.state = 1
                for i, card in enumerate(self.list_of_cards):
                    if card.rect.collidepoint(pos):
                        self._buy_card(i, player)
            else:
                offset = int(self.slider.get_offset())
                visible_cards = player.run_deck[offset:offset + self.slider.visible_items]

                for card in visible_cards:
                    if card.rect.collidepoint(pos):
                        player.coins -= self.remove_price
                        print(f"Deleted: {card}")
                        player.remove_card_from_run_deck(card)
                        self.state = 0
                        self.card_sold = 1
                        break

    def update(self, screen, player):
        screen.blit(self.bg_img, self.bg_rect)
        screen.blit(self.bg_cards_img, self.bg_cards_rect.topleft)
        if self.state == 0:
            screen.blit(self.leave_img, self.leave_rect.topleft)

            if not self.card_sold:
                screen.blit(self.remove_card_img, self.remove_card_rect.topleft)
                button_caption(f"Remove Card: {self.remove_price}", self.remove_card_rect, screen)

            self.bg_cards_rect.update(0, 220, 1366, 485)
            for index, card in enumerate(self.list_of_cards):
                card.update(screen, player, index, self.bg_cards_rect)
                button_caption(f"{card.name}: [{self.card_prices[index]}]", card.rect, screen)

        else:
            offset = int(self.slider.get_offset())
            visible_cards = player.run_deck[offset:offset + 4]

            for index, card in enumerate(visible_cards):
                card.rect.y = 240 + index * 120
                card.update(screen, player, index, self.bg_cards_rect)
                button_caption(card.name, card.rect, screen)

            self.slider.update(screen)

        super().update(screen, player)


# ======================================================================================================================

class RandomEncounter(InGame):
    def __init__(self):
        super().__init__()

        self.bg_img = pygame.image.load("../Sprites/Backgrounds/Event_BG.png")
        self.bg_rect = self.bg_img.get_rect()

        self.ev_img = pygame.image.load("../Sprites/Backgrounds/EventImage.png")
        self.ev_rect = pygame.Rect((0, 30, 1266, 600))

        self.ev_name = text_font_bigger.render(self.name, True, (218, 165, 32))
        self.name_rect = self.ev_name.get_rect()
        self.name_rect.topleft = (220, 143)

        self.choice_1_img = pygame.image.load("../Sprites/Misc/ChoiceButton.png")
        self.choice_1_rect = pygame.Rect((540, 400, 623, 46))
        self.choice_2_img = pygame.image.load("../Sprites/Misc/ChoiceButton.png")
        self.choice_2_rect = pygame.Rect((540, 470, 623, 46))

        self.exit_img = pygame.image.load("../Sprites/Misc/LeaveButton.png")
        self.exit_rect = pygame.Rect((1160, 580, 100, 100))
        pygame.display.set_caption("RANDOM ENCOUNTER")

    def update(self, screen, player):
        super().update(screen, player)
        screen.blit(self.bg_img, self.bg_rect)
        screen.blit(self.ev_img, self.ev_rect)
        screen.blit(self.ev_name, self.name_rect)
        self.draw_info_bar(screen, player)

    def event_listener(self, ev, player):
        super().event_listener(ev, player)


# ======================================================================================================================

class Ritual(RandomEncounter):
    def __init__(self):
        super().__init__()

        self.ev_photo = pygame.image.load("../Sprites/Misc/Ritual.png")
        self.ev_photo_rect = pygame.Rect((120, 250, 400, 400))

        self.choice_3_img = pygame.image.load("../Sprites/Misc/ChoiceButton.png")
        self.choice_3_rect = pygame.Rect((540, 540, 623, 46))

        self.choice_1_text = text_font_big.render("Attack them", True, (255, 255, 255))
        self.choice_1_text_rect = self.choice_1_text.get_rect()
        self.choice_1_text_rect.center = self.choice_1_rect.center

        self.choice_2_text = text_font_big.render("Join the prayer, as they slaughter their pray", True, (255, 255, 255))
        self.choice_2_text_rect = self.choice_2_text.get_rect()
        self.choice_2_text_rect.center = self.choice_2_rect.center

        self.choice_3_text = text_font_big.render("Leave before they notice you", True, (255, 255, 255))
        self.choice_3_text_rect = self.choice_3_text.get_rect()
        self.choice_3_text_rect.center = self.choice_3_rect.center

    def event_listener(self, ev, player):
        super().event_listener(ev, player)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.state == 0:
                if self.choice_1_rect.collidepoint(pos):
                    self.state = 1
                elif self.choice_2_rect.collidepoint(pos):
                    player.add_card_to_run_deck(cardsFile.Feed())
                    player.add_card_to_run_deck(cardsFile.Wound())
                    self.state = 2
                elif self.choice_3_rect.collidepoint(pos):
                    self.state = 3
            elif self.state in (2, 3):
                if self.exit_rect.collidepoint(pos):
                    player.floor += 1
                    player.current_room = Rewards(RewardsLevel.NO_REWARDS, player)

    def update(self, screen, player):
        super().update(screen, player)
        screen.blit(self.ev_photo, self.ev_photo_rect)

        if self.state == 0:
            screen.blit(self.choice_1_img, self.choice_1_rect)
            screen.blit(self.choice_1_text, self.choice_1_text_rect)

            screen.blit(self.choice_2_img, self.choice_2_rect)
            screen.blit(self.choice_2_text, self.choice_2_text_rect)

            screen.blit(self.choice_3_img, self.choice_3_rect)
            screen.blit(self.choice_3_text, self.choice_3_text_rect)

            multi_text_render("You have stumbled upon two masked man, trying to sacrifice poor, emaciated man.\n"
                              "They haven't noticed you yet.\n"
                              "One of them rises up his jagged dagger, whispering a prayer to his goddess.\n"
                              "What do you do?\n",
                              screen)
        elif self.state == 1:
            player.current_room = CombatEncounter(player, [enemyFile.Cultist(), enemyFile.Cultist()],
                                                  custom_combat_difficulty=CombatDifficulty.EASY)

        elif self.state == 2:
            multi_text_render("You join in the prayers, mumbling something under your breath.\n"
                              "The screams of killed man slowly fade away, leaving you with nothing but silence.\n"
                              "You look at the cultists, feasting on sacrifice's blood, their muscles growing visibly.\n"
                              "You can perform the same ritual now, but the feeling of uneasiness doesn't leave you.\n\n"
                              "You gain both Feed and Wound cards", screen)
            screen.blit(self.exit_img, self.exit_rect)
        elif self.state == 3:
            multi_text_render("You leave, ignoring this poor man's cries for help.\n"
                              "His problems are not yours.\n", screen)
            screen.blit(self.exit_img, self.exit_rect)


# ======================================================================================================================

class Beggar(RandomEncounter):
    def __init__(self):
        super().__init__()

        self.ev_photo = pygame.image.load("../Sprites/Misc/Beggar.png")
        self.ev_photo_rect = pygame.Rect((120, 250, 400, 400))

        self.choice_3_img = pygame.image.load("../Sprites/Misc/ChoiceButton.png")
        self.choice_3_rect = pygame.Rect((540, 540, 623, 46))

        self.choice_1_text = text_font_big.render("Give him some gold (50)", True, (255, 255, 255))
        self.choice_1_text_rect = self.choice_1_text.get_rect()
        self.choice_1_text_rect.center = self.choice_1_rect.center

        self.choice_2_text = text_font_big.render("Give him some food (Lose Flex card)", True,
                                                  (255, 255, 255))
        self.choice_2_text_rect = self.choice_2_text.get_rect()
        self.choice_2_text_rect.center = self.choice_2_rect.center

        self.choice_3_text = text_font_big.render("Ignore his plea", True, (255, 255, 255))
        self.choice_3_text_rect = self.choice_3_text.get_rect()
        self.choice_3_text_rect.center = self.choice_3_rect.center

    def event_listener(self, ev, player):
        super().event_listener(ev, player)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.state == 0:
                if self.choice_1_rect.collidepoint(pos):
                    if player.coins >= 30:
                        player.coins -= 30
                        player.add_card_to_run_deck(cardsFile.Bludgeon())
                        self.state = 1
                elif self.choice_2_rect.collidepoint(pos):
                    flex_card = None
                    for card in player.run_deck:
                        if isinstance(card, cardsFile.Flex):
                            flex_card = card
                            break
                    if flex_card:
                        player.remove_card_from_run_deck(flex_card)
                        player.add_card_to_run_deck(cardsFile.Bludgeon())
                        self.state = 2
                elif self.choice_3_rect.collidepoint(pos):
                    player.cur_health -= 10
                    self.state = 3
            elif self.state in (1, 2, 3):
                if self.exit_rect.collidepoint(pos):
                    player.floor += 1
                    player.current_room = Rewards(RewardsLevel.NO_REWARDS, player)

    def update(self, screen, player):
        super().update(screen, player)
        screen.blit(self.ev_photo, self.ev_photo_rect)

        if self.state == 0:
            screen.blit(self.choice_1_img, self.choice_1_rect)
            screen.blit(self.choice_1_text, self.choice_1_text_rect)

            screen.blit(self.choice_2_img, self.choice_2_rect)
            screen.blit(self.choice_2_text, self.choice_2_text_rect)

            screen.blit(self.choice_3_img, self.choice_3_rect)
            screen.blit(self.choice_3_text, self.choice_3_text_rect)

            multi_text_render("A lone beggar approaches you, begging for your help.\n"
                              "He looks hungry, yet there's some kind of spark in his eyes.\n"
                              "What do you do?\n", screen)
        elif self.state == 1:
            multi_text_render("Delighted beggar takes your coins, counting every one of them.\n"
                              "He then looks you in the eyes, leans slightly and touches your left temple.\n"
                              "New knowledge floods your mind, leaving you with new ability.\n"
                              "When you open your eyes, the beggar is gone.\n\n"
                              "You lose 50 gold, but gain Bludgeon card", screen)
            screen.blit(self.exit_img, self.exit_rect)
        elif self.state == 2:
            multi_text_render("Delighted beggar takes bread you gave him, biting on it eagerly.\n"
                              "He then looks you in the eyes, leans slightly and touches your left temple.\n"
                              "New knowledge floods your mind, leaving you with new ability.\n"
                              "When you open your eyes, the beggar is gone.\n\n"
                              "You lose Flex card, but gain Bludgeon card", screen)
            screen.blit(self.exit_img, self.exit_rect)
        elif self.state == 3:
            multi_text_render("Beggar looks you in the eyes for a while, slowly shaking.\n"
                              "Then, you see anger rising in his eyes.\n"
                              "\"You rich fellas think you're better than us, huh?\".\n"
                              "Then, a large fireball grows in his hand.\n"
                              "You try to run away, but some of the fire still catches up to you.\n\n"
                              "You lose 10 current health", screen)
            screen.blit(self.exit_img, self.exit_rect)


# ======================================================================================================================

class Bridge(RandomEncounter):
    def __init__(self):
        super().__init__()

        self.ev_photo = pygame.image.load("../Sprites/Misc/Bridge.png")
        self.ev_photo_rect = pygame.Rect((120, 250, 400, 400))

        self.choice_1_text = text_font_big.render("Rush to the other side", True, (255, 255, 255))
        self.choice_1_text_rect = self.choice_1_text.get_rect()
        self.choice_1_text_rect.center = self.choice_1_rect.center

        self.choice_2_text = text_font_big.render("Slowly and carefully cross the bridge", True, (255, 255, 255))
        self.choice_2_text_rect = self.choice_2_text.get_rect()
        self.choice_2_text_rect.center = self.choice_2_rect.center

    def event_listener(self, ev, player):
        super().event_listener(ev, player)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.state == 0:
                if self.choice_1_rect.collidepoint(pos):
                    player.cur_health -= 10
                    self.state = 1
                elif self.choice_2_rect.collidepoint(pos):
                    self.state = random.randint(2, 3)
                    if self.state == 3:
                        player.add_card_to_run_deck(cardsFile.Wound())
            elif self.state in (1, 2, 3):
                if self.exit_rect.collidepoint(pos):
                    player.floor += 1
                    player.current_room = Rewards(RewardsLevel.NO_REWARDS, player)

    def update(self, screen, player):
        super().update(screen, player)
        screen.blit(self.ev_photo, self.ev_photo_rect)

        if self.state == 0:
            screen.blit(self.choice_1_img, self.choice_1_rect)
            screen.blit(self.choice_1_text, self.choice_1_text_rect)

            screen.blit(self.choice_2_img, self.choice_2_rect)
            screen.blit(self.choice_2_text, self.choice_2_text_rect)

            multi_text_render("A giant chasm blocks your path.\n"
                              "Luckily, there is a old-looking bridge, which can get you to the other side.\n"
                              "When you take a few steps, the bridge starts to creak. It doesn't look very steady\n"
                              "What do you do?\n", screen)
        elif self.state == 1:
            multi_text_render("It wasn't very thoughtful of you.\n"
                              "With each step, the bridge creaks more, eventually cracking under your weight.\n"
                              "Luckily, you manage to grab the edge of the chasm, though you get hurt in the process.\n"
                              "You get up, check your wounds, and resume your journey.\n\n"
                              "You lose 10 current health", screen)
            screen.blit(self.exit_img, self.exit_rect)
        elif self.state == 2:
            multi_text_render("You slowly get to the other side of a chasm.\n"
                              "Though stressful, the journey left you unscratched.", screen)
            screen.blit(self.exit_img, self.exit_rect)
        elif self.state == 3:
            multi_text_render("The journey through the bridge is long and tiring.\n"
                              "When you get on the other side, you're beyond exhausted.\n"
                              "Yet, the further road awaits...\n\n"
                              "You gained card: Wound", screen)
            screen.blit(self.exit_img, self.exit_rect)
            button_caption("Leave", self.exit_rect, screen)


# ======================================================================================================================

class RestRoom(InGame):
    def __init__(self, player):
        super().__init__()
        self.name = "Rest Room"

        self.bg_img = pygame.image.load("../Sprites/Backgrounds/RestBg.png")
        self.bg_rect = self.bg_img.get_rect()

        self.rest_img = pygame.image.load("../Sprites/Misc/RestButton.png")
        self.rest_rect = pygame.Rect((700, 200, 222, 145))

        self.leave_img = pygame.image.load("../Sprites/Misc/LeaveButton.png")
        self.leave_rect = pygame.Rect((1216, 580, 150, 150))

        self.heal = int(0.3 * player.max_health)

        self.darken = False
        self.darken_start_time = None
        self.alpha = 0

        pygame.display.set_caption("REST ROOM")

    def event_listener(self, ev, player):
        super().event_listener(ev, player)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rest_rect.collidepoint(pos) and self.heal:
                self.darken = True
                self.darken_start_time = time.time()
                player.heal(self.heal, player)
                self.heal = 0
            if self.leave_rect.collidepoint(pos):
                player.floor += 1
                player.current_room = Rewards(RewardsLevel.NO_REWARDS, player)

    def update(self, screen, player):
        screen.blit(self.bg_img, self.bg_rect)
        screen.blit(self.leave_img, self.leave_rect)
        if self.darken:
            elapsed_time = time.time() - self.darken_start_time
            if elapsed_time < 2.75:
                self.alpha = int((elapsed_time / 2) * 255)
                dark_surface = pygame.Surface((1366, 768))
                dark_surface.fill(BLACK)
                dark_surface.set_alpha(self.alpha)
                screen.blit(dark_surface, (0, 0))
            else:
                self.darken = False
                self.alpha = 0

        if self.heal:
            screen.blit(self.rest_img, self.rest_rect)
            button_caption("Rest", self.rest_rect, screen)

        super().update(screen, player)


# ======================================================================================================================

class Rewards(InGame):
    def __init__(self, rewards_level, player):
        super().__init__()
        self.rewards_cards = []
        self.gold = 0

        self.bg_img = pygame.image.load("../Sprites/Backgrounds/RewardsBg.png")
        self.bg_rect = pygame.Rect((267, 80, 831, 650))

        self.choice_1_img = pygame.image.load("../Sprites/Misc/LeftButton.png")
        self.choice_1_rect = pygame.Rect((130, 430, 300, 157))
        self.choice_1_room = Menu(None)

        self.choice_2_img = pygame.image.load("../Sprites/Misc/RightButton.png")
        self.choice_2_rect = pygame.Rect((946, 430, 300, 157))
        self.choice_2_room = Menu(None)

        self.set_rooms(player)
        self.choice_1_name = "Random Encounter" if self.is_random_encounter(
            self.choice_1_room) else self.choice_1_room.name
        self.choice_2_name = "Random Encounter" if self.is_random_encounter(
            self.choice_2_room) else self.choice_2_room.name

        if isinstance(self.choice_1_room, CombatEncounter):
            if self.choice_1_room.combat_difficulty == CombatDifficulty.ELITE:
                self.choice_1_name = "Elite Encounter"
            elif self.choice_1_room.combat_difficulty == CombatDifficulty.BOSS:
                self.choice_1_name = "Boss"
            else:
                self.choice_1_name = self.choice_1_room.name

        if isinstance(self.choice_2_room, CombatEncounter):
            if self.choice_2_room.combat_difficulty == CombatDifficulty.ELITE:
                self.choice_2_name = "Elite Encounter"
            elif self.choice_2_room.combat_difficulty == CombatDifficulty.BOSS:
                self.choice_2_name = "Boss"
            else:
                self.choice_2_name = self.choice_2_room.name

        self.available_cards = cardsFile.ALL_CARDS

        self.set_rewards(rewards_level)

        self.cards_img = pygame.image.load("../Sprites/Misc/RewardButton.png")
        self.cards_rect = pygame.Rect((507, 300, 350, 70))
        self.cards_text = text_font_big.render("Add a card to your deck", True, (255, 255, 255))
        self.cards_text_rect = self.cards_text.get_rect()
        self.cards_text_rect.center = self.cards_rect.center

        self.get_gold_img = pygame.image.load("../Sprites/Misc/RewardButton.png")
        self.get_gold_rect = pygame.Rect((507, 450, 350, 70))
        self.get_gold_icon = pygame.image.load("../Sprites/Misc/GoldIcon.png")
        self.get_gold_icon_rect = pygame.Rect((512, 457, 50, 55))
        self.get_gold_text = text_font_big.render(f"{self.gold} Gold", True, (255, 255, 255))
        self.get_gold_text_rect = self.get_gold_text.get_rect()
        self.get_gold_text_rect.center = self.get_gold_rect.center

        self.cards_leave_img = pygame.image.load("../Sprites/Misc/LeaveButton.png")
        self.cards_leave_rect = pygame.Rect((1220, 640, 100, 100))

        self.cards_bg_img = pygame.image.load("../Sprites/Backgrounds/stone_bg.png")
        self.cards_bg_rect = pygame.Rect((0, 220, 783, 480))

        pygame.display.set_caption("REWARDS")

    def set_rewards(self, rewards_level):
        cards_weights = []
        if rewards_level == RewardsLevel.NO_REWARDS:
            return

        elif rewards_level == RewardsLevel.EASY_FIGHT:
            for card in self.available_cards:
                if card().rarity == cardsFile.Rarity.COMMON:
                    cards_weights.append(60)
                elif card().rarity == cardsFile.Rarity.UNCOMMON:
                    cards_weights.append(40)
                else:
                    cards_weights.append(0)

            self.gold = (random.randint(20, 25))

        elif rewards_level == RewardsLevel.NORMAL_FIGHT:
            for card in self.available_cards:
                if card().rarity == cardsFile.Rarity.COMMON:
                    cards_weights.append(45)
                elif card().rarity == cardsFile.Rarity.UNCOMMON:
                    cards_weights.append(40)
                elif card().rarity == cardsFile.Rarity.RARE:
                    cards_weights.append(15)
                else:
                    cards_weights.append(0)

            self.gold = (random.randint(20, 25))

        elif rewards_level == RewardsLevel.ELITE_FIGHT:
            for card in self.available_cards:
                if card().rarity == cardsFile.Rarity.RARE:
                    cards_weights.append(100)
                else:
                    cards_weights.append(0)

            self.gold = (random.randint(40, 60))

        self.rewards_cards = [random.choices(self.available_cards, cards_weights)[0]() for _ in range(3)]

    def set_rooms(self, player):
        room_types = [CombatEncounter, self.choose_random_encounter, Shop, RestRoom]
        if player.floor < 6:
            self.choice_1_room = random.choices(room_types, [0.65, 0.20, 0.15, 0])[0]
            self.choice_1_room = self.check_arguments(player, self.choice_1_room)

            self.choice_2_room = random.choices(room_types, [0.65, 0.20, 0.15, 0])[0]
            self.choice_2_room = self.check_arguments(player, self.choice_2_room)
        elif player.floor == 15:
            self.choice_1_room, self.choice_2_room = RestRoom(player), RestRoom(player)
        elif player.floor == 16:
            self.choice_1_room, self.choice_2_room = CombatEncounter(player, custom_list_of_enemies=[enemyFile.Lagavulin()], custom_combat_difficulty=CombatDifficulty.BOSS), CombatEncounter(player, custom_list_of_enemies=[enemyFile.Lagavulin()], custom_combat_difficulty=CombatDifficulty.BOSS)
        else:
            self.choice_1_room = random.choices(room_types, [0.55, 0.15, 0.2, 0.1])[0]
            self.choice_1_room = self.check_arguments(player, self.choice_1_room)

            self.choice_2_room = random.choices(room_types, [0.55, 0.15, 0.2, 0.1])[0]
            self.choice_2_room = self.check_arguments(player, self.choice_2_room)

    def check_arguments(self, player, room):
        if 'player' in inspect.signature(room).parameters:
            return room(player)
        else:
            return room()

    def is_random_encounter(self, room):
        return isinstance(room, Ritual) or isinstance(room, Beggar) or isinstance(room, Bridge)

    def choose_random_encounter(self):
        list_of_encounters = [Ritual(), Beggar(), Bridge()]
        return random.choice(list_of_encounters)

    def event_listener(self, ev, player):
        super().event_listener(ev, player)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if not self.state:
                if self.choice_1_rect.collidepoint(pos):
                    player.current_room = self.choice_1_room
                elif self.choice_2_rect.collidepoint(pos):
                    player.current_room = self.choice_2_room
                elif self.get_gold_rect.collidepoint(pos) and self.gold:
                    player.coins += self.gold
                    self.gold = 0
                elif self.cards_rect.collidepoint(pos) and self.rewards_cards:
                    self.state = 1
            else:
                if self.cards_leave_rect.collidepoint(pos):
                    self.state = 0
                for card in self.rewards_cards:
                    if card.rect.collidepoint(pos):
                        player.add_card_to_run_deck(card)
                        self.rewards_cards.clear()
                        self.state = 0

    def update(self, screen, player):
        screen.fill(BLACK)
        if self.state == 0:
            screen.blit(self.bg_img, self.bg_rect)

            screen.blit(self.choice_1_img, self.choice_1_rect)
            button_caption(self.choice_1_name, self.choice_1_rect, screen)

            screen.blit(self.choice_2_img, self.choice_2_rect)
            button_caption(self.choice_2_name, self.choice_2_rect, screen)

            if self.gold:
                screen.blit(self.get_gold_img, self.get_gold_rect)
                screen.blit(self.get_gold_icon, self.get_gold_icon_rect)
                screen.blit(self.get_gold_text, self.get_gold_text_rect)

            if self.rewards_cards:
                screen.blit(self.cards_img, self.cards_rect)
                screen.blit(self.cards_text, self.cards_text_rect)

        if self.state == 1:
            screen.blit(self.cards_leave_img, self.cards_leave_rect)
            screen.blit(self.cards_bg_img, self.cards_bg_rect)

            for index, card in enumerate(self.rewards_cards):
                card.update(screen, player, index, self.cards_bg_rect)
                button_caption(card.name, card.rect, screen)

        super().update(screen, player)
