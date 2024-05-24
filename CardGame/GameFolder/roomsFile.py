import pygame
import random
import enemyFile

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
                if self.last_room is None:
                    # Start New Run
                    player.current_room = CombatEncounter()
                    for i in range(25):
                        print(f"")
                else:
                    # Continue Current Run
                    player.current_room = self.last_room
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
                player.current_room = Menu(player.current_room)

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
        self.bg_enemy_rect = pygame.Rect((683, 0, 683, 528))
        self.bg_hand_color = PURPLE
        self.bg_hand_rect = pygame.Rect((0, 528, 1366, 240))

        self.end_turn_color = BLACK
        self.end_turn_rect = pygame.Rect((1266, 668, 100, 100))

        self.list_of_enemies = []
        self._generate_enemies()

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
        for card in player.hand:
            card.event_listener(ev, player, self.list_of_enemies, self.bg_play_rect)

    def update(self, screen, player):
        # Draw backgrounds Rects
        pygame.draw.rect(screen, self.bg_play_color, self.bg_play_rect)
        pygame.draw.rect(screen, self.bg_enemy_color, self.bg_enemy_rect)
        pygame.draw.rect(screen, self.bg_hand_color, self.bg_hand_rect)

        # Draw Go-To-Menu Rect
        super().update(screen, player)

        # Draw End-of-turn Rect
        pygame.draw.rect(screen, self.end_turn_color, self.end_turn_rect)

        # Update every enemy
        for enemy in self.list_of_enemies:
            enemy.update(screen, player)

        # Update every card in hand
        for card in player.hand:
            card.update(screen, player, self.bg_hand_rect)

        if self.state == 0:
            # COMBAT START
            player.shuffle_deck()
            self.state = 1

        if self.state == 1:
            # ROUND START
            player.draw_card(5)
            player.mana = 3
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
                if enemy.health <= 0:
                    self.list_of_enemies.remove(enemy)
                    print(f"Enemy {enemy.name} is DEAD!")

            if player.health <= 0:
                print(f">> (((  LOSE  )))")
                player.current_room = Menu(None)
                player.health = 25
            elif all(enemy.health <= 0 for enemy in self.list_of_enemies):
                print(f">> (((  WIN!  )))")
                player.current_room = Menu(None)
                player.health = 25
            pass

        if self.state == 3:
            # END TURN
            print(f">>--------------------------------------------------------------------------<<")
            for enemy in self.list_of_enemies:
                enemy.play_action(player, self.list_of_enemies)

            player.end_turn()
            pygame.time.wait(2000)
            print(f">>--------------------------------------------------------------------------<<")
            self.state = 1

    def _generate_enemies(self):
        # ENEMY GENERATOR
        number_of_enemies = random.randint(1, 4)
        offset = 683 // (number_of_enemies + 1)
        enemy_names = ["Angry Arthur", "Bad Brad", "Cruel Cooper", "Devious Dominick"]
        for i in range(number_of_enemies):
            random.shuffle(enemy_names)
            enemy_name = enemy_names.pop()
            enemy_health = random.randint(4, 10)
            enemy = enemyFile.Enemy1(enemy_name, enemy_health)
            enemy.x = (i + 1) * offset + 683
            enemy.y = 300
            print(enemy.name)
            self.list_of_enemies.append(enemy)


# ======================================================================================================================

class Shop(InGame):
    def __init__(self):
        super().__init__()
        self.bg_color = GREEN
        pygame.display.set_caption("SHOP")

    def update(self, screen, player):
        super().update(screen, player)
        pass


# ======================================================================================================================


