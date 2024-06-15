import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

Damage = pygame.mixer.Sound("../Sound Effects/Damage.mp3")
DamageBlocked = pygame.mixer.Sound("../Sound Effects/DamageBlocked.mp3")
BlockGained = pygame.mixer.Sound("../Sound Effects/BlockGained.mp3")