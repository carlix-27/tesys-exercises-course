import pygame

from .base_state import BaseState
from .. import config, data
from ..ui.widgets import Button, draw_text, draw_panel, draw_text_wrapped
from ..ui.background import draw_dungeon_background


class CharacterSelectState(BaseState):
    def enter(self, **kwargs):
        self.class_keys = list(data.CLASSES.keys())
        self.cards = []
        card_w, card_h = 320, 380
        gap = 40
        total_w = card_w * len(self.class_keys) + gap * (len(self.class_keys) - 1)
        start_x = (config.SCREEN_WIDTH - total_w) // 2
        y = 130
        for i, key in enumerate(self.class_keys):
            rect = pygame.Rect(start_x + i * (card_w + gap), y, card_w, card_h)
            select_btn = Button((rect.x + 40, rect.bottom - 70, rect.width - 80, 50),
                                 "Elegir", size=22)
            self.cards.append((key, rect, select_btn))
        self.back_button = Button((30, config.SCREEN_HEIGHT - 70, 160, 44), "Volver", size=20,
                                   base_color=config.PANEL, hover_color=config.PANEL_LIGHT)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state("menu")
            return
        for key, rect, button in self.cards:
            if button.handle_event(event):
                self._choose(key)
        if self.back_button.handle_event(event):
            self.game.change_state("menu")

    def _choose(self, key):
        self.game.player = data.make_player(key)
        self.game.depth = 1
        self.game.log(f"Eliges a tu {data.CLASSES[key]['label']}.")
        self.game.change_state("dungeon")

    def update(self, dt):
        pass

    def draw(self, surface):
        draw_dungeon_background(surface)
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        draw_text(surface, "Elige a tu guerrero", (config.SCREEN_WIDTH // 2, 60),
                  size=38, color=config.GOLD, bold=True, center=True)

        for key, rect, button in self.cards:
            info = data.CLASSES[key]
            draw_panel(surface, rect)
            draw_text(surface, info["label"], (rect.centerx, rect.y + 40),
                      size=28, color=config.WHITE, bold=True, center=True)

            lines = [
                f"Vida: {info['max_life']}",
                f"Velocidad: {info['speed']}",
                f"Arma: {info['weapon'][0]} (+{info['weapon'][1]} dmg)",
                f"Armadura: {info['armor'][0]} (+{info['armor'][1]} def)",
            ]
            for i, line in enumerate(lines):
                draw_text(surface, line, (rect.x + 24, rect.y + 90 + i * 30),
                          size=18, color=config.LIGHT_GRAY)

            draw_text_wrapped(surface, info["blurb"],
                               (rect.x + 20, rect.y + 225, rect.width - 40, 60),
                               size=15, color=config.GRAY)
            button.draw(surface)

        self.back_button.draw(surface)
