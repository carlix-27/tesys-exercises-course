import pygame

from .base_state import BaseState
from .. import config, assets
from ..ui.widgets import Button, draw_text, draw_panel
from ..ui.background import draw_dungeon_background


class GameOverState(BaseState):
    def enter(self, **kwargs):
        cx = config.SCREEN_WIDTH // 2
        button_y = 474 if self.game.survival_mode else 440
        self.retry_button = Button((cx - 150, button_y, 300, 54), "Volver al menú", size=22)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_ESCAPE):
            self._to_menu()
        if self.retry_button.handle_event(event):
            self._to_menu()

    def _to_menu(self):
        self.game.reset_run()
        self.game.change_state("menu")

    def update(self, dt):
        pass

    def draw(self, surface):
        draw_dungeon_background(surface)
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))

        player = self.game.player
        if self.game.victory:
            title, color = "¡HAS CONQUISTADO LA MAZMORRA!", config.GOLD
            subtitle = "El jefe de la mazmorra yace derrotado. Tu leyenda comienza."
        elif self.game.survival_mode and self.game.rounds_survived > 0:
            title, color = "HAS CAÍDO EN LA OSCURIDAD", config.RED
            subtitle = f"Sobreviviste {self.game.rounds_survived} ronda(s) antes de caer."
        else:
            title, color = "HAS CAÍDO EN LA OSCURIDAD", config.RED
            subtitle = "La mazmorra reclama otra víctima."

        draw_text(surface, title, (config.SCREEN_WIDTH // 2, 160), size=40,
                  color=color, bold=True, center=True)
        draw_text(surface, subtitle, (config.SCREEN_WIDTH // 2, 210), size=18,
                  color=config.LIGHT_GRAY, center=True)

        if player is not None:
            extra_h = 34 if self.game.survival_mode else 0
            panel_rect = (config.SCREEN_WIDTH // 2 - 200, 260, 400, 150 + extra_h)
            draw_panel(surface, panel_rect)
            lines = [
                f"Personaje: {player.name} ({player.class_name})",
                f"Salas superadas: {player.rooms_cleared}",
            ]
            if self.game.survival_mode:
                lines.append(f"Rondas de jefe superadas: {self.game.rounds_survived}")
            for i, line in enumerate(lines):
                draw_text(surface, line, (panel_rect[0] + 24, panel_rect[1] + 24 + i * 34),
                          size=18, color=config.WHITE)
            coin_icon = assets.get_item_icon((1, 1), scale=1.4)
            coin_y = panel_rect[1] + 24 + len(lines) * 34
            surface.blit(coin_icon, (panel_rect[0] + 24, coin_y))
            draw_text(surface, f"Oro en tu billetera: {player.gold}",
                      (panel_rect[0] + 24 + coin_icon.get_width() + 8, coin_y + 5),
                      size=18, color=config.WHITE)

        self.retry_button.draw(surface)
