import random
import pygame
import playerFile
import cardsFile
import enemyFile
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

TO_ROOM = pygame.USEREVENT + 1
TO_COMBAT = pygame.USEREVENT + 2
TO_SHOP = pygame.USEREVENT + 3
DISPLAY_INFO = pygame.USEREVENT + 4

timer = pygame.time.Clock()

PLAYER_NAME = "VictoriousGuy"
STARTING_HEALTH = 70
STARTING_DECK = [cardsFile.Draw2Heal3(), cardsFile.Draw2Heal3(),
                 cardsFile.Deal5Damage(), cardsFile.Deal5Damage(),
                 cardsFile.Draw1(), cardsFile.Draw1(),
                 cardsFile.Armor4(), cardsFile.Armor4(),
                 cardsFile.Buff(), cardsFile.Debuff(), cardsFile.Juggernaut()]

PLAYER = playerFile.Player(PLAYER_NAME, STARTING_HEALTH, STARTING_DECK)

# ======================================================================================================================

is_running = True

test_card = cardsFile.CardBase()

scene = 1

while is_running:
    # =========== CHECK ALL EVENTS ===========
    for event in pygame.event.get():
        # ===========    QUIT EVENTS   ===========
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            is_running = False
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
