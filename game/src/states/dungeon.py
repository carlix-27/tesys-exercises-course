import pygame

from .base_state import BaseState
from .. import config, data
from ..ui.widgets import Button, draw_text, draw_panel, draw_bar, draw_text_wrapped
from ..ui.background import draw_dungeon_background


class DungeonState(BaseState):
    def enter(self, **kwargs):
        self.boss_incoming = self.game.depth >= config.BOSS_DEPTH
        self._build_buttons()
        self.info_message = ""

    def _build_buttons(self):
        self.door_buttons = []
        if self.boss_incoming:
            rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 160, 300, 320, 140)
            self.door_buttons.append((None, rect, Button(
                (rect.x + 30, rect.bottom - 60, rect.width - 60, 44),
                "Enfrentar al Rey Goblin", size=18,
                base_color=config.DARK_RED, hover_color=config.RED)))
        else:
            door_w, gap = 220, 40
            total = door_w * 3 + gap * 2
            start_x = (config.SCREEN_WIDTH - total) // 2
            for i, door in enumerate(data.DOORS):
                rect = pygame.Rect(start_x + i * (door_w + gap), 260, door_w, 220)
                btn = Button((rect.x + 20, rect.bottom - 60, rect.width - 40, 44),
                             "Abrir", size=20)
                self.door_buttons.append((i, rect, btn))

    def handle_event(self, event):
        for index, rect, button in self.door_buttons:
            if button.handle_event(event):
                self._choose_door(index)

    def _choose_door(self, index):
        player = self.game.player
        if self.boss_incoming:
            enemy = data.boss_enemy(self.game.depth)
            self.game.log(f"¡El {enemy.name} bloquea tu camino!")
            self.game.change_state("combat", enemy=enemy)
            return

        kind, payload, message = data.resolve_door(index, self.game.depth, player)
        if kind in ("enemy",):
            self.game.log(f"Te encuentras con un {payload.name}.")
            self.game.change_state("combat", enemy=payload)
            return

        if message:
            self.game.log(message)
        self.game.depth += 1
        player.rooms_cleared += 1
        self.boss_incoming = self.game.depth >= config.BOSS_DEPTH
        self._build_buttons()

    def update(self, dt):
        pass

    def draw(self, surface):
        draw_dungeon_background(surface)
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        surface.blit(overlay, (0, 0))

        player = self.game.player
        self._draw_hud(surface, player)

        if self.boss_incoming:
            draw_text(surface, "El fondo del pasillo se abre a una sala inmensa...",
                      (config.SCREEN_WIDTH // 2, 220), size=22, color=config.RED, center=True)
        else:
            draw_text(surface, f"Piso {self.game.depth} - Elige una puerta",
                      (config.SCREEN_WIDTH // 2, 220), size=26, color=config.GOLD,
                      bold=True, center=True)

        for index, rect, button in self.door_buttons:
            draw_panel(surface, rect, color=config.PANEL)
            if index is not None:
                door = data.DOORS[index]
                draw_text(surface, door["name"], (rect.centerx, rect.y + 30),
                          size=20, color=config.WHITE, bold=True, center=True)
                draw_text_wrapped(surface, door["flavor"],
                                   (rect.x + 16, rect.y + 60, rect.width - 32, 100),
                                   size=14, color=config.GRAY)
            else:
                draw_text(surface, "El Rey Goblin te espera", (rect.centerx, rect.y + 30),
                          size=18, color=config.WHITE, bold=True, center=True)
            button.draw(surface)

        self._draw_log(surface)

    def _draw_hud(self, surface, player):
        panel_rect = (20, 20, 340, 120)
        draw_panel(surface, panel_rect)
        draw_text(surface, f"{player.name} ({player.class_name})", (36, 32),
                  size=18, color=config.WHITE, bold=True)
        draw_bar(surface, (36, 60, 300, 22), player.life, player.max_life,
                 config.GREEN, label=f"{player.life}/{player.max_life} HP")
        draw_text(surface, f"Oro: {player.gold}   Pociones: {player.potions}",
                  (36, 92), size=16, color=config.GOLD)
        draw_text(surface, f"Arma: {player.weapon.name} (+{player.weapon.damage})",
                  (36, 114), size=14, color=config.LIGHT_GRAY)

    def _draw_log(self, surface):
        log_rect = (20, config.SCREEN_HEIGHT - 130, config.SCREEN_WIDTH - 40, 110)
        draw_panel(surface, log_rect, color=(20, 20, 26))
        for i, message in enumerate(self.game.message_log[-4:]):
            draw_text(surface, message, (36, log_rect[1] + 12 + i * 24),
                      size=16, color=config.LIGHT_GRAY)
