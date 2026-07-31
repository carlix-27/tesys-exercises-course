import math

import pygame

from .base_state import BaseState
from .. import config
from ..ui.widgets import Button, draw_text
from ..ui.background import draw_dungeon_background


class MenuState(BaseState):
    def enter(self, **kwargs):
        self.time = 0.0
        cx = config.SCREEN_WIDTH // 2
        self.start_button = Button((cx - 140, 380, 280, 56), "Comenzar aventura", size=26)
        self.quit_button = Button((cx - 140, 452, 280, 56), "Salir", size=24,
                                   base_color=config.DARK_RED, hover_color=config.RED)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._start()
            elif event.key == pygame.K_ESCAPE:
                self.game.running = False
        if self.start_button.handle_event(event):
            self._start()
        if self.quit_button.handle_event(event):
            self.game.running = False

    def _start(self):
        self.game.reset_run()
        self.game.change_state("character_select")

    def update(self, dt):
        self.time += dt

    def draw(self, surface):
        draw_dungeon_background(surface)
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        pulse = 6 * math.sin(self.time * 2)
        draw_text(surface, "DUNGEON OF SHADOWS", (config.SCREEN_WIDTH // 2, 190 + pulse),
                  size=56, color=config.GOLD, bold=True, center=True)
        draw_text(surface, "Una mazmorra generada al azar te espera",
                  (config.SCREEN_WIDTH // 2, 250), size=22, color=config.LIGHT_GRAY, center=True)

        self.start_button.draw(surface)
        self.quit_button.draw(surface)

        draw_text(surface, "ENTER para comenzar  -  ESC para salir",
                  (config.SCREEN_WIDTH // 2, 540), size=16, color=config.GRAY, center=True)
