import random
import pygame.image
import characterFile
import roomsFile
import cardsFile
import ongoingFile as o
import animationsFile
import fontsFile

ON_CARD_EXHAUSTED = pygame.USEREVENT + 1
ON_STATUS_CARD_DRAWN = pygame.USEREVENT + 2
ON_CURSE_CARD_DRAWN = pygame.USEREVENT + 3
ON_PLAYER_ATTACKED = pygame.USEREVENT + 4
ON_ATTACK_PLAYED = pygame.USEREVENT + 5
ON_PLAYER_LOSE_HP_FROM_CARD = pygame.USEREVENT + 6
ON_SKILL_PLAYED = pygame.USEREVENT + 7
ON_PLAYER_GAIN_BLOCK = pygame.USEREVENT + 8
ON_TURN_END = pygame.USEREVENT + 9
ON_TURN_START = pygame.USEREVENT + 10


class Player(characterFile.Character):
    def __init__(self, name, health, starting_deck):
        super().__init__(name, health)
        # RUN RELATED
        self.fight_count = 0
        self.floor = 0
        self.coins = 50
        self.run_deck = starting_deck
        # COMBAT RELATED
        self.max_hand_size = 10
        self.deck = []
        self.hand = []
        self.discard = []
        self.mana = 3
        self.current_room = roomsFile.Menu(None)
        self.highlight = None
        self.drag = None

        # VISUAL RELATED
        self.image_sprite = pygame.image.load("../Sprites/Characters/Player.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 350
        self.rect_sprite.centerx = 250

        self.image_mana = characterFile.text_font.render(f"{self.mana} / 3", True, (0, 0, 0))
        self.rect_mana = self.image_mana.get_rect()
        self.rect_mana.midbottom = self.rect_sprite.midtop - pygame.Vector2(0, 4)

    def event_listener(self, ev, player, list_of_enemies):
        super().event_listener(ev, player, list_of_enemies)

    def update(self, screen):
        super().update(screen)

        # DRAWING PLAYER MANA
        self.image_mana = fontsFile.text_font_big.render(f"{self.mana} / 3", True, (255, 255, 255))
        self.rect_mana = self.image_mana.get_rect()
        outline_mana = pygame.rect.Rect(0, 0, self.rect_mana.width + 4, self.rect_mana.height + 4)
        self.rect_mana.midbottom = self.rect_sprite.midtop - pygame.Vector2(0, 4)
        outline_mana.center = self.rect_mana.center

        pygame.draw.rect(screen, (255, 0, 0), outline_mana)
        fill = self.mana / 3
        if fill > 1:
            fill = 1
        self.rect_mana.width = self.rect_mana.width * fill
        pygame.draw.rect(screen, (48, 33, 209), self.rect_mana)
        screen.blit(self.image_mana, self.rect_mana.topleft)

    def info(self):
        super().info()
        print(f"    Mana: {self.mana}")
        print(f"    Coins: {self.coins} ")
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

    def play_card(self, player, list_of_enemies, target, card, use_mana=True):
        if len(self.hand) < 1:
            print(f">>  {self.name}'s hand is EMPTY!")
        else:
            print(f">>  {self.name} is playing a card:")

            if o.Effect.CORRUPTION in self.dict_of_ongoing and card.type == cardsFile.CardType.SKILL:
                card.cost = 0
                card.exhaust = True

            if o.Effect.ENTANGLED in self.dict_of_ongoing and card.type == cardsFile.CardType.ATTACK:
                if self.dict_of_ongoing[o.Effect.ENTANGLED].value > 0:
                    return

            if card.cost <= self.mana or use_mana is False:
                if use_mana is True:
                    self.mana -= card.cost

                for enemy in list_of_enemies:
                    if o.Effect.ENRAGE in enemy.dict_of_ongoing and card.type == cardsFile.CardType.SKILL:
                        enemy.add_strength(enemy.dict_of_ongoing[o.Effect.ENRAGE].value, enemy)

                if card.type == cardsFile.CardType.POWER:
                    self.remove_card(card)
                elif not card.exhaust:
                    self.discard_card(card)
                elif card.exhaust:
                    self.exhaust_card(card)
                else:
                    print("There is some CRITICAL error here D:")

                if card.type == cardsFile.CardType.ATTACK:
                    pygame.event.post(pygame.event.Event(ON_ATTACK_PLAYED))

                card.action(player, list_of_enemies, target)

                if (o.Effect.DOUBLE_TAP in self.dict_of_ongoing and card.type == cardsFile.CardType.ATTACK and
                        self.dict_of_ongoing[o.Effect.DOUBLE_TAP].counter > 0):
                    card.action(player, list_of_enemies, target)
                    self.dict_of_ongoing[o.Effect.DOUBLE_TAP].counter -= 1

                card.reset_card_position()
            else:
                print(f"Not enough mana to play {card.name}!")

    def shuffle_deck(self):
        print(f">>  {self.name} is shuffling the deck!")
        random.shuffle(self.deck)

    def draw_card(self, how_much):
        if o.Effect.NO_DRAW in self.dict_of_ongoing and self.dict_of_ongoing[o.Effect.NO_DRAW].duration > 0:
            return

        return_card = None
        for i in range(how_much):
            if not self.deck and not self.discard:
                break

            elif not self.deck and self.discard:
                self.deck += self.discard
                self.discard.clear()
                self.shuffle_deck()

            if len(self.hand) <= self.max_hand_size:
                card_drawn = self.deck.pop(0)
                self.hand.append(card_drawn)
                if card_drawn.type == cardsFile.CardType.STATUS:
                    pygame.event.post(pygame.event.Event(ON_STATUS_CARD_DRAWN))
                elif card_drawn.type == cardsFile.CardType.CURSE:
                    pygame.event.post(pygame.event.Event(ON_CURSE_CARD_DRAWN))
                return_card = card_drawn

        return return_card

    def deal_damage(self, damage, target, is_attack=True, hit_block=True):
        super().deal_damage(damage, target)
        if target == self and damage > 0:
            # Post event
            pygame.event.post(pygame.event.Event(ON_PLAYER_LOSE_HP_FROM_CARD))

        return damage

    def add_block(self, value, target, affected_by_ongoing=True):
        super().add_block(value, target)
        if target == self:
            # Post event
            pygame.event.post(pygame.event.Event(ON_PLAYER_GAIN_BLOCK))

    def add_card_to_deck(self, card):
        self.deck.append(card)

    def add_card_to_run_deck(self, card):
        self.run_deck.append(card)

    def remove_card_from_run_deck(self, card):
        card_id = id(card)
        for card in self.run_deck:
            if id(card) == card_id:
                self.run_deck.remove(card)

    def add_card_to_hand(self, card):
        if len(self.hand) <= self.max_hand_size:
            self.hand.append(card)
        return card

    def add_card_to_discard(self, card):
        self.discard.append(card)

    def discard_card(self, card):
        self.hand.remove(card)
        self.discard.append(card)
        card.reset_card_position()

    def exhaust_card(self, card):
        self.hand.remove(card)
        card.reset_card_position()
        if card.name == "Sentinel":
            self.gain_mana(2)
        pygame.event.post(pygame.event.Event(ON_CARD_EXHAUSTED))

    def remove_card(self, card):
        # (For Powers)
        self.hand.remove(card)
        card.reset_card_position()

    def gain_mana(self, how_much):
        self.mana += how_much

    def start_combat(self):
        self.deck += self.run_deck
        self.shuffle_deck()
        for card in self.deck:
            card.reset_card_position()

    def end_combat(self):
        self.fight_count += 1
        self.deck.clear()
        self.hand.clear()
        self.discard.clear()
        self.dict_of_ongoing.clear()
        self.anim_list.clear()
        if self.cur_health > 0:
            self.heal(6, self)

    def start_turn(self):
        self.mana = 3
        if o.Effect.BARRICADE not in self.dict_of_ongoing:
            self.block = 0

        if o.Effect.BERSERK in self.dict_of_ongoing:
            self.gain_mana(self.dict_of_ongoing[o.Effect.BERSERK].intensity)

        if o.Effect.BRUTALITY in self.dict_of_ongoing:
            self.deal_damage(1, self, is_attack=False, hit_block=False)
            self.draw_card(self.dict_of_ongoing[o.Effect.BRUTALITY].intensity)

        super().start_turn()
        self.draw_card(5)

    def end_turn(self):
        super().end_turn()
        self.drag = None
        while self.hand:
            if self.hand[0].name == "Burn":
                self.deal_damage(2, self, is_attack=False)

            if not self.hand[0].ethereal:
                self.discard_card(self.hand[0])
            else:
                self.exhaust_card(self.hand[0])
        pygame.event.post(pygame.event.Event(ON_TURN_END))
        if o.Effect.METALLICIZE in self.dict_of_ongoing and self.dict_of_ongoing[o.Effect.METALLICIZE].intensity > 0:
            self.add_block(self.dict_of_ongoing[o.Effect.METALLICIZE].intensity, self)

