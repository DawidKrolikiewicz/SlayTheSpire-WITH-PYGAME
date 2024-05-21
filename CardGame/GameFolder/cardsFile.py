
# ======================= CardBase =======================
class CardBase:
    def __init__(self):
        self.name = self.__class__.__name__
        self.cost = 99
        self.text = "There is no text here!"
        self.price_range = (0, 0)
        self.weight = 0

    def action(self, player, list_of_enemies):
        print(f"CardBase action executing!")


# ======================= Card1 =======================

class Draw2Heal3(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.text = "There is no text here!"
        self.price_range = (30, 40)
        self.weight = 1

    def action(self, player, list_of_enemies):
        player.heal(3, player)
        player.draw_card(2)


# ======================= Card2 =======================

class Deal5Damage(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.text = "There is no text here!"
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies):
        # TEMP SOLUTION: ALWAYS TARGETS FIRST ENEMY RN (Should be able to choose in future)
        player.deal_damage(5, list_of_enemies[0])


# ======================= Card3 =======================

class Draw1(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.text = "There is no text here!"
        self.price_range = (18, 25)
        self.weight = 2

    def action(self, player, list_of_enemies):
        player.draw_card(1)


# ======================= Card4 =======================

class Armor4(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.text = "There is no text here!"
        self.price_range = (15, 20)
        self.weight = 3

    def action(self, player, list_of_enemies):
        player.add_armor(4, player)


# ======================= Card5 =======================

class Buff(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.text = "There is no text here!"
        self.price_range = (25, 35)
        self.weight = 1

    def action(self, player, list_of_enemies):
        player.add_dex(1, player)
        player.add_str(1, player)


# ======================= Card6 =======================

class Debuff(CardBase):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.text = "There is no text here!"
        self.price_range = (18, 25)
        self.weight = 2

    def action(self, player, list_of_enemies):
        # TEMP SOLUTION: ALWAYS TARGETS FIRST ENEMY RN (Should be able to choose in future)
        player.add_frag(1, list_of_enemies[0])
        player.add_vuln(1, list_of_enemies[0])


# ======================= Card6 =======================

class KYS(CardBase):  # Testing purposes card
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.text = "There is no text here!"

    def action(self, player, list_of_enemies):
        player.deal_damage(99, player)


