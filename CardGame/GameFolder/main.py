import random
import pygame
import playerFile
import cardsFile
import enemyFile
import roomsFile

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


# ======================================================================================================================

class Test(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale_by(pygame.image.load("Cards/Depression.png"), 1)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.movex = 1
        self.movey = 1

    def update(self):
        if self.rect.top <= 0:
            self.movey = 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.movey = -1
        if self.rect.left <= 0:
            self.movex = 1
        if self.rect.right >= SCREEN_WIDTH:
            self.movex = -1

        self.x = self.x + self.movex
        self.y = self.y + self.movey
        self.rect.topleft = (self.x, self.y)
        pass

    def draw(self, surface):
        pygame.draw.rect(SCREEN, BLACK, self.rect)
        surface.blit(self.image, (self.x, self.y))


# ======================================================================================================================

is_running = True

test_group = pygame.sprite.Group()

test_1 = Test(55, 103)
test_2 = Test(400, 100)
test_group.add(test_1)
test_group.add(test_2)

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

#   test_group.update()
    test_1.update()
    test_1.draw(SCREEN)
#   test_2.draw(SCREEN)

    # UPDATING THE DISPLAY
    pygame.display.update()

    # Setting Frames per Second
    timer.tick(60)
    # Display actual FPS
    # print(int(timer.get_fps()))

pygame.quit()
