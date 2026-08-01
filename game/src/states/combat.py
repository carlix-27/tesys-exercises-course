import pygame

from .base_state import BaseState
from .. import config, assets
from ..ui.widgets import Button, draw_text, draw_panel, draw_bar
from ..ui.background import draw_dungeon_background

FALLBACK_TURN_DELAY = 0.7
ENEMY_PAUSE = 0.35
END_DELAY = 1.0

ARENA_RECT = pygame.Rect(20, 14, config.SCREEN_WIDTH - 40, 300)
FLOOR_Y = ARENA_RECT.y + int(ARENA_RECT.height * 0.82)
PLAYER_ANCHOR = (ARENA_RECT.x + int(ARENA_RECT.width * 0.26), FLOOR_Y)
ENEMY_ANCHOR = (ARENA_RECT.x + int(ARENA_RECT.width * 0.74), FLOOR_Y)
NORMAL_SCALE = 1.9
BOSS_SCALE = 2.15

LOG_RECT = (20, 420, config.SCREEN_WIDTH - 40, 70)
ITEM_ROW_Y = 496
ITEM_ROW_H = 34
MAIN_ROW_Y = 546
MAIN_ROW_H = 50

# --- Item effect tuning ---------------------------------------------------
SPELL_DAMAGE = 24          # Libro: flat magic damage, ignores armor
LINTERNA_BOSS_DAMAGE = 40  # Linterna can't one-shot the boss, just scorches it
PARALYSIS_DURATION = 5.0   # Reloj: seconds the enemy skips retaliating


