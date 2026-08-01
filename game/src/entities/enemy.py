from .character import Character


class Enemy(Character):
    def __init__(self, name, max_life, speed, weapon, armor, classification, is_boss=False,
                 gold_reward=0, mechanic=None):
        super().__init__(name, max_life, speed, weapon, armor)
        self.classification = classification
        self.is_boss = is_boss
        self.gold_reward = gold_reward
        # Special boss behaviour hook: None, "bones" (Jefe Esqueleto regenerates
        # once its minions die) or "hex" (Bruja can poison the player on hit).
        self.mechanic = mechanic
