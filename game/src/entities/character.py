class Character:
    """Base entity for anything that fights: has life, speed, a weapon and armor."""

    def __init__(self, name, max_life, speed, weapon, armor, max_mana=0):
        self.name = name
        self.max_life = max_life
        self.life = max_life
        self.speed = speed
        self.weapon = weapon
        self.armor = armor
        self.max_mana = max_mana
        self.mana = max_mana
        # Poison-over-time state; 0 means "not poisoned". Left as plain
        # attributes (not constructor args) since only whoever inflicts the
        # poison needs to set them.
        self.poison_remaining = 0
        self.poison_tick = 0

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

    def spend_mana(self, amount):
        if self.mana < amount:
            return False
        self.mana -= amount
        return True

    def restore_mana(self, amount):
        before = self.mana
        self.mana = min(self.max_mana, self.mana + amount)
        return self.mana - before

    def damage_against(self, defender):
        # A fight where damage always resolves to 0 can stall forever, so
        # every hit chips at least 1 point through armor.
        raw = self.weapon.damage - defender.armor.defense
        return max(raw, 1)


class Player(Character):
    def __init__(self, name, class_name, max_life, speed, weapon, armor, max_mana=0, wallet=None):
        super().__init__(name, max_life, speed, weapon, armor, max_mana=max_mana)
        self.class_name = class_name
        self.rooms_cleared = 0
        self.inventory = {}
        self.equipped_book = False
        self.wallet = wallet
        self._local_gold = 0

    @property
    def gold(self):
        return self.wallet.balance if self.wallet else self._local_gold

    @gold.setter
    def gold(self, value):
        if self.wallet:
            self.wallet.balance = value
            self.wallet.save()
        else:
            self._local_gold = value

    def add_item(self, item_key, qty=1):
        self.inventory[item_key] = self.inventory.get(item_key, 0) + qty

    def has_item(self, item_key):
        return self.inventory.get(item_key, 0) > 0

    def consume_item(self, item_key):
        if not self.has_item(item_key):
            return False
        self.inventory[item_key] -= 1
        return True
