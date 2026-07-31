class Character:
    """Base entity for anything that fights: has life, speed, a weapon and armor."""

    def __init__(self, name, max_life, speed, weapon, armor):
        self.name = name
        self.max_life = max_life
        self.life = max_life
        self.speed = speed
        self.weapon = weapon
        self.armor = armor

    @property
    def is_alive(self):
        return self.life > 0

    def take_damage(self, amount):
        self.life = max(0, self.life - amount)
        return amount

    def heal(self, amount):
        before = self.life
        self.life = min(self.max_life, self.life + amount)
        return self.life - before

    def damage_against(self, defender):
        # A fight where damage always resolves to 0 can stall forever, so
        # every hit chips at least 1 point through armor.
        raw = self.weapon.damage - defender.armor.defense
        return max(raw, 1)


class Player(Character):
    def __init__(self, name, class_name, max_life, speed, weapon, armor):
        super().__init__(name, max_life, speed, weapon, armor)
        self.class_name = class_name
        self.potions = 2
        self.gold = 0
        self.rooms_cleared = 0

    def use_potion(self, amount=30):
        if self.potions <= 0:
            return 0
        self.potions -= 1
        return self.heal(amount)
