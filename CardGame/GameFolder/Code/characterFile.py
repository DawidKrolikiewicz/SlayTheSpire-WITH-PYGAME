import pygame.sprite
import ongoingFile as o

pygame.font.init()
text_font = pygame.font.Font("../Fonts/Kreon-Regular.ttf", 20)


class Character(pygame.sprite.Sprite):
    def __init__(self, name, health):
        # GAMEPLAY RELATED
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.max_health = health
        self.cur_health = health
        self.armor = 0
        self.list_of_ongoing = [o.Strength(), o.Dexterity(), o.Frail(), o.Vulnerable()]

        # DISPLAY RELATED
        self.image_sprite = pygame.image.load("../Sprites/Characters/Don'tMakeInstancesOfBaseEnemyPLS.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.image_name = text_font.render(self.name, True, (0, 0, 0))
        self.rect_name = self.image_name.get_rect()
        self.rect_name.top = self.rect_sprite.bottom + 4

        self.image_hp = text_font.render(f"[{self.armor}] {self.cur_health} / {self.max_health} HP", True,
                                         (0, 0, 0))
        self.rect_hp = self.image_hp.get_rect()
        self.rect_hp.top = self.rect_name.bottom + 4

        self.rect_ongoing = (0, 0, 0, 0)
        self.ongoing_counter = 0

    def event_listener(self, ev, list_of_enemies):
        for ongoing in self.list_of_ongoing:
            ongoing.event_listener(ev, self, list_of_enemies)

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

        # ONGOING EFFECTS
        self.ongoing_counter = 0
        for ongoing in self.list_of_ongoing:
            if (ongoing.counter is not None and ongoing.counter > 0) or (ongoing.duration is not None and ongoing.duration > 0) or (
                    ongoing.intensity is not None and ongoing.intensity != 0):
                self.ongoing_counter += 1

        self.rect_ongoing = pygame.Rect(0, 0, self.ongoing_counter * 30, 30)
        self.rect_ongoing.centerx = self.rect_sprite.centerx
        self.rect_ongoing.top = self.rect_hp.bottom + 4
        self.ongoing_counter -= 1

        pygame.draw.rect(screen, (150, 150, 150), self.rect_ongoing)
        for ongoing in self.list_of_ongoing:
            ongoing.update(self, screen)

    def info(self):
        print(f">>  {self.name}'s info is being displayed!")
        print(f"    Health: {self.cur_health} / {self.max_health}")
        print(f"    Armor: {self.armor}")
        for ongoing in self.list_of_ongoing:
            if ongoing.duration is not None and ongoing.duration != 0:
                print(f"    {ongoing.__class__.__name__}: {ongoing.duration}")
            elif ongoing.intensity is not None and ongoing.intensity != 0:
                print(f"    {ongoing.__class__.__name__}: {ongoing.intensity}")
            elif ongoing.counter is not None and ongoing.counter != 0:
                print(f"    {ongoing.__class__.__name__}: {ongoing.counter}")

    def deal_damage(self, base_damage_value, target):
        damage = base_damage_value + self.list_of_ongoing[0].intensity
        if target.list_of_ongoing[3].duration > 0:
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
        target.armor += int((armor + self.list_of_ongoing[1].intensity) / (1.5 if self.list_of_ongoing[2].duration > 0 else 1))

    def heal(self, value, target):
        target.cur_health += value
        if target.cur_health > target.max_health:
            target.cur_health = target.max_health

    def add_str(self, value, target):
        target.list_of_ongoing[0].intensity += value

    def add_dex(self, value, target):
        target.list_of_ongoing[1].intensity += value

    def add_frai(self, value, target):
        target.list_of_ongoing[2].duration += value

    def add_vuln(self, value, target):
        target.list_of_ongoing[3].duration += value
