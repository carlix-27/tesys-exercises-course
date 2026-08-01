import os

from . import config
from .ui.sprites import CharacterSprite

CHARACTERS_DIR = os.path.join(config.ASSETS_DIR, "characters")

_cache = {}


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
