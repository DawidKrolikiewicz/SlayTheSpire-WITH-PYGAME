import pygame
import random
import enemyFile
import cardsFile


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (150, 0, 250)


# > Room   (superclass)
# - Menu
# > InGame (superclass)
# - CombatEncounter
# - Shop


# ======================================================================================================================

class Room:
    # Should be superclass only - never instantiated!
    def __init__(self):
        self.bg_color = RED
        self.state = 0
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
                if self.last_room.__class__.__name__ == "CombatEncounter":
                    # Continue Current Run
                    print("Cont Last Combat")
                    player.current_room = self.last_room
                    for i in range(25):
                        print(f"")
                else:
                    # Start New Run
                    print("Start New Combat!!!")
                    player.current_room = CombatEncounter()
                    for i in range(25):
                        print(f"")
                pass
            elif self.menu_button_2_rect.collidepoint(pos):
                player.current_room = Shop()
                pass
            elif self.menu_button_3_rect.collidepoint(pos):
                pass
            elif self.menu_button_4_rect.collidepoint(pos):
                pass

    def update(self, screen, player):
        pygame.draw.rect(screen, self.button_colors, self.menu_button_1_rect)
        pygame.draw.rect(screen, self.button_colors, self.menu_button_2_rect)
        pygame.draw.rect(screen, self.button_colors, self.menu_button_3_rect)
        pygame.draw.rect(screen, self.button_colors, self.menu_button_4_rect)


# ======================================================================================================================

class InGame(Room):
    # Should be superclass only - never instantiated!
    def __init__(self):
        super().__init__()
        self.menu_button_rect = pygame.Rect((1266, 0, 100, 100))
        self.menu_button_color = WHITE
        pygame.display.set_caption("INGAME")

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
    def __init__(self):
        super().__init__()
        pygame.display.set_caption("COMBAT ENCOUNTER")
        self.bg_play_color = BLUE
        self.bg_play_rect = pygame.Rect((0, 0, 1366, 528))
        self.bg_enemy_color = GREEN
        self.bg_enemy_rect = pygame.Rect((500, 0, 866, 528))
        self.bg_hand_color = PURPLE
        self.bg_hand_rect = pygame.Rect((125, 528, 1116, 240))

        self.end_turn_color = BLACK
        self.end_turn_rect = pygame.Rect((1266, 668, 100, 100))

        self.list_of_enemies = []
        self._get_random_combat()

        self._position_enemies()

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
        player.event_listener(ev, self.list_of_enemies)

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
        for enemy in self.list_of_enemies :
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
                player.current_room = Menu(None)
                player.end_combat()
            elif all(enemy.cur_health <= 0 for enemy in self.list_of_enemies):
                print(f">> (((  WIN!  )))")
                player.current_room = Menu(None)
                player.end_combat()

        if self.state == 3:
            # END TURN
            print(f">>--------------------------------------------------------------------------<<")
            for enemy in self.list_of_enemies:
                enemy.play_action(player, self.list_of_enemies)

            player.end_turn()
            print(f">>--------------------------------------------------------------------------<<")
            self.state = 1

    def _get_random_combat(self):
        # Get random combat encounter from the list
        fights = [[enemyFile.Worm("Wormmer", 1), enemyFile.Frog("Frogger", 6), enemyFile.Enemy("BaseEnemy", 6)]]
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
    def __init__(self):
        super().__init__()
        self.bg_color = GREEN
        pygame.display.set_caption("SHOP")
        self.available_cards = [cardsFile.Draw2Heal3, cardsFile.Draw1,
                                cardsFile.Buff, cardsFile.Debuff,
                                cardsFile.Armor4, cardsFile.Deal5Damage]
        self.list_of_cards = []
        self.card_prices = []

        self.create_shop_items()

        self.leave_color = BLACK
        self.leave_rect = pygame.Rect((1266, 668, 100, 100))

        self.bg_cards_color = PURPLE
        self.bg_cards_rect = pygame.Rect((0, 220, 1366, 320))

    def create_shop_items(self):
        cards_weights = [available_card().weight for available_card in self.available_cards]
        self.list_of_cards = [random.choices(self.available_cards, cards_weights)[0]() for _ in range(4)]
        self.set_prices()

    def set_prices(self):
        for i,card in enumerate(self.list_of_cards):
            self.card_prices.append(random.randint(card.price_range[0], card.price_range[1]))

    def buy_card(self, card_index, player):
        if self.card_prices[card_index] <= player.coins:
            player.coins -= self.card_prices[card_index]
            player.add_card_to_deck(self.list_of_cards[card_index])
            print(f"You bought {self.list_of_cards[card_index].name} for {self.card_prices[card_index]} coins!")

            self.list_of_cards.pop(card_index)
            self.card_prices.pop(card_index)
        else:
            print("You don't have enough coins!")

    def event_listener(self, ev, player):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.leave_rect.collidepoint(pos):
                print(f"LEAVING SHOP")
                player.current_room = Menu(None)
            for i, card in enumerate(self.list_of_cards):
                if card.rect.collidepoint(pos):
                    self.buy_card(i, player)

    def update(self, screen, player):
        pygame.draw.rect(screen, self.bg_cards_color, self.bg_cards_rect)
        pygame.draw.rect(screen, self.leave_color, self.leave_rect)

        for index, card in enumerate(self.list_of_cards):
            card.update(screen, player, index, self.bg_cards_rect)

        super().update(screen, player)
