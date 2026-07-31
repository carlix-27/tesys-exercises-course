import random

import pygame

from .. import config

_BRICK_W = 64
_BRICK_H = 32


def draw_dungeon_background(surface):
    """Procedurally draws a simple brick/stone wall so the game needs no image assets."""
    surface.fill(config.STONE_A)
    w, h = surface.get_size()
    rng = random.Random(1337)  # fixed seed so the wall pattern is stable across frames
    row = 0
    y = 0
    while y < h:
        offset = (_BRICK_W // 2) if row % 2 else 0
        x = -offset
        while x < w:
            shade = config.STONE_B if rng.random() > 0.5 else config.STONE_A
            surface_rect = (x, y, _BRICK_W - 2, _BRICK_H - 2)
            _draw_brick(surface, surface_rect, shade)
            x += _BRICK_W
        y += _BRICK_H
        row += 1


def _draw_brick(surface, rect, color):
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, config.BLACK, rect, 1)
