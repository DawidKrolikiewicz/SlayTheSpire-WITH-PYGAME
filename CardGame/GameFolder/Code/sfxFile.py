import pygame

pygame.mixer.pre_init(44100, -16, 6, 512)
pygame.mixer.init()

damage_1 = pygame.mixer.Sound("../Sound Effects/Damage1.mp3")
damage_2 = pygame.mixer.Sound("../Sound Effects/Damage2.mp3")
damage_3 = pygame.mixer.Sound("../Sound Effects/Damage3.mp3")
damages = (damage_1, damage_2, damage_3)

damage_blocked_1 = pygame.mixer.Sound("../Sound Effects/DamageBlocked1.mp3")
damage_blocked_2 = pygame.mixer.Sound("../Sound Effects/DamageBlocked2.mp3")
damage_blocked_3 = pygame.mixer.Sound("../Sound Effects/DamageBlocked3.mp3")
damages_blocked = (damage_blocked_1, damage_blocked_2, damage_blocked_3)

block_gained = pygame.mixer.Sound("../Sound Effects/BlockGained.mp3")

heal_1 = pygame.mixer.Sound("../Sound Effects/Heal1.mp3")
heal_2 = pygame.mixer.Sound("../Sound Effects/Heal2.mp3")
heal_3 = pygame.mixer.Sound("../Sound Effects/Heal3.mp3")
heals = (heal_1, heal_2, heal_3)


card_played = pygame.mixer.Sound("../Sound Effects/CardPlayed.mp3")
card_exhausted = pygame.mixer.Sound("../Sound Effects/CardExhausted.mp3")
power_played = pygame.mixer.Sound("../Sound Effects/PowerPlayed.mp3")
