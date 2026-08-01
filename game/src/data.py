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
        max_mana=20,
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
        max_mana=35,
        blurb="Frágil pero letal y veloz. Golpea primero, pero no aguanta mucho.",
        sprite="picaro",
    ),
    "mago": dict(
        label="Mago",
        name="Mago",
        max_life=60,
        speed=8,
        weapon=("Bastón arcano", 6),
        armor=("Túnica encantada", 3),
        max_mana=100,
        blurb="Frágil cuerpo a cuerpo, pero con un pozo de maná enorme para dominar el fuego y el rayo.",
        sprite="mago",
    ),
}


def make_player(class_key, wallet=None):
    data = CLASSES[class_key]
    weapon = Weapon(*data["weapon"])
    armor = Armor(*data["armor"])
    player = Player(data["name"], data["label"], data["max_life"], data["speed"], weapon, armor,
                     max_mana=data.get("max_mana", 0), wallet=wallet)
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

BOSS_TEMPLATES = [
    dict(name="Rey Goblin", classification="Monarca Goblin", life=120, speed=12,
         weapon=("Espada real de acero templado", 16), armor=("Armadura real", 4), gold=150,
         sprite="goblin", mechanic=None),
    dict(name="Jefe Esqueleto", classification="Señor de los Huesos", life=140, speed=9,
         weapon=("Guadaña ósea", 14), armor=("Coraza de huesos", 6), gold=180,
         sprite="jefe_esqueleto", mechanic="bones"),
    dict(name="Bruja del Bosque Negro", classification="Hechicera maldita", life=110, speed=11,
         weapon=("Cetro maldito", 12), armor=("Manto sombrío", 3), gold=170,
         sprite="bruja", mechanic="hex"),
]

# Spawned alongside the Jefe Esqueleto; when the three of them die the boss
# "regenerates" from their bones (see combat.py's BOSS_REGEN_RATIO).
MINI_ESQUELETO_TEMPLATE = dict(
    name="Hueso Andante", classification="Esqueleto menor", life=25, speed=10,
    weapon=("Hueso afilado", 6), armor=("Huesos sueltos", 1), gold=0, sprite="esqueleto",
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
        mechanic=template.get("mechanic"),
    )
    enemy.sprite_key = template.get("sprite")
    return enemy


def random_enemy(depth):
    return _build_enemy(random.choice(ENEMY_TEMPLATES), depth)


def random_elite(depth):
    return _build_enemy(random.choice(ELITE_TEMPLATES), depth)


def pick_boss_template():
    return random.choice(BOSS_TEMPLATES)


def boss_encounter(depth, template=None):
    """Builds the full enemy line-up for the boss fight.

    Bosses tuned with mechanic == "bones" (Jefe Esqueleto) show up with 3
    mini-skeletons ahead of them in the queue; combat.py pops them off one
    at a time and regenerates the boss once the last one falls. Templates
    are already tuned for the depth at which the boss appears, so (like the
    old boss_enemy()) they skip the extra depth scaling regular enemies get.
    """
    template = template or pick_boss_template()
    enemies = []
    if template.get("mechanic") == "bones":
        enemies.extend(_build_enemy(MINI_ESQUELETO_TEMPLATE, depth=0) for _ in range(3))
    enemies.append(_build_enemy(template, depth=0, is_boss=True))
    return enemies


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
        player.add_item("pocion_vida")
        return "Encuentras una poción de vida."

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


# --- Shop ---------------------------------------------------------------
SHOP_CATEGORIES = [
    ("equipamiento", "Equipamiento"),
    ("puertas", "Puertas"),
    ("combate", "Combate"),
    ("pociones", "Pociones"),
]

SHOP_ITEMS = [
    dict(key="libro", name="Libro Arcano", icon=(0, 0), price=40, category="equipamiento",
         description="Da poder de maná y permite lanzar hechizos de fuego o rayo. Equipar antes de elegir puerta."),
    dict(key="llave", name="Llave Dorada", icon=(3, 0), price=35, category="puertas",
         description="Abre la puerta del tesoro: arma legendaria o armadura al azar."),
    dict(key="lentes", name="Lentes Reveladores", icon=(2, 1), price=25, category="puertas",
         description="Revela qué hay detrás de cada puerta antes de elegir."),
    dict(key="reloj", name="Reloj Detenido", icon=(3, 1), price=30, category="combate",
         description="Paraliza al enemigo 5s: golpéalo sin recibir contraataque."),
    dict(key="linterna", name="Linterna Solar", icon=(2, 3), price=60, category="combate",
         description="Desintegra al enemigo al instante (los jefes solo se queman)."),
    dict(key="pistola", name="Pistola Vieja", icon=(0, 3), price=100, category="combate",
         description="Mata a cualquier enemigo, incluso jefes, de un disparo."),
    dict(key="pocion_vida", name="Poción de Vida", icon_folder="vida", price=20, category="pociones",
         description="Restaura 40 puntos de vida al instante."),
    dict(key="pocion_mana", name="Poción de Maná", icon_folder="mana", price=20, category="pociones",
         description="Restaura 35 puntos de maná al instante."),
    dict(key="pocion_veneno", name="Poción de Veneno", icon_folder="veneno", price=25, category="pociones",
         description="Se la arrojas al enemigo: le drena hasta 30 de vida con el tiempo."),
]


