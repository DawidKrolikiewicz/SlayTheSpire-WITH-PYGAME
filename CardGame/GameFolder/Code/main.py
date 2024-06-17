import pygame
import cardsFile
import playerFile
import sfxFile
import roomsFile

pygame.init()

# 1366 x 768
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

timer = pygame.time.Clock()

PLAYER_NAME = "VictoriousGuy"
STARTING_HEALTH = 70
STARTING_DECK = [cardsFile.Strike, cardsFile.Strike, cardsFile.Strike, cardsFile.Strike, cardsFile.Strike,
                 cardsFile.Defend, cardsFile.Defend, cardsFile.Defend, cardsFile.Defend,
                 cardsFile.Bash]

PLAYER = playerFile.Player(PLAYER_NAME, STARTING_HEALTH, [card() for card in STARTING_DECK])

# ======================================================================================================================

is_running = True

while is_running:
    # =========== CHECK ALL EVENTS ===========
    for event in pygame.event.get():
        # ===========    QUIT EVENTS   ===========
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            is_running = False
        # ====== OTHER (TESTING MAINLY ¯\_(ツ)_/¯ ) ======
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            PLAYER.floor = 16
            PLAYER.fight_count = 3
            PLAYER.end_combat()
            PLAYER.current_room = roomsFile.Rewards(roomsFile.RewardsLevel.NO_REWARDS, PLAYER)

        # ===========   EVENT LISTEN IN THIS ROOM ONLY  ===========
        PLAYER.current_room.event_listener(event, PLAYER)

    # UPDATE EVERY FRAME
    SCREEN.fill(WHITE)

    PLAYER.current_room.update(SCREEN, PLAYER)

    # UPDATING THE DISPLAY
    pygame.display.update()

    # Setting Frames per Second
    timer.tick(60)

    # Display actual FPS
    # print(int(timer.get_fps()))

pygame.quit()
