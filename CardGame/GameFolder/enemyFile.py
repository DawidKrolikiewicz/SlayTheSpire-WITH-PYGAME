import random

import pygame

import characterFile


class Enemy(characterFile.Character):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.list_of_actions = []
        self.next_action = None

        #self.image = pygame.image.load("Enemies/frog.png")
        self.rect = pygame.Rect((0, 0, 100, 100))

    def update(self, screen, player):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        #screen.blit(self.image, self.rect.topleft)

    def declare_action(self, player, list_of_enemies):
        if self.list_of_actions:
            self.next_action = self.list_of_actions[random.randint(0, len(self.list_of_actions) - 1)]
            print(f">>  {self.name}'s Next Action: {self.next_action.__name__}")
        else:
            print(f">>  THIS ENEMY DOESNT HAVE ANY ACTIONS!!!")

    def play_action(self, player, list_of_enemies):
        self.next_action(player, list_of_enemies)


class Enemy1(Enemy):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.list_of_actions = [self.attack_6, self.gain_6_armor, self.give_1_vuln]

    def attack_6(self, player, list_of_enemies):
        print(f">>  {self.name} attacks!")
        self.deal_damage(6, player)

    def gain_6_armor(self, player, list_of_enemies):
        print(f">>  {self.name} puts up his defences!")
        self.add_armor(6, self)

    def give_1_vuln(self, player, list_of_enemies):
        print(f">>  {self.name} makes you more vulnerable!")
        self.add_vuln(1, player)


class Frog(Enemy):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.image = pygame.image.load("/Enemies/frog.png")
        self.rect = self.image.get_rect()

    def update(self, screen, player):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        screen.blit(self.image, self.rect.topleft)

