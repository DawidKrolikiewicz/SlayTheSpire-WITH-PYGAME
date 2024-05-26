import pygame.sprite

pygame.font.init()
text_font = pygame.font.SysFont("Comic Sans MS", 18)


class Character(pygame.sprite.Sprite):
    def __init__(self, name, health):
        # GAMEPLAY RELATED
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.max_health = health
        self.cur_health = health
        self.armor = 0
        self.strength = 0
        self.vulnerability = 0
        self.dexterity = 0
        self.fragility = 0

        # DISPLAY RELATED
        self.image_sprite = pygame.image.load("Enemies/Don'tMakeInstancesOfBaseEnemyPLS.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 370

        self.image_name = text_font.render(self.name, True, (0, 0, 0))
        self.rect_name = self.image_name.get_rect()
        self.rect_name.top = self.rect_sprite.bottom + 4

        self.image_hp = text_font.render(f"[{self.armor}] {self.cur_health} / {self.max_health} HP", True,
                                         (0, 0, 0))
        self.rect_hp = self.image_hp.get_rect()
        self.rect_hp.top = self.rect_name.bottom + 4

    def update(self, screen):
        # DRAWING CHARACTER SPRITE
        pygame.draw.rect(screen, (255, 0, 0), self.rect_sprite)
        screen.blit(self.image_sprite, self.rect_sprite.topleft)

        # DRAWING CHARACTER NAME
        self.rect_name.centerx = self.rect_sprite.centerx
        pygame.draw.rect(screen, (0, 100, 255), self.rect_name)
        screen.blit(self.image_name, self.rect_name.topleft)

        # DRAWING CHARACTER HP
        self.image_hp = text_font.render(f"[{self.armor}] {self.cur_health} / {self.max_health} HP", True,
                                         (0, 0, 0))
        self.rect_hp.centerx = self.rect_sprite.centerx
        pygame.draw.rect(screen, (0, 100, 255), self.rect_hp)
        screen.blit(self.image_hp, self.rect_hp.topleft)

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
        if target.cur_health > target.max_health:
            target.cur_health = target.max_health

    def add_str(self, value, target):
        target.strength += value

    def add_dex(self, value, target):
        target.dexterity += value

    def add_frag(self, value, target):
        target.fragility += value

    def add_vuln(self, value, target):
        target.vulnerability += value
