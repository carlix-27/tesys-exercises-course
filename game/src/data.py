"""Static game data: starting classes, the enemy bestiary, the boss and loot tables."""
import random

from .entities.items import Weapon, Armor
from .entities.character import Player
from .entities.enemy import Enemy
from . import config

# --- Playable classes --------------------------------------------------
CLASSES = {
    "espadachin": dict(
        label="Espadachín",
        name="Espadachín",
        max_life=100,
        speed=10,
        weapon=("Espada de hierro", 10),
        armor=("Armadura de acero", 10),
        blurb="Resistente y equilibrado. Golpea fuerte y aguanta el castigo.",
        sprite="espadachin",
    ),
    "picaro": dict(
        label="Pícaro",
        name="Pícaro",
        max_life=70,
        speed=15,
        weapon=("Espada de acero", 15),
        armor=("Armadura de hierro", 5),
        blurb="Frágil pero letal y veloz. Golpea primero, pero no aguanta mucho.",
        sprite="picaro",
    ),
}


def make_player(class_key):
    data = CLASSES[class_key]
    weapon = Weapon(*data["weapon"])
    armor = Armor(*data["armor"])
    player = Player(data["name"], data["label"], data["max_life"], data["speed"], weapon, armor)
    player.sprite_key = data.get("sprite")
    return player


# --- Bestiary ------------------------------------------------------------
ENEMY_TEMPLATES = [
    dict(name="Goblin Común", classification="Goblin Pícaro", life=45, speed=5,
         weapon=("Daga oxidada", 8), armor=("Harapos", 2), gold=8, sprite="goblin"),
    dict(name="Goblin Guerrero", classification="Goblin Guerrero", life=65, speed=8,
         weapon=("Hacha corta", 12), armor=("Cota ligera", 5), gold=12, sprite="goblin"),
    dict(name="Esqueleto Errante", classification="No-muerto", life=55, speed=6,
         weapon=("Espada oxidada", 10), armor=("Huesos endurecidos", 3), gold=10, sprite="esqueleto"),
    dict(name="Bandido de la Mazmorra", classification="Humano corrupto", life=60, speed=9,
         weapon=("Daga doble", 11), armor=("Cuero reforzado", 4), gold=14, sprite="bandido"),
]

ELITE_TEMPLATES = [
    dict(name="Abominación de la Mazmorra", classification="Horror", life=90, speed=7,
         weapon=("Garras retorcidas", 16), armor=("Piel correosa", 6), gold=22, sprite="abominacion"),
    dict(name="Habitante Olvidado", classification="Espectro", life=80, speed=11,
         weapon=("Filo espectral", 15), armor=("Bruma", 5), gold=20, sprite="espectro"),
]

BOSS_TEMPLATE = dict(
    name="Rey Goblin", classification="Monarca Goblin", life=120, speed=12,
    weapon=("Espada real de acero templado", 16), armor=("Armadura real", 4), gold=150,
    sprite="goblin",
)

WEAPON_UPGRADES = [
    Weapon("Espada de acero templado", 20),
    Weapon("Espada rúnica", 26),
    Weapon("Espadón del Rey", 32),
]

ARMOR_UPGRADES = [
    Armor("Armadura de acero templado", 14),
    Armor("Armadura rúnica", 18),
    Armor("Armadura real", 24),
]


def _build_enemy(template, depth, is_boss=False):
    life_bonus = depth * 6
    dmg_bonus = depth
    def_bonus = depth // 2
    weapon = Weapon(template["weapon"][0], template["weapon"][1] + dmg_bonus)
    armor = Armor(template["armor"][0], template["armor"][1] + def_bonus)
    life = template["life"] + life_bonus
    enemy = Enemy(
        template["name"], life, template["speed"], weapon, armor,
        template["classification"], is_boss=is_boss, gold_reward=template["gold"],
    )
    enemy.sprite_key = template.get("sprite")
    return enemy


def random_enemy(depth):
    return _build_enemy(random.choice(ENEMY_TEMPLATES), depth)


def random_elite(depth):
    return _build_enemy(random.choice(ELITE_TEMPLATES), depth)


def boss_enemy(depth):
    # The template is already tuned for the depth at which the boss appears,
    # so it does not receive the extra depth scaling regular enemies get
    # (otherwise the fight becomes unwinnable with starting-tier gear).
    return _build_enemy(BOSS_TEMPLATE, depth=0, is_boss=True)


def open_chest(player, rare=False):
    """Applies chest loot straight to the player and returns a description."""
    roll = random.random()
    if rare:
        roll *= 0.6  # rare chests bias towards better outcomes

    if roll < 0.35:
        amount = random.randint(15, 30) if rare else random.randint(8, 18)
        player.gold += amount
        return f"Encuentras un cofre con {amount} monedas de oro."

    if roll < 0.6:
        player.potions += 1
        return "Encuentras una poción de curación."

    if roll < 0.8:
        candidates = [w for w in WEAPON_UPGRADES if w.damage > player.weapon.damage]
        if candidates:
            new_weapon = min(candidates, key=lambda w: w.damage)
            player.weapon = new_weapon
            return f"¡Encuentras {new_weapon.name}! Tu arma ha mejorado."
        player.gold += 15
        return "El cofre solo contenía chatarra sin valor. Consigues 15 de oro."

    candidates = [a for a in ARMOR_UPGRADES if a.defense > player.armor.defense]
    if candidates:
        new_armor = min(candidates, key=lambda a: a.defense)
        player.armor = new_armor
        return f"¡Encuentras {new_armor.name}! Tu armadura ha mejorado."
    player.gold += 15
    return "El cofre solo contenía chatarra sin valor. Consigues 15 de oro."


DOORS = [
    dict(name="Puerta de Piedra", flavor="Se siente tranquila... quizás demasiado."),
    dict(name="Puerta de Hierro", flavor="Un frío metálico recorre tu espalda."),
    dict(name="Puerta Maldita", flavor="Susurros salen de las grietas de la madera."),
]


def resolve_door(door_index, depth, player):
    """Rolls an encounter for the chosen door.

    Returns a tuple (kind, payload, message) where kind is one of:
    'nothing', 'chest', 'enemy', 'elite', 'chalice'.
    """
    roll = random.random()

    if door_index == 0:  # Puerta de Piedra: safer
        if roll < 0.45:
            return "nothing", None, "Avanzas por un pasillo vacío. No encuentras nada."
        if roll < 0.75:
            return "enemy", random_enemy(depth), None
        return "chest", None, open_chest(player)

    if door_index == 1:  # Puerta de Hierro: balanced, more fights
        if roll < 0.55:
            return "enemy", random_enemy(depth), None
        return "chest", None, open_chest(player)

    # Puerta Maldita: high risk, high reward
    if roll < 0.25:
        return "enemy", random_elite(depth), None
    if roll < 0.45:
        return "enemy", random_enemy(depth), None
    if roll < 0.70:
        return "chest", None, open_chest(player, rare=True)
    if roll < 0.85:
        amount = random.randint(12, 22)
        player.heal(amount)
        return "chalice", None, f"Bebes de un cáliz misterioso y recuperas {amount} de vida."
    amount = random.randint(8, 16)
    player.take_damage(amount)
    return "chalice", None, f"El cáliz estaba envenenado. Pierdes {amount} de vida."
