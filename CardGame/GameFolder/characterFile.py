import pygame.sprite


class Character(pygame.sprite.Sprite):
    def __init__(self, name, health):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.max_health = health
        self.cur_health = health
        self.armor = 0
        self.strength = 0
        self.vulnerability = 0
        self.dexterity = 0
        self.fragility = 0
        self.x = 0
        self.y = 0

    def info(self):
        print(f">>  {self.name}'s info is being displayed!")
        print(f"    Health: {self.cur_health} / {self.max_health}")
        print(f"    Armor: {self.armor}")
        print(f"    Buffs: S- {self.strength}, D- {self.dexterity}, V- {self.vulnerability}, F- {self.fragility}")

    def deal_damage(self, base_damage_value, target):
        damage = base_damage_value + self.strength
        if target.vulnerability > 0:
            damage = int(damage * 1.5)
        if target.armor > 0:
            if target.armor >= damage:
                target.armor -= damage
            else:
                damage -= target.armor
                target.armor = 0
                target.cur_health -= damage
        else:
            target.cur_health -= damage

    def add_armor(self, armor, target):
        target.armor += int((armor + self.dexterity) / (1.5 if self.fragility > 0 else 1))

    def heal(self, value, target):
        target.cur_health += value

    def add_str(self, value, target):
        target.strength += value

    def add_dex(self, value, target):
        target.dexterity += value

    def add_frag(self, value, target):
        target.fragility += value

    def add_vuln(self, value, target):
        target.vulnerability += value
