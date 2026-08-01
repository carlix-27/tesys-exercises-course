import os

import pygame

from . import config
from .ui.sprites import CharacterSprite

CHARACTERS_DIR = os.path.join(config.ASSETS_DIR, "characters")
ITEMS_SHEET_PATH = os.path.join(config.ASSETS_DIR, "items", "items.png")
POTIONS_DIR = os.path.join(config.ASSETS_DIR, "items", "pociones")
EFFECTS_DIR = os.path.join(CHARACTERS_DIR, "effects")
ITEM_ICON_SIZE = 16

# Spell effect sprites: folder name under assets/characters/effects/ plus the
# frame filename prefix used inside it (they don't match for "rayo").
EFFECT_SOURCES = {
    "fuego": ("fuego", "fuego"),
    "rayo": ("rayos", "rayo"),
}

_cache = {}
_item_sheet = None
_item_icon_cache = {}
_potion_icon_cache = {}
_effect_frames_cache = {}


def get_character_sprite(sprite_key, flip=False, scale=2.0):
    """Returns a cached CharacterSprite for sprite_key, or None if that
    character has no art yet (missing folder / no frames)."""
    if not sprite_key:
        return None
    cache_key = (sprite_key, flip, scale)
    if cache_key not in _cache:
        folder = os.path.join(CHARACTERS_DIR, sprite_key)
        sprite = CharacterSprite(folder, flip=flip, scale=scale)
        _cache[cache_key] = sprite if sprite.has_art else None
    return _cache[cache_key]


def get_item_icon(grid_pos, scale=2.0):
    """Returns a scaled surface for a 16x16 icon cut out of the shared items
    spritesheet. grid_pos is (col, row), both 0-indexed."""
    global _item_sheet
    cache_key = (grid_pos, scale)
    if cache_key in _item_icon_cache:
        return _item_icon_cache[cache_key]

    if _item_sheet is None:
        _item_sheet = pygame.image.load(ITEMS_SHEET_PATH).convert_alpha()

    col, row = grid_pos
    rect = pygame.Rect(col * ITEM_ICON_SIZE, row * ITEM_ICON_SIZE,
                        ITEM_ICON_SIZE, ITEM_ICON_SIZE)
    icon = _item_sheet.subsurface(rect).copy()
    if scale != 1:
        size = int(ITEM_ICON_SIZE * scale)
        icon = pygame.transform.scale(icon, (size, size))
    _item_icon_cache[cache_key] = icon
    return icon


def get_potion_icon(potion_key, scale=2.0):
    """Returns a scaled surface for a potion's idle_0 frame (its own folder
    under assets/items/pociones/<potion_key>/, unlike the shared items sheet)."""
    cache_key = (potion_key, scale)
    if cache_key in _potion_icon_cache:
        return _potion_icon_cache[cache_key]

    path = os.path.join(POTIONS_DIR, potion_key, "idle_0.png")
    icon = pygame.image.load(path).convert_alpha()
    if scale != 1:
        w, h = icon.get_size()
        icon = pygame.transform.scale(icon, (int(w * scale), int(h * scale)))
    _potion_icon_cache[cache_key] = icon
    return icon


def get_effect_frames(effect_key):
    """Returns the cached list of frame Surfaces for a spell effect
    ("fuego" or "rayo"), loaded from assets/characters/effects/."""
    if effect_key in _effect_frames_cache:
        return _effect_frames_cache[effect_key]

    folder, prefix = EFFECT_SOURCES[effect_key]
    frames = []
    i = 0
    while True:
        path = os.path.join(EFFECTS_DIR, folder, f"{prefix}_{i}.png")
        if not os.path.isfile(path):
            break
        frames.append(pygame.image.load(path).convert_alpha())
        i += 1
    _effect_frames_cache[effect_key] = frames
    return frames
