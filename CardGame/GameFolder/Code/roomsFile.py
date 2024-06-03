import pygame
import random
import enemyFile
import cardsFile
from fontsFile import text_font
import inspect

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


def multi_text_render(text, screen):
    rendered_fonts = []
    for i, line in enumerate(text.split('\n')):
        txt_surf = text_font.render(line, True, (0, 0, 0))
        txt_rect = txt_surf.get_rect()
        txt_rect.topleft = (350, 10 + i * 24)
        rendered_fonts.append((txt_surf, txt_rect))
    for txt_surf, txt_rect in rendered_fonts:
        screen.blit(txt_surf, txt_rect)


def button_caption(text, rect, screen):
    rend_text = text_font.render(text, True,
                                 (0, 0, 0))
    rect_text = rend_text.get_rect()
    text_pos = pygame.Vector2(
        rect.centerx - rect_text.width / 2,
        rect.bottom + 5
    )
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
        self.bg_color = WHITE
        self.button_colors = BLUE
        self.menu_button_1_rect = pygame.Rect((0, 0, 100, 100))
        self.menu_button_2_rect = pygame.Rect((0, 120, 100, 100))
        self.menu_button_3_rect = pygame.Rect((0, 240, 100, 100))
        self.menu_button_4_rect = pygame.Rect((0, 360, 100, 100))
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
                    player.current_room = CombatEncounter()

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
        pygame.draw.rect(screen, self.button_colors, self.menu_button_1_rect)
        pygame.draw.rect(screen, self.button_colors, self.menu_button_2_rect)
        pygame.draw.rect(screen, self.button_colors, self.menu_button_3_rect)
        pygame.draw.rect(screen, self.button_colors, self.menu_button_4_rect)

        if player.floor == 0 or player.cur_health <= 0:
            button_1_text = text_font.render("START NEW RUN (player.floor == 0 OR player.cur_health <= 0)", True,
                                             (0, 0, 0))
        else:
            button_1_text = text_font.render("CONT FROM LAST ROOM (player.floor != 0 OR player.cur_health < 0)", True,
                                             (0, 0, 0))

        button_1_text_rect = button_1_text.get_rect()
        button_1_text_rect.topleft = self.menu_button_1_rect.topright

        screen.blit(button_1_text, button_1_text_rect)


# ======================================================================================================================

class InGame(Room):
    # Should be superclass only - never instantiated!
    def __init__(self):
        super().__init__()
        self.menu_button_rect = pygame.Rect((1266, 0, 100, 100))
        self.menu_button_color = WHITE
        pygame.display.set_caption("IN GAME")

    def event_listener(self, ev, player):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.menu_button_rect.collidepoint(pos):
                last_room = player.current_room
                player.current_room = Menu(last_room)
                print(last_room.state)

    def update(self, screen, player):
        pygame.draw.rect(screen, self.menu_button_color, self.menu_button_rect)


# ======================================================================================================================

