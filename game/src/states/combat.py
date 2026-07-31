import pygame

from .base_state import BaseState
from .. import config
from ..ui.widgets import Button, draw_text, draw_panel, draw_bar
from ..ui.background import draw_dungeon_background

TURN_DELAY = 0.7
END_DELAY = 1.1


class CombatState(BaseState):
    def enter(self, enemy=None, **kwargs):
        self.enemy = enemy
        self.phase = "player_turn"  # player_turn -> enemy_wait -> player_turn | resolved
        self.timer = 0.0
        self.combat_log = [f"¡Un {enemy.name} aparece frente a ti!"]
        self.result = None  # "victory" | "defeat" | "fled"

        btn_w, btn_h, gap = 190, 54, 20
        total = btn_w * 3 + gap * 2
        start_x = (config.SCREEN_WIDTH - total) // 2
        y = config.SCREEN_HEIGHT - 100
        self.attack_button = Button((start_x, y, btn_w, btn_h), "Atacar", size=22)
        self.potion_button = Button((start_x + btn_w + gap, y, btn_w, btn_h), "Usar poción",
                                     size=20, base_color=config.DARK_GREEN, hover_color=config.GREEN)
        self.flee_button = Button((start_x + (btn_w + gap) * 2, y, btn_w, btn_h), "Huir",
                                   size=22, base_color=config.PANEL, hover_color=config.PANEL_LIGHT)

    def _add_log(self, text):
        self.combat_log.append(text)
        self.combat_log = self.combat_log[-5:]

    def handle_event(self, event):
        if self.phase != "player_turn":
            return
        if self.attack_button.handle_event(event):
            self._player_attacks()
        if self.potion_button.handle_event(event):
            self._use_potion()
        if self.flee_button.handle_event(event):
            self._flee()

    def _player_attacks(self):
        player = self.game.player
        dmg = player.damage_against(self.enemy)
        self.enemy.take_damage(dmg)
        self._add_log(f"Atacas a {self.enemy.name} y le causas {dmg} de daño.")
        if not self.enemy.is_alive:
            self._finish("victory")
            return
        self.phase = "enemy_wait"
        self.timer = TURN_DELAY

    def _use_potion(self):
        player = self.game.player
        if player.potions <= 0:
            self._add_log("No tienes pociones.")
            return
        healed = player.use_potion()
        self._add_log(f"Bebes una poción y recuperas {healed} de vida.")
        self.phase = "enemy_wait"
        self.timer = TURN_DELAY

    def _flee(self):
        self._add_log("Huyes del combate.")
        self.result = "fled"
        self.phase = "resolved"
        self.timer = END_DELAY * 0.5

    def _enemy_attacks(self):
        player = self.game.player
        dmg = self.enemy.damage_against(player)
        player.take_damage(dmg)
        self._add_log(f"{self.enemy.name} te ataca y te causa {dmg} de daño.")
        if not player.is_alive:
            self._finish("defeat")
            return
        self.phase = "player_turn"

    def _finish(self, result):
        self.result = result
        self.phase = "resolved"
        self.timer = END_DELAY
        if result == "victory":
            gold = self.enemy.gold_reward
            self.game.player.gold += gold
            self._add_log(f"¡Has derrotado a {self.enemy.name}! Ganas {gold} de oro.")

    def update(self, dt):
        if self.phase == "enemy_wait":
            self.timer -= dt
            if self.timer <= 0:
                self._enemy_attacks()
        elif self.phase == "resolved":
            self.timer -= dt
            if self.timer <= 0:
                self._transition()

    def _transition(self):
        game = self.game
        if self.result == "victory":
            game.log(f"Derrotaste a {self.enemy.name}.")
            if self.enemy.is_boss:
                game.victory = True
                game.change_state("game_over")
            else:
                game.depth += 1
                game.player.rooms_cleared += 1
                game.change_state("dungeon")
        elif self.result == "defeat":
            game.log(f"Has caído ante {self.enemy.name}.")
            game.victory = False
            game.change_state("game_over")
        else:  # fled
            game.log("Escapas de vuelta a la mazmorra.")
            game.change_state("dungeon")

    def draw(self, surface):
        draw_dungeon_background(surface)
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        player = self.game.player
        self._draw_combatant(surface, (40, 40, 380, 150), player.name, player.class_name,
                              player.life, player.max_life, player.weapon, player.armor,
                              config.GREEN)
        self._draw_combatant(surface, (config.SCREEN_WIDTH - 420, 40, 380, 150),
                              self.enemy.name, self.enemy.classification,
                              self.enemy.life, self.enemy.max_life,
                              self.enemy.weapon, self.enemy.armor, config.RED)

        draw_text(surface, "VS", (config.SCREEN_WIDTH // 2, 110), size=40,
                  color=config.GOLD, bold=True, center=True)

        log_rect = (config.SCREEN_WIDTH // 2 - 320, 240, 640, 220)
        draw_panel(surface, log_rect, color=(20, 20, 26))
        for i, line in enumerate(self.combat_log[-6:]):
            draw_text(surface, line, (log_rect[0] + 20, log_rect[1] + 16 + i * 28),
                      size=17, color=config.LIGHT_GRAY)

        self.potion_button.enabled = self.game.player.potions > 0 and self.phase == "player_turn"
        self.attack_button.enabled = self.phase == "player_turn"
        self.flee_button.enabled = self.phase == "player_turn"
        self.attack_button.draw(surface)
        self.potion_button.draw(surface)
        self.flee_button.draw(surface)

        draw_text(surface, f"Pociones: {self.game.player.potions}",
                  (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 130),
                  size=16, color=config.GOLD, center=True)

    def _draw_combatant(self, surface, rect, name, subtitle, life, max_life, weapon, armor, bar_color):
        draw_panel(surface, rect)
        x, y, w, h = rect
        draw_text(surface, name, (x + 16, y + 12), size=22, color=config.WHITE, bold=True)
        draw_text(surface, subtitle, (x + 16, y + 40), size=15, color=config.GRAY)
        draw_bar(surface, (x + 16, y + 66, w - 32, 22), life, max_life, bar_color,
                 label=f"{life}/{max_life} HP")
        draw_text(surface, f"Arma: {weapon.name} (+{weapon.damage})", (x + 16, y + 96),
                  size=14, color=config.LIGHT_GRAY)
        draw_text(surface, f"Armadura: {armor.name} (+{armor.defense})", (x + 16, y + 118),
                  size=14, color=config.LIGHT_GRAY)
