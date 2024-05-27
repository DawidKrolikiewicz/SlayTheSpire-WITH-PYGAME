import random
import pygame.image
import characterFile
import roomsFile

ON_CARD_EXHAUSTED = pygame.USEREVENT + 1
ON_STATUS_CARD_DRAWN = pygame.USEREVENT + 2
ON_STATUS_OR_CURSE_CARD_DRAWN = pygame.USEREVENT + 3
ON_PLAYER_ATTACKED = pygame.USEREVENT + 4
ON_ATTACK_PLAYED = pygame.USEREVENT + 5
ON_PLAYER_LOSE_HP_FROM_CARD = pygame.USEREVENT + 6
ON_SKILL_PLAYER = pygame.USEREVENT + 7
ON_PLAYER_GAIN_BLOCK = pygame.USEREVENT + 8
ON_TURN_END = pygame.USEREVENT + 9
ON_TURN_START = pygame.USEREVENT + 10

class Player(characterFile.Character):
    def __init__(self, name, health, starting_deck):
        super().__init__(name, health)
        self.run_deck = starting_deck
        self.max_hand_size = 10
        self.deck = []
        self.hand = []
        self.discard = []
        self.mana = 3
        self.coins = 40
        self.current_room = roomsFile.Menu(None)
        self.highlight = None
        self.drag = None
        self.buffs = []

        self.image_sprite = pygame.image.load("Enemies/player.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 370
        self.rect_sprite.centerx = 250

        self.image_mana = characterFile.text_font.render(f"{self.mana} / 3", True, (0, 0, 0))
        self.rect_mana = self.image_mana.get_rect()
        self.rect_mana.midbottom = self.rect_sprite.midtop - pygame.Vector2(0, 4)

    def event_listener(self, ev, list_of_enemies):
        for buff in self.buffs:
            buff.event_listener(ev, self, list_of_enemies)

    def update(self, screen):
        super().update(screen)

        # DRAWING PLAYER MANA
        self.image_mana = characterFile.text_font.render(f"{self.mana} / 3", True, (0, 0, 0))
        self.rect_mana = self.image_mana.get_rect()
        self.rect_mana.midbottom = self.rect_sprite.midtop - pygame.Vector2(0, 4)
        pygame.draw.rect(screen, (255, 0, 0), self.rect_mana)
        screen.blit(self.image_mana, self.rect_mana.topleft)

    def info(self):
        super().info()
        print(f"    Mana: {self.mana}")
        print(f"    Deck: ", end="")
        for card in self.deck:
            print(f"{card.name}[{card.cost}]", end=" / ")
        print()
        print(f"    Hand: ", end="")
        for card in self.hand:
            print(f"{card.name}[{card.cost}]", end=" / ")
        print()
        print(f"    Discard: ", end="")
        for card in self.discard:
            print(f"{card.name}[{card.cost}]", end=" / ")
        print()

    def play_card(self, player, list_of_enemies, target, card):
        if len(self.hand) < 1:
            print(f">>  {self.name}'s hand is EMPTY!")
        else:
            print(f">>  {self.name} is playing a card:")

            if card.cost <= self.mana:
                pygame.event.post(pygame.event.Event(ON_ATTACK_PLAYED))
                self.mana -= card.cost

                card.action(player, list_of_enemies, target)
                card.reset_card_position()
                if not card.exhaust:
                    self.discard_card(card)
                else:
                    self.exhaust_card(card)
                # Post event

            else:
                print(f"Not enough mana to play {card.name}!")

    def shuffle_deck(self):
        print(f">>  {self.name} is shuffling the deck!")
        random.shuffle(self.deck)

    def draw_card(self, how_much):
        for i in range(how_much):
            if not self.deck and not self.discard:
                break

            elif not self.deck and self.discard:
                self.deck += self.discard
                self.discard.clear()
                self.shuffle_deck()

            card_drawn = self.deck.pop(0)
            self.hand.append(card_drawn)

    def deal_damage(self, base_damage_value, target):
        super().deal_damage(base_damage_value, target)
        if target == self:
            # Post event
            pygame.event.post(pygame.event.Event(ON_PLAYER_LOSE_HP_FROM_CARD))

    def add_card_to_deck(self, card):
        self.deck.append(card)

    def add_card_to_hand(self, card):
        if len(self.hand) <= self.max_hand_size:
            self.hand.append(card)

    def add_card_to_discard(self, card):
        self.discard.append(card)

    def discard_card(self, card):
        self.hand.remove(card)
        self.discard.append(card)
        card.reset_card_position()

    def exhaust_card(self, card):
        self.hand.remove(card)
        card.reset_card_position()

    def gain_mana(self, how_much):
        self.mana += how_much

    def start_combat(self):
        self.deck += self.run_deck
        self.shuffle_deck()

    def end_combat(self):
        self.deck.clear()
        self.hand.clear()
        self.discard.clear()
        self.strength = 0
        self.dexterity = 0
        self.fragility = 0
        self.vulnerability = 0

    def start_turn(self):
        self.armor = 0
        self.draw_card(5)
        self.mana = 3

    def end_turn(self):
        self.drag = None
        if self.fragility > 0:
            self.fragility -= 1
        if self.vulnerability > 0:
            self.vulnerability -= 1
        while self.hand:
            self.discard_card(self.hand[0])
        print(f">>  {self.name} is ENDING THEIR TURN:")
