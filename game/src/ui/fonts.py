import pygame

_CACHE = {}
_CANDIDATES = ["couriernew", "consolas", "dejavusansmono", "monospace"]


def get_font(size, bold=False):
    key = (size, bold)
    if key not in _CACHE:
        font = pygame.font.SysFont(",".join(_CANDIDATES), size, bold=bold)
        _CACHE[key] = font
    return _CACHE[key]
