import pygame

from .base_state import BaseState
from .. import config, data, assets
from ..ui.widgets import Button, draw_text, draw_panel, draw_bar, draw_text_wrapped
from ..ui.background import draw_dungeon_background

KEY_DOOR = "key"
DOOR_Y = 260
DOOR_H = 236


class DungeonState(BaseState):
    def enter(self, **kwargs):
        self.boss_incoming = self.game.depth >= config.BOSS_DEPTH
        self.boss_template = None
        self.shop_button = Button((config.SCREEN_WIDTH - 190, 20, 170, 44), "Tienda", size=20,
                                   base_color=config.DARK_GREEN, hover_color=config.GREEN)
        self.book_button = Button((config.SCREEN_WIDTH - 190, 72, 170, 40), "Equipar Libro",
                                   size=15, base_color=config.PANEL, hover_color=config.PANEL_LIGHT)
        self._build_buttons()

    def _build_buttons(self):
        self.door_buttons = []
        self.door_outcomes = {}
        player = self.game.player

        if self.boss_incoming:
            if self.boss_template is None:
                self.boss_template = data.pick_boss_template()
            rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 160, 300, 320, 140)
            self.door_buttons.append((None, rect, Button(
                (rect.x + 30, rect.bottom - 60, rect.width - 60, 44),
                f"Enfrentar a {self.boss_template['name']}", size=16,
                base_color=config.DARK_RED, hover_color=config.RED)))
            return

        self.has_key_door = player.has_item("llave")
        count = len(data.DOORS) + (1 if self.has_key_door else 0)
        door_w, gap = (210, 26) if self.has_key_door else (220, 40)
        total = door_w * count + gap * (count - 1)
        start_x = (config.SCREEN_WIDTH - total) // 2
        name_size = 18 if self.has_key_door else 20

        for i, door in enumerate(data.DOORS):
            self.door_outcomes[i] = data.roll_door_outcome(i, self.game.depth)
            rect = pygame.Rect(start_x + i * (door_w + gap), DOOR_Y, door_w, DOOR_H)
            btn = Button((rect.x + 20, rect.bottom - 44, rect.width - 40, 32),
                         "Abrir", size=18)
            self.door_buttons.append((i, rect, btn))

        if self.has_key_door:
            i = len(data.DOORS)
            rect = pygame.Rect(start_x + i * (door_w + gap), DOOR_Y, door_w, DOOR_H)
            btn = Button((rect.x + 20, rect.bottom - 44, rect.width - 40, 32),
                         "Usar llave", size=16, base_color=config.DARK_GREEN, hover_color=config.GOLD)
            self.door_buttons.append((KEY_DOOR, rect, btn))

        self._name_size = name_size

    def handle_event(self, event):
        if self.shop_button.handle_event(event):
            self.game.change_state("shop")
            return
        if not self.boss_incoming and self.game.player.has_item("libro"):
            if self.book_button.handle_event(event):
                self.game.player.equipped_book = not self.game.player.equipped_book
        for index, rect, button in self.door_buttons:
            if button.handle_event(event):
                self._choose_door(index)
                return

    def _choose_door(self, index):
        player = self.game.player
        if self.boss_incoming:
            enemies = data.boss_encounter(self.game.depth, template=self.boss_template)
            self.game.log(f"¡Te enfrentas a {self.boss_template['name']}!")
            self.game.change_state("combat", enemies=enemies)
            return

        if index == KEY_DOOR:
            player.consume_item("llave")
            self.game.log(data.open_key_door(player))
            self._advance_room()
            return

        outcome = self.door_outcomes[index]
        kind, payload, message = data.apply_door_outcome(outcome, player)
        if kind == "enemy":
            self.game.log(f"Te encuentras con un {payload.name}.")
            self.game.change_state("combat", enemy=payload)
            return

        if message:
            self.game.log(message)
        self._advance_room()

    def _advance_room(self):
        self.game.depth += 1
        self.game.player.rooms_cleared += 1
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
        self.shop_button.draw(surface)
        if not self.boss_incoming and player.has_item("libro"):
            self.book_button.text = "Libro equipado ✓" if player.equipped_book else "Equipar Libro"
            self.book_button.base_color = config.DARK_GREEN if player.equipped_book else config.PANEL
            self.book_button.draw(surface)

        if self.boss_incoming:
            draw_text(surface, "El fondo del pasillo se abre a una sala inmensa...",
                      (config.SCREEN_WIDTH // 2, 220), size=22, color=config.RED, center=True)
        else:
            draw_text(surface, f"Piso {self.game.depth} - Elige una puerta",
                      (config.SCREEN_WIDTH // 2, 220), size=26, color=config.GOLD,
                      bold=True, center=True)

        has_lentes = player.has_item("lentes")
        for index, rect, button in self.door_buttons:
            draw_panel(surface, rect, color=config.PANEL)
            if index == KEY_DOOR:
                draw_text(surface, "Puerta del Tesoro", (rect.centerx, rect.y + 26),
                          size=self._name_size, color=config.GOLD, bold=True, center=True)
                draw_text_wrapped(surface, "Arma legendaria o armadura poderosa, al azar.",
                                   (rect.x + 14, rect.y + 56, rect.width - 28, 70),
                                   size=13, color=config.GRAY)
            elif index is not None:
                door = data.DOORS[index]
                draw_text(surface, door["name"], (rect.centerx, rect.y + 26),
                          size=self._name_size, color=config.WHITE, bold=True, center=True)
                draw_text_wrapped(surface, door["flavor"],
                                   (rect.x + 14, rect.y + 56, rect.width - 28, 70),
                                   size=13, color=config.GRAY)
                if has_lentes:
                    hint = data.preview_door_outcome(self.door_outcomes[index])
                    draw_text_wrapped(surface, hint,
                                       (rect.x + 14, rect.y + 135, rect.width - 28, 40),
                                       size=12, color=config.GOLD)
            else:
                draw_text(surface, f"{self.boss_template['name']} te espera", (rect.centerx, rect.y + 30),
                          size=18, color=config.WHITE, bold=True, center=True)
            button.draw(surface)

        self._draw_log(surface)

    def _draw_hud(self, surface, player):
        panel_rect = (20, 20, 340, 148)
        draw_panel(surface, panel_rect)
        draw_text(surface, f"{player.name} ({player.class_name})", (36, 32),
                  size=18, color=config.WHITE, bold=True)
        draw_bar(surface, (36, 58, 300, 20), player.life, player.max_life,
                 config.GREEN, label=f"{player.life}/{player.max_life} HP")
        if player.max_mana > 0:
            draw_bar(surface, (36, 82, 300, 16), player.mana, player.max_mana,
                     config.BLUE, label=f"{player.mana}/{player.max_mana} MP")
        coin_icon = assets.get_item_icon((1, 1), scale=1.2)
        surface.blit(coin_icon, (36, 106))
        draw_text(surface, f"{player.gold}",
                  (36 + coin_icon.get_width() + 6, 108), size=16, color=config.GOLD)
        draw_text(surface, f"Arma: {player.weapon.name} (+{player.weapon.damage})",
                  (36, 132), size=14, color=config.LIGHT_GRAY)

    def _draw_log(self, surface):
        log_rect = (20, config.SCREEN_HEIGHT - 130, config.SCREEN_WIDTH - 40, 110)
        draw_panel(surface, log_rect, color=(20, 20, 26))
        for i, message in enumerate(self.game.message_log[-4:]):
            draw_text(surface, message, (36, log_rect[1] + 12 + i * 24),
                      size=16, color=config.LIGHT_GRAY)
