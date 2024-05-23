import random
import characterFile
import roomsFile


class Player(characterFile.Character):
    def __init__(self, name, health, starting_deck):
        super().__init__(name, health)
        self.deck = starting_deck
        self.hand = []
        self.discard = []
        self.mana = 3
        self.coins = 40
        self.current_room = roomsFile.Menu(None)
        self.drag = None

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

    def add_card_do_deck(self, card):
        # NOT USED CURRENTLY
        self.deck.append(card)

    def shuffle_deck(self):
        print(f">>  {self.name} is shuffling the deck!")
        random.shuffle(self.deck)

    def draw_card(self, how_much):
        for i in range(how_much):
            if not self.deck and not self.discard:
                break
            #               print(f">> CAN'T DRAW: BOTH DECK AND DISCARD ARE EMPTY")

            elif not self.deck and self.discard:
                self.deck += self.discard
                self.discard.clear()
                self.shuffle_deck()

            #            print(f">> {self.name} is drawing a card!")
            card_drawn = self.deck.pop(0)
            self.hand.append(card_drawn)

    #        print(f"==============================================================================")

    def play_card(self, player, list_of_enemies, index):
        if len(self.hand) < 1:
            print(f">>  {self.name}'s hand is EMPTY!")
        else:
            print(f">>  {self.name} is playing a card:")
#            for i in range(len(self.hand)):
#                print(f"{i}) {self.hand[i].name}[{self.hand[i].cost}]")

            index_picked = index
            if self.hand[index_picked].cost <= self.mana:
                card_picked = self.hand[index_picked]
                print(f">>  Playing {card_picked.name} from hand!")
                self.mana -= card_picked.cost
                self.hand.pop(index_picked)
                card_picked.action(player, list_of_enemies)
                self.discard.append(card_picked)
            else:
                print(f">>  Not enough mana to play {self.hand[index_picked].name}!")

    def discard_card(self, card):
        self.hand.remove(card)
        self.discard.append(card)

    def start_turn(self):
        self.armor = 0
        self.draw_card(5)
        self.mana = 3

    def end_turn(self):
        if self.fragility > 0:
            self.fragility -= 1
        if self.vulnerability > 0:
            self.vulnerability -= 1
        while self.hand:
            self.discard_card(self.hand[0])
        print(f">>  {self.name} is ENDING THEIR TURN:")