class CombatState(BaseState):
    def enter(self, enemy=None, **kwargs):
        self.enemy = enemy
        self.phase = "player_turn"
        self.timer = 0.0
        self.pending_mode = "normal"
        self.paralysis_timer = 0.0
        self.combat_log = [f"¡Un {enemy.name} aparece frente a ti!"]
        self.result = None  # "victory" | "defeat" | "fled"

        player = self.game.player
        self.player_sprite = assets.get_character_sprite(
            getattr(player, "sprite_key", None), flip=False, scale=NORMAL_SCALE)
        enemy_scale = BOSS_SCALE if enemy.is_boss else NORMAL_SCALE
        self.enemy_sprite = assets.get_character_sprite(
            getattr(enemy, "sprite_key", None), flip=True, scale=enemy_scale)

        btn_w, btn_h, gap = 190, MAIN_ROW_H, 20
        total = btn_w * 3 + gap * 2
        start_x = (config.SCREEN_WIDTH - total) // 2
        y = MAIN_ROW_Y
        self.attack_button = Button((start_x, y, btn_w, btn_h), "Atacar", size=22)
        self.potion_button = Button((start_x + btn_w + gap, y, btn_w, btn_h), "Usar poción",
                                     size=20, base_color=config.DARK_GREEN, hover_color=config.GREEN)
        self.flee_button = Button((start_x + (btn_w + gap) * 2, y, btn_w, btn_h), "Huir",
                                   size=22, base_color=config.PANEL, hover_color=config.PANEL_LIGHT)

        self._build_item_buttons()

    def _build_item_buttons(self):
        player = self.game.player
        available = []
        if player.equipped_book:
            available.append(("spell", "Hechizo", self._use_spell))
        if player.has_item("reloj"):
            available.append(("reloj", f"Reloj (x{player.inventory['reloj']})", self._use_reloj))
        if player.has_item("linterna"):
            available.append(("linterna", f"Linterna (x{player.inventory['linterna']})", self._use_linterna))
        if player.has_item("pistola"):
            available.append(("pistola", f"Pistola (x{player.inventory['pistola']})", self._use_pistola))

        self.item_buttons = []
        if not available:
            return
        btn_w, gap = 160, 14
        total = btn_w * len(available) + gap * (len(available) - 1)
        start_x = (config.SCREEN_WIDTH - total) // 2
        for i, (key, label, handler) in enumerate(available):
            rect = (start_x + i * (btn_w + gap), ITEM_ROW_Y, btn_w, ITEM_ROW_H)
            btn = Button(rect, label, size=14, base_color=config.PANEL, hover_color=config.PANEL_LIGHT)
            self.item_buttons.append((key, btn, handler))

    def _add_log(self, text):
        self.combat_log.append(text)
        self.combat_log = self.combat_log[-5:]

    def _anim_duration(self, sprite, state, fallback=FALLBACK_TURN_DELAY):
        if sprite is None:
            return fallback
        duration = sprite.duration_of(state)
        return duration if duration else fallback

    def handle_event(self, event):
        if self.phase != "player_turn":
            return
        if self.attack_button.handle_event(event):
            self._player_attacks()
            return
        if self.potion_button.handle_event(event):
            self._use_potion()
            return
        if self.flee_button.handle_event(event):
            self._flee()
            return
        for key, btn, handler in self.item_buttons:
            if btn.handle_event(event):
                handler()
                return

    def _player_attacks(self, mode="normal"):
        self.pending_mode = mode
        if self.player_sprite:
            self.player_sprite.play("attack")
        self.phase = "player_attack"
        self.timer = self._anim_duration(self.player_sprite, "attack")

    def _use_spell(self):
        self._player_attacks(mode="spell")

    def _use_reloj(self):
        player = self.game.player
        if not player.consume_item("reloj"):
            return
        self.paralysis_timer = PARALYSIS_DURATION
        self._add_log(f"Detienes el tiempo alrededor de {self.enemy.name}: "
                       f"tienes {int(PARALYSIS_DURATION)} segundos para golpear sin represalias.")
        self._build_item_buttons()

    def _use_linterna(self):
        if not self.game.player.consume_item("linterna"):
            return
        self._build_item_buttons()
        self._player_attacks(mode="linterna")

    def _use_pistola(self):
        if not self.game.player.consume_item("pistola"):
            return
        self._build_item_buttons()
        self._player_attacks(mode="pistola")

    def _resolve_player_hit(self):
        player = self.game.player
        mode = self.pending_mode
        if mode == "spell":
            dmg = SPELL_DAMAGE
            self._add_log(f"Lanzas un hechizo arcano a {self.enemy.name} y le causas {dmg} de daño mágico.")
        elif mode == "linterna":
            if self.enemy.is_boss:
                dmg = LINTERNA_BOSS_DAMAGE
                self._add_log(f"La linterna quema a {self.enemy.name}, pero resiste la desintegración total.")
            else:
                dmg = self.enemy.life
                self._add_log(f"¡La luz desintegra a {self.enemy.name} por completo!")
        elif mode == "pistola":
            dmg = self.enemy.life
            self._add_log(f"Un disparo certero acaba con {self.enemy.name} al instante.")
        else:
            dmg = player.damage_against(self.enemy)
            self._add_log(f"Atacas a {self.enemy.name} y le causas {dmg} de daño.")

        self.enemy.take_damage(dmg)
        if not self.enemy.is_alive:
            if self.enemy_sprite:
                self.enemy_sprite.play("death")
            self._finish("victory")
            return
        if self.enemy_sprite:
            self.enemy_sprite.play("hurt")
        if self.paralysis_timer > 0:
            self._add_log(f"{self.enemy.name} sigue paralizado y no puede contraatacar.")
            self.phase = "player_turn"
        else:
            self.phase = "enemy_pause"
            self.timer = ENEMY_PAUSE

    def _use_potion(self):
        player = self.game.player
        if player.potions <= 0:
            self._add_log("No tienes pociones.")
            return
        healed = player.use_potion()
        self._add_log(f"Bebes una poción y recuperas {healed} de vida.")
        self.phase = "enemy_pause"
        self.timer = ENEMY_PAUSE

    def _flee(self):
        self._add_log("Huyes del combate.")
        self.result = "fled"
        self.phase = "resolved"
        self.timer = END_DELAY * 0.5

    def _start_enemy_attack(self):
        if self.enemy_sprite:
            self.enemy_sprite.play("attack")
        self.phase = "enemy_attack"
        self.timer = self._anim_duration(self.enemy_sprite, "attack")

    def _resolve_enemy_hit(self):
        player = self.game.player
        dmg = self.enemy.damage_against(player)
        player.take_damage(dmg)
        self._add_log(f"{self.enemy.name} te ataca y te causa {dmg} de daño.")
        if not player.is_alive:
            if self.player_sprite:
                self.player_sprite.play("death")
            self._finish("defeat")
            return
        if self.player_sprite:
            self.player_sprite.play("hurt")
        self.phase = "player_turn"

    def _finish(self, result):
        self.result = result
        self.phase = "resolved"
        death_sprite = self.enemy_sprite if result == "victory" else self.player_sprite
        self.timer = self._anim_duration(death_sprite, "death", fallback=END_DELAY) + 0.4
        if result == "victory":
            gold = self.enemy.gold_reward
            self.game.player.gold += gold
            self._add_log(f"¡Has derrotado a {self.enemy.name}! Ganas {gold} de oro.")

    def update(self, dt):
        if self.player_sprite:
            self.player_sprite.update(dt)
        if self.enemy_sprite:
            self.enemy_sprite.update(dt)
        if self.paralysis_timer > 0:
            self.paralysis_timer = max(0.0, self.paralysis_timer - dt)

        if self.phase == "player_attack":
            self.timer -= dt
            if self.timer <= 0:
                self._resolve_player_hit()
        elif self.phase == "enemy_pause":
            self.timer -= dt
            if self.timer <= 0:
                self._start_enemy_attack()
        elif self.phase == "enemy_attack":
            self.timer -= dt
            if self.timer <= 0:
                self._resolve_enemy_hit()
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
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        self._draw_arena(surface)

        player = self.game.player
        self._draw_stat_panel(surface, (20, 324, 470, 90), player.name, player.class_name,
                               player.life, player.max_life, player.weapon, player.armor, config.GREEN)
        self._draw_stat_panel(surface, (config.SCREEN_WIDTH - 490, 324, 470, 90),
                               self.enemy.name, self.enemy.classification,
                               self.enemy.life, self.enemy.max_life,
                               self.enemy.weapon, self.enemy.armor, config.RED)

        draw_panel(surface, LOG_RECT, color=(20, 20, 26))
        for i, line in enumerate(self.combat_log[-3:]):
            draw_text(surface, line, (LOG_RECT[0] + 20, LOG_RECT[1] + 8 + i * 20),
                      size=15, color=config.LIGHT_GRAY)

        if self.paralysis_timer > 0:
            draw_text(surface, f"⏱ {self.enemy.name} paralizado: {self.paralysis_timer:0.1f}s",
                      (config.SCREEN_WIDTH // 2, ITEM_ROW_Y - 14), size=14,
                      color=config.GOLD, bold=True, center=True)

        for key, btn, handler in self.item_buttons:
            btn.enabled = self.phase == "player_turn"
            btn.draw(surface)

        self.potion_button.text = f"Usar poción ({player.potions})"
        self.potion_button.enabled = player.potions > 0 and self.phase == "player_turn"
        self.attack_button.enabled = self.phase == "player_turn"
        self.flee_button.enabled = self.phase == "player_turn"
        self.attack_button.draw(surface)
        self.potion_button.draw(surface)
        self.flee_button.draw(surface)

    def _draw_arena(self, surface):
        draw_panel(surface, ARENA_RECT, color=(18, 18, 24, 255))
        pygame.draw.line(surface, config.PANEL_BORDER,
                          (ARENA_RECT.x + 20, FLOOR_Y), (ARENA_RECT.right - 20, FLOOR_Y), 2)

        for anchor in (PLAYER_ANCHOR, ENEMY_ANCHOR):
            shadow = pygame.Surface((90, 24), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 110), shadow.get_rect())
            surface.blit(shadow, shadow.get_rect(center=anchor))

        if self.player_sprite:
            self.player_sprite.draw(surface, PLAYER_ANCHOR)
        else:
            draw_text(surface, self.game.player.name, PLAYER_ANCHOR, size=20,
                      color=config.WHITE, bold=True, center=True)

        if self.enemy_sprite:
            self.enemy_sprite.draw(surface, ENEMY_ANCHOR)
        else:
            draw_text(surface, self.enemy.name, ENEMY_ANCHOR, size=20,
                      color=config.WHITE, bold=True, center=True)

        draw_text(surface, "VS", (config.SCREEN_WIDTH // 2, ARENA_RECT.y + 30), size=32,
                  color=config.GOLD, bold=True, center=True)

    def _draw_stat_panel(self, surface, rect, name, subtitle, life, max_life, weapon, armor, bar_color):
        draw_panel(surface, rect)
        x, y, w, h = rect
        draw_text(surface, name, (x + 16, y + 10), size=20, color=config.WHITE, bold=True)
        draw_text(surface, subtitle, (x + 16, y + 34), size=14, color=config.GRAY)
        draw_bar(surface, (x + 16, y + 56, w - 32, 20), life, max_life, bar_color,
                 label=f"{life}/{max_life} HP")
        draw_text(surface, f"{weapon.name} (+{weapon.damage})  |  {armor.name} (+{armor.defense})",
                  (x + 16, y + 80), size=13, color=config.LIGHT_GRAY)
