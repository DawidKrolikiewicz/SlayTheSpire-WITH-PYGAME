import pygame
import random
import enemyFile

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

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
        self.menu_button_rect = pygame.Rect((500, 0, 100, 100))
        self.menu_button_color = WHITE
        pygame.display.set_caption("INGAME")

    def event_listener(self, ev, player):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.menu_button_rect.collidepoint(pos):
                player.current_room = Menu(player.current_room)

    def update(self, screen, player):
        screen.fill(self.bg_color)
        pygame.draw.rect(screen, self.menu_button_color, self.menu_button_rect)


# ======================================================================================================================

class CombatEncounter(InGame):
    def __init__(self):
        super().__init__()
        self.bg_color = BLUE
        self.enemy = None
        pygame.display.set_caption("COMBAT ENCOUNTER")

    def event_listener(self, ev, player):
        super().event_listener(ev, player)
        if self.state == 2:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_i:
                    player.info()
                    player.current_room.enemy.info()
                if ev.key == pygame.K_1:
                    player.play_card(player, [player.current_room.enemy], 0)
                if ev.key == pygame.K_2:
                    player.play_card(player, [player.current_room.enemy], 1)
                if ev.key == pygame.K_3:
                    player.play_card(player, [player.current_room.enemy], 2)
                if ev.key == pygame.K_4:
                    player.play_card(player, [player.current_room.enemy], 3)
                if ev.key == pygame.K_5:
                    player.play_card(player, [player.current_room.enemy], 4)
                if ev.key == pygame.K_6:
                    player.play_card(player, [player.current_room.enemy], 5)
                if ev.key == pygame.K_7:
                    player.play_card(player, [player.current_room.enemy], 6)
                if ev.key == pygame.K_8:
                    player.play_card(player, [player.current_room.enemy], 7)
                if ev.key == pygame.K_9:
                    player.play_card(player, [player.current_room.enemy], 8)
                if ev.key == pygame.K_0:
                    player.play_card(player, [player.current_room.enemy], 9)

    def update(self, screen, player):
        # Executes every frame
        super().update(screen, player) # Fill background color AND Draw Go-To-Menu Rect

        button_rect = pygame.Rect((250, 200, 100, 100))
        pygame.draw.rect(screen, BLACK, button_rect)
        if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            print(f"END TURN")
            self.state = 3

        if self.state == 0:
            # COMBAT START
            pygame.display.set_caption('COMBAT')
            player.shuffle_deck()
            enemy_name = random.choice(["Angry Arthur", "Bad Brad", "Cruel Cooper", "Devious Dominick"])
            enemy_health = random.randint(1, 16)
            self.enemy = enemyFile.Enemy1(enemy_name, enemy_health)
            self.state = 1

        if self.state == 1:
            # ROUND START
            player.draw_card(5)
            player.mana = 3
            self.enemy.declare_action(player, [self.enemy])
            print(f">>--------------------------------------------------------------------------<<")
            player.info()
            self.enemy.info()
            self.state = 2

        if self.state == 2:
            # PLAYER ACTIONS TURN
            if player.health <= 0:
                print(f">> (((  LOSE  )))")
                self.enemy = None
                current_room = Menu(None)
                player.health = 25
            elif all(enemy.health <= 0 for enemy in [self.enemy]):
                print(f">> (((  WIN!  )))")
                self.enemy = None
                current_room = Menu(None)
                player.health = 25
            pass

        if self.state == 3:
            # END TURN
            print(f">>--------------------------------------------------------------------------<<")
            self.enemy.play_action(player, [self.enemy])
            player.end_turn()
            pygame.time.wait(2000)
            print(f">>--------------------------------------------------------------------------<<")
            self.state = 1


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