class CombatEncounter(InGame):
    def __init__(self, custom_list_of_enemies=None):
        super().__init__()
        if custom_list_of_enemies is None:
            custom_list_of_enemies = []
        pygame.display.set_caption("COMBAT ENCOUNTER")
        self.bg_play_color = BLUE
        self.bg_play_rect = pygame.Rect((0, 0, 1366, 528))
        self.bg_enemy_color = GREEN
        self.bg_enemy_rect = pygame.Rect((500, 0, 866, 528))
        self.bg_hand_color = PURPLE
        self.bg_hand_rect = pygame.Rect((125, 528, 1116, 240))

        self.end_turn_color = BLACK
        self.end_turn_rect = pygame.Rect((1266, 668, 100, 100))

        if not custom_list_of_enemies:
            self.list_of_enemies = []
            self._get_random_combat()
        else:
            self.list_of_enemies = custom_list_of_enemies

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
        pygame.draw.rect(screen, self.bg_play_color, self.bg_play_rect)
        pygame.draw.rect(screen, self.bg_enemy_color, self.bg_enemy_rect)
        pygame.draw.rect(screen, self.bg_hand_color, self.bg_hand_rect)

        # Draw Go-To-Menu Rect
        super().update(screen, player)

        # Draw End-of-turn Rect
        pygame.draw.rect(screen, self.end_turn_color, self.end_turn_rect)

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
                    self.list_of_enemies.remove(enemy)
                    print(f"Enemy {enemy.name} is DEAD!")

            if player.cur_health <= 0:
                print(f">> (((  LOSE  )))")
                player.end_combat()
                player.current_room = Menu(None)  # LOSE
            elif all(enemy.cur_health <= 0 for enemy in self.list_of_enemies):
                print(f">> (((  WIN!  )))")
                player.end_combat()
                player.floor += 1
                player.current_room = Rewards(self.number_of_enemies, player)

        if self.state == 3:
            # END TURN
            print(f">>--------------------------------------------------------------------------<<")
            player.end_turn()

            for enemy in self.list_of_enemies:
                enemy.play_action(player, self.list_of_enemies)
                enemy.end_turn()
            print(f">>--------------------------------------------------------------------------<<")
            self.state = 1

    def _get_random_combat(self):
        # Get random combat encounter from the list
        fights = ([enemyFile.Cultist()],
                  [enemyFile.JawWorm()],
                  [enemyFile.Frog(), enemyFile.Frog(), enemyFile.Worm()],
                  [enemyFile.Worm(), enemyFile.Icecream(), enemyFile.Worm()]
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
        self.available_cards = [cardsFile.Anger,
                                cardsFile.BattleTrance,
                                cardsFile.BloodForBlood,
                                cardsFile.Bloodletting,
                                cardsFile.BodySlam,
                                cardsFile.Carnage,
                                cardsFile.Clash,
                                cardsFile.Cleave,
                                cardsFile.Clothesline,
                                cardsFile.Combust,
                                cardsFile.DarkEmbrace,
                                cardsFile.Disarm,
                                cardsFile.Dropkick,
                                cardsFile.Entrench,
                                cardsFile.Evolve,
                                cardsFile.FeelNoPain,
                                cardsFile.FireBreathing,
                                cardsFile.FlameBarrier,
                                cardsFile.Flex,
                                cardsFile.GhostlyArmor,
                                cardsFile.Havoc,
                                cardsFile.HeavyBlade,
                                cardsFile.Hemokinesis,
                                cardsFile.InfernalBlade,
                                cardsFile.Inflame,
                                cardsFile.Intimidate,
                                cardsFile.IronWave,
                                cardsFile.Juggernaut,
                                cardsFile.Metallicize,
                                cardsFile.PommelStrike,
                                cardsFile.PowerThrough,
                                cardsFile.Pummel,
                                cardsFile.Rage,
                                cardsFile.Rampage,
                                cardsFile.RecklessCharge,
                                cardsFile.Rupture,
                                cardsFile.SecondWind,
                                cardsFile.SeeingRed,
                                cardsFile.Sentinel,
                                cardsFile.SeverSoul,
                                cardsFile.Shockwave,
                                cardsFile.ShrugItOff,
                                cardsFile.SpotWeakness,
                                cardsFile.SwordBoomerang,
                                cardsFile.Thunderclap,
                                cardsFile.TrueGrit,
                                cardsFile.TwinStrike,
                                cardsFile.Uppercut,
                                cardsFile.Whirlwind,
                                cardsFile.WildStrike
                                ]

        self.list_of_cards = []
        self.card_prices = []
        self.remove_price = random.randint(30, 50)
        self.card_sold = 0

        self.create_shop_items()

        self.remove_card_color = GOLD
        self.remove_card_rect = pygame.Rect((50, 0, 100, 100))

        self.leave_color = BLACK
        self.leave_rect = pygame.Rect((1266, 618, 100, 100))

        self.bg_cards_color = PURPLE
        self.bg_cards_rect = pygame.Rect((0, 220, 1366, 480))

        self.slider = Slider(220, 700, 926, 20, len(player.run_deck), 4)

    def create_shop_items(self):
        cards_weights = [available_card().weight for available_card in self.available_cards]
        self.list_of_cards = [random.choices(self.available_cards, cards_weights)[0]() for _ in range(4)]
        self._set_prices()

    def _set_prices(self):
        for i, card in enumerate(self.list_of_cards):
            self.card_prices.append(random.randint(card.price_range[0], card.price_range[1]))

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

        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.state == 0:
                if self.leave_rect.collidepoint(pos):
                    print(f"LEAVING SHOP")
                    player.floor += 1
                    player.current_room = Rewards(0, player)
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
        if self.state == 0:
            pygame.draw.rect(screen, self.bg_cards_color, self.bg_cards_rect)
            pygame.draw.rect(screen, self.leave_color, self.leave_rect)
            button_caption("Leave", self.leave_rect, screen)

            if not self.card_sold:
                pygame.draw.rect(screen, self.remove_card_color, self.remove_card_rect)
                button_caption(f"Remove Card: {self.remove_price}", self.remove_card_rect, screen)

            self.bg_cards_rect.update(0, 220, 1366, 480)
            for index, card in enumerate(self.list_of_cards):
                card.update(screen, player, index, self.bg_cards_rect)
                button_caption(f"{card.name}: [{self.card_prices[index]}]", card.rect, screen)
            super().update(screen, player)
        else:
            offset = int(self.slider.get_offset())
            visible_cards = player.run_deck[offset:offset + 4]

            for index, card in enumerate(visible_cards):
                card.rect.y = 240 + index * 120
                card.update(screen, player, index, self.bg_cards_rect)
                button_caption(card.name, card.rect, screen)

            self.slider.update(screen)


# ======================================================================================================================

class RandomEncounter(InGame):
    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__
        self.choice_1_color = BLUE
        self.choice_1_rect = pygame.Rect((205, 400, 250, 250))
        self.choice_2_color = GREEN
        self.choice_2_rect = pygame.Rect((515, 400, 250, 250))
        self.exit_color = BLACK
        self.exit_rect = pygame.Rect((1116, 0, 250, 250))


# ======================================================================================================================

class Ritual(RandomEncounter):
    def __init__(self):
        super().__init__()
        self.choice_3_color = PURPLE
        self.choice_3_rect = pygame.Rect((825, 400, 250, 250))

    def event_listener(self, ev, player):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.state == 0:
                if self.choice_1_rect.collidepoint(pos):
                    self.state = 1
                elif self.choice_2_rect.collidepoint(pos):
                    player.add_card_to_run_deck(cardsFile.Ritual())
                    player.add_card_to_run_deck(cardsFile.Wound())
                    self.state = 2
                elif self.choice_3_rect.collidepoint(pos):
                    self.state = 3
            elif self.state in (2, 3):
                if self.exit_rect.collidepoint(pos):
                    player.floor += 1
                    player.current_room = Rewards(0, player)

    def update(self, screen, player):
        if self.state == 0:
            pygame.draw.rect(screen, self.choice_1_color, self.choice_1_rect)
            button_caption("Attack them", self.choice_1_rect, screen)

            pygame.draw.rect(screen, self.choice_2_color, self.choice_2_rect)
            button_caption("Join the prayer, as they slaughter their pray", self.choice_2_rect, screen)

            pygame.draw.rect(screen, self.choice_3_color, self.choice_3_rect)
            button_caption("Leave before they notice you", self.choice_3_rect, screen)

            multi_text_render("You have stumbled upon two masked man, trying to sacrifice poor, emaciated man.\n"
                              "They haven't noticed you yet.\n"
                              "One of them rises up his jagged dagger, whispering a prayer to his goddess. What do you do?\n",
                              screen)
        elif self.state == 1:
            player.current_room = CombatEncounter([enemyFile.Cultist(), enemyFile.Cultist()])
        elif self.state == 2:
            multi_text_render("You join in the prayers, mumbling something under your breath.\n"
                              "The screams of killed man slowly fade away, leaving you with nothing but silence.\n"
                              "You look at the cultists, feasting on sacrifice's blood, their muscles growing visibly.\n"
                              "You can perform the same ritual now, but the feeling of uneasiness doesn't leave you.\n\n"
                              "You gain both Ritual and Wound cards", screen)
            pygame.draw.rect(screen, self.exit_color, self.exit_rect)
        elif self.state == 3:
            multi_text_render("You leave, ignoring this poor man's cries for help.\n"
                              "His problems are not yours.\n", screen)
            pygame.draw.rect(screen, self.exit_color, self.exit_rect)
            button_caption("Leave", self.exit_rect, screen)


# ======================================================================================================================

class Beggar(RandomEncounter):
    def __init__(self):
        super().__init__()
        self.choice_3_color = PURPLE
        self.choice_3_rect = pygame.Rect((825, 400, 250, 250))

    def event_listener(self, ev, player):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.state == 0:
                if self.choice_1_rect.collidepoint(pos):
                    if player.coins >= 30:
                        player.coins -= 30
                        player.add_card_to_run_deck(cardsFile.Fireball())
                        self.state = 1
                elif self.choice_2_rect.collidepoint(pos):
                    buff_card = None
                    for card in player.run_deck:
                        if isinstance(card, cardsFile.A100pNatural):
                            buff_card = card
                            break
                    if buff_card:
                        player.remove_card_from_run_deck(buff_card)
                        player.add_card_to_run_deck(cardsFile.Fireball())
                        self.state = 2
                elif self.choice_3_rect.collidepoint(pos):
                    player.cur_health -= 10
                    self.state = 3
            elif self.state in (1, 2, 3):
                if self.exit_rect.collidepoint(pos):
                    player.floor += 1
                    player.current_room = Rewards(0, player)

    def update(self, screen, player):
        if self.state == 0:
            pygame.draw.rect(screen, self.choice_1_color, self.choice_1_rect)
            button_caption("Give him some gold (30)", self.choice_1_rect, screen)

            pygame.draw.rect(screen, self.choice_2_color, self.choice_2_rect)
            button_caption("Give him some food (Lose Buff card)", self.choice_2_rect, screen)

            pygame.draw.rect(screen, self.choice_3_color, self.choice_3_rect)
            button_caption("Ignore his plea", self.choice_3_rect, screen)

            multi_text_render("A lone beggar approaches you, begging for your help.\n"
                              "He looks hungry, yet there's some kind of spark in his eyes.\n"
                              "What do you do?\n", screen)
        elif self.state == 1:
            multi_text_render("Delighted beggar takes your coins, counting every one of them.\n"
                              "He then looks you in the eyes, leans slightly and touches your left temple.\n"
                              "New knowledge floods your mind, leaving you with new ability.\n"
                              "When you open your eyes, the beggar is gone.\n\n"
                              "You lose 30 gold, but gain Fireball card", screen)
            pygame.draw.rect(screen, self.exit_color, self.exit_rect)
        elif self.state == 2:
            multi_text_render("Delighted beggar takes bread you gave him, biting on it eagerly.\n"
                              "He then looks you in the eyes, leans slightly and touches your left temple.\n"
                              "New knowledge floods your mind, leaving you with new ability.\n"
                              "When you open your eyes, the beggar is gone.\n\n"
                              "You lose Buff card, but gain Fireball card", screen)
            pygame.draw.rect(screen, self.exit_color, self.exit_rect)
        elif self.state == 3:
            multi_text_render("Beggar looks you in the eyes for a while, slowly shaking.\n"
                              "Then, you see anger rising in his eyes.\n"
                              "\"You rich fellas think you're better than us, huh?\".\n"
                              "Then, a large fireball grows in his hand.\n"
                              "You try to run away, but some of the fire still catches up to you.\n\n"
                              "You lose 10 current health", screen)
            pygame.draw.rect(screen, self.exit_color, self.exit_rect)
            button_caption("Leave", self.exit_rect, screen)


# ======================================================================================================================


class Bridge(RandomEncounter):
    def __init__(self):
        super().__init__()

    def event_listener(self, ev, player):
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
                    player.current_room = Rewards(0, player)

    def update(self, screen, player):
        if self.state == 0:
            pygame.draw.rect(screen, self.choice_1_color, self.choice_1_rect)
            button_caption("Rush to the other side", self.choice_1_rect, screen)

            pygame.draw.rect(screen, self.choice_2_color, self.choice_2_rect)
            button_caption("Slowly and carefully cross the bridge", self.choice_2_rect, screen)

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
            pygame.draw.rect(screen, self.exit_color, self.exit_rect)
        elif self.state == 2:
            multi_text_render("You slowly get to the other side of a chasm.\n"
                              "Though stressful, the journey left you unscratched.", screen)
            pygame.draw.rect(screen, self.exit_color, self.exit_rect)
        elif self.state == 3:
            multi_text_render("The journey through the bridge is long and tiring.\n"
                              "When you get on the other side, you're beyond exhausted.\n"
                              "Yet, the further road awaits...\n\n"
                              "You gained card: Wound", screen)
            pygame.draw.rect(screen, self.exit_color, self.exit_rect)
            button_caption("Leave", self.exit_rect, screen)


# ======================================================================================================================

class RestRoom(InGame):
    def __init__(self, player):
        super().__init__()
        self.rest_color = BLUE
        self.rest_rect = pygame.Rect((205, 400, 250, 250))

        self.leave_color = BLACK
        self.leave_rect = pygame.Rect((1216, 580, 150, 150))

        self.heal = int(0.3 * player.max_health)

    def event_listener(self, ev, player):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rest_rect.collidepoint(pos) and self.heal:
                player.heal(self.heal, player)
                self.heal = 0
            if self.leave_rect.collidepoint(pos):
                player.floor += 1
                player.current_room = Rewards(0, player)

    def update(self, screen, player):
        if self.heal:
            pygame.draw.rect(screen, self.rest_color, self.rest_rect)
            button_caption("Rest", self.rest_rect, screen)

        pygame.draw.rect(screen, self.leave_color, self.leave_rect)
        button_caption("Leave", self.leave_rect, screen)


# ======================================================================================================================

class Rewards(InGame):
    def __init__(self, enemies_numb, player):
        super().__init__()
        self.rewards_cards = []
        self.gold = 0

        self.choice_1_color = BLUE
        self.choice_1_rect = pygame.Rect((205, 400, 250, 250))
        self.choice_1_room = Menu(None)

        self.choice_2_color = GREEN
        self.choice_2_rect = pygame.Rect((911, 400, 250, 250))
        self.choice_2_room = Menu(None)

        self.set_rooms(player)
        self.choice_1_name = "Random Encounter" if self.is_random_encounter(
            self.choice_1_room) else self.choice_1_room.name
        self.choice_2_name = "Random Encounter" if self.is_random_encounter(
            self.choice_2_room) else self.choice_2_room.name

        self.cards_color = PURPLE
        self.cards_rect = pygame.Rect((1166, 0, 200, 150))

        self.get_gold_color = GOLD
        self.get_gold_rect = pygame.Rect((0, 0, 200, 150))

        self.cards_leave_color = BLACK
        self.cards_leave_rect = pygame.Rect((1216, 618, 150, 150))

        self.cards_bg_color = RED
        self.cards_bg_rect = pygame.Rect((0, 220, 783, 480))

        self.available_cards = [cardsFile.Anger,
                                cardsFile.BattleTrance,
                                cardsFile.BloodForBlood,
                                cardsFile.Bloodletting,
                                cardsFile.BodySlam,
                                cardsFile.Carnage,
                                cardsFile.Clash,
                                cardsFile.Cleave,
                                cardsFile.Clothesline,
                                cardsFile.Combust,
                                cardsFile.DarkEmbrace,
                                cardsFile.Disarm,
                                cardsFile.Dropkick,
                                cardsFile.Entrench,
                                cardsFile.Evolve,
                                cardsFile.FeelNoPain,
                                cardsFile.FireBreathing,
                                cardsFile.FlameBarrier,
                                cardsFile.Flex,
                                cardsFile.GhostlyArmor,
                                cardsFile.Havoc,
                                cardsFile.HeavyBlade,
                                cardsFile.Hemokinesis,
                                cardsFile.InfernalBlade,
                                cardsFile.Inflame,
                                cardsFile.Intimidate,
                                cardsFile.IronWave,
                                cardsFile.Juggernaut,
                                cardsFile.Metallicize,
                                cardsFile.PommelStrike,
                                cardsFile.PowerThrough,
                                cardsFile.Pummel,
                                cardsFile.Rage,
                                cardsFile.Rampage,
                                cardsFile.RecklessCharge,
                                cardsFile.Rupture,
                                cardsFile.SecondWind,
                                cardsFile.SeeingRed,
                                cardsFile.Sentinel,
                                cardsFile.SeverSoul,
                                cardsFile.Shockwave,
                                cardsFile.ShrugItOff,
                                cardsFile.SpotWeakness,
                                cardsFile.SwordBoomerang,
                                cardsFile.Thunderclap,
                                cardsFile.TrueGrit,
                                cardsFile.TwinStrike,
                                cardsFile.Uppercut,
                                cardsFile.Whirlwind,
                                cardsFile.WildStrike
                                ]

        self.set_rewards(enemies_numb)

    def set_rewards(self, enemies_numb):
        if enemies_numb > 0:
            cards_weights = [available_card().weight for available_card in self.available_cards]
            self.rewards_cards = [random.choices(self.available_cards, cards_weights)[0]() for _ in range(2)]
            self.gold = (enemies_numb * random.randint(20, 25))

    def set_rooms(self, player):
        room_types = [CombatEncounter, self.choose_random_encounter, Shop, RestRoom]
        if player.floor < 6:
            self.choice_1_room = random.choices(room_types, [0.65, 0.25, 0.1, 0])[0]
            self.choice_1_room = self.check_arguments(player, self.choice_1_room)

            self.choice_2_room = random.choices(room_types, [0.65, 0.25, 0.1, 0])[0]
            self.choice_2_room = self.check_arguments(player, self.choice_2_room)
        elif player.floor == 15:
            self.choice_1_room, self.choice_2_room = RestRoom(player), RestRoom(player)
        else:
            self.choice_1_room = random.choices(room_types, [0.6, 0.25, 0.1, 0.05])[0]
            self.choice_1_room = self.check_arguments(player, self.choice_1_room)

            self.choice_2_room = random.choices(room_types, [0.6, 0.25, 0.1, 0.05])[0]
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

    def update(self, screen, player):
        if self.state == 0:
            pygame.draw.rect(screen, self.choice_1_color, self.choice_1_rect)
            button_caption(self.choice_1_name, self.choice_1_rect, screen)

            pygame.draw.rect(screen, self.choice_2_color, self.choice_2_rect)
            button_caption(self.choice_2_name, self.choice_2_rect, screen)

            if self.rewards_cards:
                pygame.draw.rect(screen, self.cards_color, self.cards_rect)
                button_caption("Choose a card", self.cards_rect, screen)

            if self.gold:
                pygame.draw.rect(screen, self.get_gold_color, self.get_gold_rect)
                button_caption(f"Gold: {self.gold}", self.get_gold_rect, screen)

        if self.state == 1:
            pygame.draw.rect(screen, self.cards_leave_color, self.cards_leave_rect)
            button_caption("Leave", self.cards_leave_rect, screen)

            pygame.draw.rect(screen, self.cards_bg_color, self.cards_bg_rect)

            self.cards_bg_rect.update(0, 220, 783, 480)
            for index, card in enumerate(self.rewards_cards):
                card.update(screen, player, index, self.cards_bg_rect)
                button_caption(card.name, card.rect, screen)
