import json
import os

from .. import config

SAVE_PATH = os.path.join(config.BASE_DIR, "save", "wallet.json")


class Wallet:
    """Gold balance saved to disk, independent of the current run. Money
    earned combat after combat keeps accumulating even after death/reset_run,
    since Game creates it once and never rebuilds it on reset_run()."""

    def __init__(self, balance=0):
        self.balance = balance

    @classmethod
    def load(cls):
        try:
            with open(SAVE_PATH) as f:
                raw = json.load(f)
            return cls(balance=int(raw.get("balance", 0)))
        except (OSError, ValueError, TypeError):
            return cls(balance=0)

    def save(self):
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        with open(SAVE_PATH, "w") as f:
            json.dump({"balance": self.balance}, f)

    def add(self, amount):
        self.balance += amount
        self.save()

    def spend(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        self.save()
        return True
