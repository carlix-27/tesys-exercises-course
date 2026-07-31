from .character import Character


class Enemy(Character):
    def __init__(self, name, max_life, speed, weapon, armor, classification, is_boss=False, gold_reward=0):
        super().__init__(name, max_life, speed, weapon, armor)
        self.classification = classification
        self.is_boss = is_boss
        self.gold_reward = gold_reward
