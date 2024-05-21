import random
import os
import pygame
import playerFile
import cardsFile
import enemyFile

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode((600, 500))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

TO_ROOM = pygame.USEREVENT + 1
TO_COMBAT = pygame.USEREVENT + 2
TO_SHOP = pygame.USEREVENT + 3
DISPLAY_INFO = pygame.USEREVENT + 4

timer = pygame.time.Clock()
pygame.display.set_caption('Slay the spire clone thingy')

PLAYER_NAME = "VictoriousGuy"
STARTING_HEALTH = 25
STARTING_DECK = [cardsFile.Draw2Heal3(), cardsFile.Draw2Heal3(),
                 cardsFile.Deal5Damage(), cardsFile.Deal5Damage(),
                 cardsFile.Draw1(), cardsFile.Draw1(),
                 cardsFile.Armor4(), cardsFile.Armor4(),
                 cardsFile.Buff(), cardsFile.Debuff(), cardsFile.KYS()]

PLAYER = playerFile.Player(PLAYER_NAME, STARTING_HEALTH, STARTING_DECK)


# --------------------------------------------------------

class Room:
    def __init__(self):
        self.bg_color = RED
        self.menu_rect = pygame.Rect((500, 0, 100, 100))
        self.state = 0

    #        self.room_rect = pygame.Rect((0, 0, 200, 50))
    #        self.combat_rect = pygame.Rect((200, 0, 200, 50))
    #        self.shop_rect = pygame.Rect((400, 0, 200, 50))

    def event_listener(self, ev):
        pass

    def update(self):
        if self.state == 0:
            pygame.display.set_caption('ROOM (superclass)')
            self.state = 1

        SCREEN.fill(self.bg_color)
        pygame.draw.rect(SCREEN, BLACK, self.menu_rect)


# --------------------------------------------------------

class MidMenu(Room):
    def __init__(self, last_room):
        super().__init__()
        self.bg_color = BLACK
        self.last_room = last_room

    def event_listener(self, ev):
        if ev.type == pygame.KEYDOWN:
            global current_room
            if ev.key == pygame.K_1:
                current_room = a
                current_room.state = 0
                for i in range(25):
                    print(f"")
            if ev.key == pygame.K_2:
                current_room = b
                current_room.state = 0
                for i in range(25):
                    print(f"")
            if ev.key == pygame.K_3:
                current_room = c
                current_room.state = 0
                for i in range(25):
                    print(f"")

    def update(self):
        if self.state == 0:
            pygame.display.set_caption('MIDMENU')
            self.state = 1
        pygame.draw.rect(SCREEN, self.last_room.bg_color, self.menu_rect)


# --------------------------------------------------------

class CombatEncounter(Room):
    def __init__(self):
        super().__init__()
        self.bg_color = BLUE
        self.enemy = None

    def event_listener(self, ev):
        if self.state == 2:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_i:
                    PLAYER.info()
                    current_room.enemy.info()
                if ev.key == pygame.K_1:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 0)
                if ev.key == pygame.K_2:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 1)
                if ev.key == pygame.K_3:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 2)
                if ev.key == pygame.K_4:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 3)
                if ev.key == pygame.K_5:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 4)
                if ev.key == pygame.K_6:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 5)
                if ev.key == pygame.K_7:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 6)
                if ev.key == pygame.K_8:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 7)
                if ev.key == pygame.K_9:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 8)
                if ev.key == pygame.K_0:
                    PLAYER.play_card(PLAYER, [current_room.enemy], 9)

    def update(self):
        # Executes every frame
        SCREEN.fill(self.bg_color)
        pygame.draw.rect(SCREEN, BLACK, self.menu_rect)

        button_rect = pygame.Rect((250, 200, 100, 100))
        pygame.draw.rect(SCREEN, BLACK, button_rect)
        if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            print(f"END TURN")
            self.state = 3

        if self.state == 0:
            # COMBAT START
            pygame.display.set_caption('COMBAT')
            PLAYER.shuffle_deck()
            enemy_name = random.choice(["Angry Arthur", "Bad Brad", "Cruel Cooper", "Devious Dominick"])
            enemy_health = random.randint(1, 16)
            self.enemy = enemyFile.Enemy1(enemy_name, enemy_health)
            self.state = 1

        if self.state == 1:
            # ROUND START
            PLAYER.draw_card(5)
            PLAYER.mana = 3
            self.enemy.declare_action(PLAYER, [self.enemy])
            print(f">>--------------------------------------------------------------------------<<")
            PLAYER.info()
            self.enemy.info()
            self.state = 2

        if self.state == 2:
            # PLAYER ACTIONS TURN
            global current_room
            if PLAYER.health <= 0:
                print(f">> (((  LOSE  )))")
                self.enemy = None
                current_room = MidMenu(a)
                PLAYER.health = STARTING_HEALTH
            elif all(enemy.health <= 0 for enemy in [self.enemy]):
                print(f">> (((  WIN!  )))")
                self.enemy = None
                current_room = MidMenu(a)
                PLAYER.health = STARTING_HEALTH
            pass

        if self.state == 3:
            # END TURN
            print(f">>--------------------------------------------------------------------------<<")
            self.enemy.play_action(PLAYER, [self.enemy])
            PLAYER.end_turn()
            pygame.time.wait(2000)
            print(f">>--------------------------------------------------------------------------<<")
            self.state = 1


# --------------------------------------------------------

class Shop(Room):
    def __init__(self):
        super().__init__()
        self.bg_color = GREEN

    def update(self):
        if self.state == 0:
            pygame.display.set_caption('SHOP')
            self.state = 1
        SCREEN.fill(self.bg_color)
        pygame.draw.rect(SCREEN, BLACK, self.menu_rect)


# --------------------------------------------------------

is_running = True

a = Room()
b = CombatEncounter()
c = Shop()

current_room = a

scene = 1
while is_running:
    # =========== CHECK ALL EVENTS ===========
    for event in pygame.event.get():
        # ===========    QUIT EVENTS   ===========
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            is_running = False

        # ===========  ROOM SWITCHING  ===========
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if current_room.menu_rect.collidepoint(pos):
                if current_room.__class__.__name__ != "MidMenu":
                    current_room = MidMenu(current_room)
                    print(f"Press:\n - Q to QUIT\n - I to DISPLAY DECK\n - 1 to go to ROOM (superclass)")
                    print(f" - 2 to go to COMBAT\n - 3 to go to SHOP")
                else:
                    current_room = current_room.last_room
                    current_room.state = 0
                    for i in range(20):
                        print(f"")

        # ===========   EVENT LISTEN IN THIS ROOM ONLY  ===========
        current_room.event_listener(event)

    # UPDATE EVERY FRAME
    SCREEN.fill(WHITE)

    current_room.update()

    # UPDATING THE DISPLAY
    pygame.display.update()

    # Setting Frames per Second
    timer.tick(30)

pygame.quit()