DOORS = [
    dict(name="Puerta de Piedra", flavor="Se siente tranquila... quizás demasiado."),
    dict(name="Puerta de Hierro", flavor="Un frío metálico recorre tu espalda."),
    dict(name="Puerta Maldita", flavor="Susurros salen de las grietas de la madera."),
]


def roll_door_outcome(door_index, depth):
    """Rolls what a door holds WITHOUT touching the player.

    Kept separate from apply_door_outcome so all doors of a room can be
    rolled up front (letting Lentes preview them) without the two doors the
    player doesn't pick still granting gold/potions or healing/damaging them.
    Returns a dict with at least a "kind" key: 'nothing', 'chest', 'enemy',
    'chalice'.
    """
    roll = random.random()

    if door_index == 0:  # Puerta de Piedra: safer
        if roll < 0.45:
            return dict(kind="nothing",
                        message="Avanzas por un pasillo vacío. No encuentras nada.")
        if roll < 0.75:
            return dict(kind="enemy", enemy=random_enemy(depth))
        return dict(kind="chest", rare=False)

    if door_index == 1:  # Puerta de Hierro: balanced, more fights
        if roll < 0.55:
            return dict(kind="enemy", enemy=random_enemy(depth))
        return dict(kind="chest", rare=False)

    # Puerta Maldita: high risk, high reward
    if roll < 0.25:
        return dict(kind="enemy", enemy=random_elite(depth))
    if roll < 0.45:
        return dict(kind="enemy", enemy=random_enemy(depth))
    if roll < 0.70:
        return dict(kind="chest", rare=True)
    if roll < 0.85:
        return dict(kind="chalice", heal=random.randint(12, 22))
    return dict(kind="chalice", damage=random.randint(8, 16))


def apply_door_outcome(outcome, player):
    """Applies a previously-rolled outcome to the player.

    Returns a tuple (kind, payload, message), same shape the old
    resolve_door() returned, so callers don't need to change.
    """
    kind = outcome["kind"]
    if kind == "nothing":
        return "nothing", None, outcome["message"]
    if kind == "enemy":
        return "enemy", outcome["enemy"], None
    if kind == "chest":
        return "chest", None, open_chest(player, rare=outcome.get("rare", False))
    # chalice
    if "heal" in outcome:
        amount = outcome["heal"]
        player.heal(amount)
        return "chalice", None, f"Bebes de un cáliz misterioso y recuperas {amount} de vida."
    amount = outcome["damage"]
    player.take_damage(amount)
    return "chalice", None, f"El cáliz estaba envenenado. Pierdes {amount} de vida."


DOOR_PREVIEW_HINTS = {
    "nothing": "Presientes un pasillo vacío.",
    "chest": "Presientes un cofre cercano.",
    "chalice": "Presientes una energía extraña.",
}


def preview_door_outcome(outcome):
    """Lentes flavor text for a rolled-but-not-yet-applied outcome."""
    kind = outcome["kind"]
    if kind == "enemy":
        return f"Presientes la presencia de: {outcome['enemy'].classification}."
    return DOOR_PREVIEW_HINTS.get(kind, "")


# --- Llave: treasure door -------------------------------------------------
LEGENDARY_WEAPON = Weapon("Espada Legendaria", 42)
LEGENDARY_ARMOR = Armor("Armadura Legendaria", 32)


def open_key_door(player):
    """Spends a llave's worth of luck: random legendary weapon or armor."""
    if random.random() < 0.5:
        player.weapon = LEGENDARY_WEAPON
        return f"¡La puerta del tesoro te entrega la {LEGENDARY_WEAPON.name}! (+{LEGENDARY_WEAPON.damage} daño)"
    player.armor = LEGENDARY_ARMOR
    return f"¡La puerta del tesoro te entrega la {LEGENDARY_ARMOR.name}! (+{LEGENDARY_ARMOR.defense} defensa)"