# ======================================================================================================================


class Ritual:
    def __init__(self):
        self.name = self.__class__.__name__

    def encounter(self, player, shop, random_encounters):
        while True:
            choice = int(input(("You have stumbled upon two masked man, trying to sacrifice poor, emaciated man.\n"
              "They haven't noticed you yet.\n"
              "One of them rises his jagged dagger up, whispering a prayer to his goddess. What do you do?\n"
              "1) Attack them\n"
              "2) Join the prayer, as they slaughter their pray\n"
              "3) Leave before they notice you\nChoice: ")))
            if choice == 1:
                k1 = enemyFile.Cultist(player)
                k2 = enemyFile.Cultist(player)
                #gl.combat_encounter(player, [k1, k2], shop, random_encounters)
                break
            elif choice == 2:
                print("You join in the prayers, mumbling something under your breath.\n"
                      "The screams of killed man slowly fade away, leaving you with nothing but silence.\n"
                      "You look at the cultists, feasting on sacrifice's blood, their muscles growing visibly.\n"
                      "You can perform the same ritual now, but the feeling of uneasiness doesn't leave you.")
                ritual = cardsFile.Ritual()
                feeble = cardsFile.Depression()
                player.add_card_do_deck(ritual)
                player.add_card_do_deck(feeble)
                break
            elif choice == 3:
                print("You leave, ignoring this poor man's cries for help.\n"
                      "His problems are not yours.\n")
                break
            else:
                print("Wrong input!")


class Beggar:
    def __init__(self):
        self.name = self.__class__.__name__

    def encounter(self, player, shop, random_encounters):
        while True:
            choice = int(input(("A lone beggar approaches you, begging for your help.\n"
                  "He looks hungry, yet there's some kind of spark in his eyes.\n"
                  "What do you do?\n"
                  "1) Give him some gold (30)\n"
                  "2) Give him some food (Lose Buff card)\n"
                  "3) Ignore his plea\nChoice: ")))
            if choice == 1:
                if player.coins >= 30:
                    player.coins -=30
                    player.add_card_do_deck(cardsFile.Fireball())
                    print("Delighted beggar takes your coins, counting every one of them.\n"
                          "He then looks you in the eyes, leans slightly and touches your left temple.\n"
                          "New knowledge floods your mind, leaving you with new ability.\n"
                          "When you open your eyes, the beggar is gone.")
                    break
                else:
                    print("You don't have enough coins!")
            elif choice == 2:
                buff_card = None
                for card in player.deck:
                    if isinstance(card, cardsFile.Buff):
                        buff_card = card
                        break
                if buff_card:
                    player.remove_card_from_deck(buff_card)
                    player.add_card_do_deck(cardsFile.Fireball())
                    print("Delighted beggar takes bread you gave him, biting on it eagerly.\n"
                          "He then looks you in the eyes, leans slightly and touches your left temple.\n"
                          "New knowledge floods your mind, leaving you with new ability.\n"
                          "When you open your eyes, the beggar is gone.")
                    break
                else:
                    print("You don't have that card!")
            elif choice == 3:
                print("Beggar looks you in the eyes for a while, slowly shaking.\n"
                      "Then, you see anger rising in his eyes.\n"
                      "\"You rich fellas think you're better than us, huh?\".\n"
                      "Then, a large fireball grows in his hand.\n"
                      "You try to run away, but some of the fire still catches up to you.")
                player.health -= 10
                break
            else:
                print("Wrong input!")

class Bridge:
    def __init__(self):
        self.name = self.__class__.__name__

    def encounter(self, player, shop, random_encounters):
        while True:
            choice = int(input(("A giant chasm blocks your path.\n"
                  "Luckily, there is a old-looking bridge, which can get you to the other side.\n"
                  "When you take a few steps, the bridge starts to creak. It doesn't look very steady\n"
                  "What do you do?\n"
                  "1) Rush to the other side\n"
                  "2) Slowly and carefully cross the bridge\n")))
            if choice == 1:
                player.health -= 10
                print("It wasn't very thoughtful of you.\n"
                      "With each step, the bridge creaks more, eventually cracking under your weight.\n"
                      "Luckily, you manage to grab the edge of the chasm, though you get hurt in the process.\n"
                      "You get up, check your wounds, and resume your journey.")
                break
            elif choice == 2:
                if random.random() > 0.5:
                    print("You slowly get to the other side of a chasm.\n"
                          "Though stressful, the journey left you unscrached.\n")
                    break
                else:
                    player.add_card_do_deck(cardsFile.Depression())
                    print("The journey through the bridge is long and tiring.\n"
                          "When you get on the other side, you're beyond exhausted.\n"
                          "Yet, the further road awaits...\n")
                    break
            else:
                print("Wrong input!")
