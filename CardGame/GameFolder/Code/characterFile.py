import pygame.sprite
import cardsFile
import ongoingFile as o
from fontsFile import text_font


class Character(pygame.sprite.Sprite):
    def __init__(self, name="PlayerName", health=70):
        # GAMEPLAY RELATED
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.max_health = health
        self.cur_health = self.max_health
        self.block = 0
        self.dict_of_ongoing = {}

        # DISPLAY RELATED
        self.image_sprite = pygame.image.load("../Sprites/Characters/Don'tMakeInstancesOfBaseEnemyPLS.png")
        self.rect_sprite = self.image_sprite.get_rect()
        self.rect_sprite.bottom = 340

        self.image_name = text_font.render(self.name, True, (0, 0, 0))
        self.rect_name = self.image_name.get_rect()
        self.rect_name.top = self.rect_sprite.bottom + 4

        self.image_hp = text_font.render(f"[{self.block}] {self.cur_health} / {self.max_health} HP", True,
                                         (0, 0, 0))
        self.rect_hp = self.image_hp.get_rect()
        self.rect_hp.top = self.rect_name.bottom + 4

        self.rect_ongoing = (0, 0, 0, 0)
        self.counter = 0

    def event_listener(self, ev, player, list_of_enemies):
        for key in self.dict_of_ongoing:
            self.dict_of_ongoing[key].event_listener(ev, self, player, list_of_enemies)

    def update(self, screen):
        # DRAWING CHARACTER SPRITE
        pygame.draw.rect(screen, (255, 0, 0), self.rect_sprite)
        screen.blit(self.image_sprite, self.rect_sprite.topleft)

        # DRAWING CHARACTER NAME
        self.rect_name.centerx = self.rect_sprite.centerx
        pygame.draw.rect(screen, (0, 100, 255), self.rect_name)
        screen.blit(self.image_name, self.rect_name.topleft)

        # DRAWING CHARACTER HP
        self.image_hp = text_font.render(f"[{self.block}] {self.cur_health} / {self.max_health} HP", True,
                                         (0, 0, 0))
        self.rect_hp = self.image_hp.get_rect()
        self.rect_hp.top = self.rect_name.bottom + 4
        self.rect_hp.centerx = self.rect_sprite.centerx
        pygame.draw.rect(screen, (0, 100, 255), self.rect_hp)
        screen.blit(self.image_hp, self.rect_hp.topleft)

        # ONGOING EFFECTS
        self.counter = 0
        for key in self.dict_of_ongoing:
            if self.dict_of_ongoing[key].value is not None and self.dict_of_ongoing[key].value != 0:
                self.counter += 1

        self.rect_ongoing = pygame.Rect(0, 0, self.counter * 30, 30)
        self.rect_ongoing.centerx = self.rect_sprite.centerx
        self.rect_ongoing.top = self.rect_hp.bottom + 4
        self.counter -= 1

        pygame.draw.rect(screen, (150, 150, 150), self.rect_ongoing)
        for key in self.dict_of_ongoing:
            self.dict_of_ongoing[key].update(self, screen)

    def info(self):
        print(f">>  {self.name}'s info is being displayed!")
        print(f"    Health: {self.cur_health} / {self.max_health}")
        print(f"    Armor: {self.block}")
        for key in self.dict_of_ongoing:
            if self.dict_of_ongoing[key].value is not None and self.dict_of_ongoing[key].value != 0:
                print(f"    {self.dict_of_ongoing[key].__class__.__name__}: {self.dict_of_ongoing[key].value}")

    def start_turn(self):
        for key in self.dict_of_ongoing:
            if self.dict_of_ongoing[key].duration is not None and self.dict_of_ongoing[key].duration > 0:
                self.dict_of_ongoing[key].duration -= 1

        if o.Effect.DEMON_FORM in self.dict_of_ongoing:
            self.add_strength(self.dict_of_ongoing[o.Effect.DEMON_FORM].intensity, self)

    def end_turn(self):
        if o.Effect.RITUAL in self.dict_of_ongoing:
            self.add_strength(self.dict_of_ongoing[o.Effect.RITUAL].intensity, self)

    def deal_damage(self, damage, target, is_attack=True, hit_block=True):
        if is_attack:
            if o.Effect.STRENGTH in self.dict_of_ongoing:
                damage = damage + self.dict_of_ongoing[o.Effect.STRENGTH].intensity

            if o.Effect.WEAK in self.dict_of_ongoing and self.dict_of_ongoing[o.Effect.WEAK].duration > 0:
                damage = damage * 0.75

            if o.Effect.VULNERABLE in target.dict_of_ongoing and target.dict_of_ongoing[o.Effect.VULNERABLE].duration > 0:
                damage = damage * 1.5

        damage = int(damage)

        if hit_block:
            og_block = target.block
            target.block -= damage
            damage -= og_block
            if target.block < 0:
                target.block = 0

        if damage <= 0:
            return

        if o.Effect.CURLUP in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.CURLUP].action(target)

        if o.Effect.ANGRY in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.ANGRY].action(target)

        target.cur_health -= damage
        if target.__class__.__name__ == "Player":
            if cardsFile.BloodForBlood.cost > 0:
                cardsFile.BloodForBlood.cost -= 1
                print(cardsFile.BloodForBlood.cost)

        return damage

    def add_block(self, value, target, affected_by_ongoing=True):
        if affected_by_ongoing:
            if o.Effect.DEXTERITY in target.dict_of_ongoing:
                value += target.dict_of_ongoing[o.Effect.DEXTERITY].intensity

            if o.Effect.FRAIL in target.dict_of_ongoing and target.dict_of_ongoing[o.Effect.FRAIL].duration > 0:
                value = int(value * 0.75)

        target.block += value

    def heal(self, value, target):
        target.cur_health += value
        if target.cur_health > target.max_health:
            target.cur_health = target.max_health

    def add_strength(self, value, target):
        if o.Effect.STRENGTH not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.STRENGTH] = o.Strength()

        target.dict_of_ongoing[o.Effect.STRENGTH].intensity += value

    def add_dexterity(self, value, target):
        if o.Effect.DEXTERITY not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.DEXTERITY] = o.Dexterity()

        target.dict_of_ongoing[o.Effect.DEXTERITY].intensity += value

    def add_frail(self, value, target):
        if o.Effect.FRAIL not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.FRAIL] = o.Frail()

        target.dict_of_ongoing[o.Effect.FRAIL].duration += value

    def add_vulnerable(self, value, target):
        if o.Effect.VULNERABLE not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.VULNERABLE] = o.Vulnerable()

        target.dict_of_ongoing[o.Effect.VULNERABLE].duration += value

    def add_weak(self, value, target):
        if o.Effect.WEAK not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.WEAK] = o.Weak()

        target.dict_of_ongoing[o.Effect.WEAK].duration += value

    def add_ritual(self, value, target):
        if o.Effect.RITUAL not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.RITUAL] = o.Ritual()

        target.dict_of_ongoing[o.Effect.RITUAL].intensity += value

    def add_curlup(self, value, target):
        if o.Effect.CURLUP not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.CURLUP] = o.CurlUp()

        target.dict_of_ongoing[o.Effect.CURLUP].intensity += value

    def add_juggernaut(self, value, target):
        if o.Effect.JUGGERNAUT not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.JUGGERNAUT] = o.Juggernaut()

        target.dict_of_ongoing[o.Effect.JUGGERNAUT].intensity += value

    def add_strength_down(self, value, target):
        if o.Effect.STRENGTH_DOWN not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.STRENGTH_DOWN] = o.StrengthDown()

        target.dict_of_ongoing[o.Effect.STRENGTH_DOWN].intensity += value

    def add_no_draw(self, value, target):
        if o.Effect.NO_DRAW not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.NO_DRAW] = o.NoDraw()

        target.dict_of_ongoing[o.Effect.NO_DRAW].duration += value

    def add_combust(self, value, target):
        if o.Effect.COMBUST not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.COMBUST] = o.Combust()

        target.dict_of_ongoing[o.Effect.COMBUST].intensity += value

    def add_dark_embrace(self, value, target):
        if o.Effect.DARK_EMBRACE not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.DARK_EMBRACE] = o.DarkEmbrace()

        target.dict_of_ongoing[o.Effect.DARK_EMBRACE].intensity += value

    def add_evolve(self, value, target):
        if o.Effect.EVOLVE not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.EVOLVE] = o.Evolve()

        target.dict_of_ongoing[o.Effect.EVOLVE].intensity += value

    def add_feel_no_pain(self, value, target):
        if o.Effect.FEEL_NO_PAIN not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.FEEL_NO_PAIN] = o.FeelNoPain()

        target.dict_of_ongoing[o.Effect.FEEL_NO_PAIN].intensity += value

    def add_fire_breathing(self, value, target):
        if o.Effect.FIRE_BREATHING not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.FIRE_BREATHING] = o.FireBreathing()

        target.dict_of_ongoing[o.Effect.FIRE_BREATHING].intensity += value

    def add_flame_barrier(self, value, target):
        if o.Effect.FLAME_BARRIER not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.FLAME_BARRIER] = o.FlameBarrier()

        target.dict_of_ongoing[o.Effect.FLAME_BARRIER].intensity += value

    def add_metallicize(self, value, target):
        if o.Effect.METALLICIZE not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.METALLICIZE] = o.Metallicize()

        target.dict_of_ongoing[o.Effect.METALLICIZE].intensity += value

    def add_rage(self, value, target):
        if o.Effect.RAGE not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.RAGE] = o.Rage()

        target.dict_of_ongoing[o.Effect.RAGE].intensity += value

    def add_rupture(self, value, target):
        if o.Effect.RUPTURE not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.RUPTURE] = o.Rupture()

        target.dict_of_ongoing[o.Effect.RUPTURE].intensity += value

    def add_barricade(self, target):
        if o.Effect.BARRICADE not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.BARRICADE] = o.Barricade()

    def add_berserk(self, value, target):
        if o.Effect.BERSERK not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.BERSERK] = o.Berserk()

        target.dict_of_ongoing[o.Effect.BERSERK].intensity += value

    def add_brutality(self, value, target):
        if o.Effect.BRUTALITY not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.BRUTALITY] = o.Brutality()

        target.dict_of_ongoing[o.Effect.BRUTALITY].intensity += value

    def add_corruption(self, target):
        if o.Effect.CORRUPTION not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.CORRUPTION] = o.Corruption()

    def add_demon_form(self, value, target):
        if o.Effect.DEMON_FORM not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.DEMON_FORM] = o.DemonForm()

        target.dict_of_ongoing[o.Effect.DEMON_FORM].intensity += value

    def add_double_tap(self, value, target):
        if o.Effect.DOUBLE_TAP not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.DOUBLE_TAP] = o.DoubleTap()

        target.dict_of_ongoing[o.Effect.DOUBLE_TAP].counter += value

    def add_entangled(self, value, target):
        if o.Effect.ENTANGLED not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.ENTANGLED] = o.Entangled()

        target.dict_of_ongoing[o.Effect.ENTANGLED].duration += value

    def add_angry(self, value, target):
        if o.Effect.ANGRY not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.ANGRY] = o.Angry()

        target.dict_of_ongoing[o.Effect.ANGRY].intensity += value

    def add_spore_cloud(self, value, target):
        if o.Effect.SPORE_CLOUD not in target.dict_of_ongoing:
            target.dict_of_ongoing[o.Effect.SPORE_CLOUD] = o.SporeCloud()

        target.dict_of_ongoing[o.Effect.SPORE_CLOUD].intensity += value

