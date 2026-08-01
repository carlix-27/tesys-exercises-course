import random

import pygame

from .base_state import BaseState
from .. import config, assets
from ..ui.widgets import Button, draw_text, draw_panel, draw_bar
from ..ui.sprites import Animator
from ..ui.background import draw_dungeon_background

FALLBACK_TURN_DELAY = 0.7
ENEMY_PAUSE = 0.35
DEFEAT_PAUSE = 0.6
END_DELAY = 1.0

ARENA_RECT = pygame.Rect(20, 14, config.SCREEN_WIDTH - 40, 300)
FLOOR_Y = ARENA_RECT.y + int(ARENA_RECT.height * 0.82)
PLAYER_ANCHOR = (ARENA_RECT.x + int(ARENA_RECT.width * 0.26), FLOOR_Y)
ENEMY_ANCHOR = (ARENA_RECT.x + int(ARENA_RECT.width * 0.74), FLOOR_Y)
NORMAL_SCALE = 1.9
BOSS_SCALE = 2.15

STAT_PANEL_H = 122
LOG_RECT = (20, 452, config.SCREEN_WIDTH - 40, 62)
ITEM_ROW_Y = 522
ITEM_ROW_H = 34
MAIN_ROW_Y = 568
MAIN_ROW_H = 50

# --- Item / spell effect tuning -------------------------------------------
FUEGO_COST = 20           # Libro: fireball, ignores armor
FUEGO_DAMAGE = 30
RAYO_COST = 12            # Libro: lightning bolt, ignores armor, cheaper/weaker
RAYO_DAMAGE = 18
EFFECT_FPS = 12
LINTERNA_BOSS_DAMAGE = 40  # Linterna can't one-shot the boss, just scorches it
PARALYSIS_DURATION = 5.0   # Reloj: seconds the enemy skips retaliating
POCION_VIDA_HEAL = 40
POCION_MANA_RESTORE = 35
POISON_TOTAL = 30          # Veneno: total damage dealt over several ticks
POISON_TICK = 6
BOSS_REGEN_RATIO = 0.4     # Jefe Esqueleto: life restored once its minions die
HEX_CHANCE = 0.5           # Bruja: odds an attack also poisons the player


class CombatState(BaseState):
    def enter(self, enemy=None, enemies=None, **kwargs):
        self.enemies = list(enemies) if enemies else [enemy]
        self.phase = "player_turn"
        self.timer = 0.0
        self.pending_mode = "normal"
        self.paralysis_timer = 0.0
        self.gold_earned = 0
        self.active_effects = []
        self.result = None  # "victory" | "defeat" | "fled"

        if len(self.enemies) > 1:
            boss = self.enemies[-1]
            self.combat_log = [f"¡{boss.name} aparece junto a {len(self.enemies) - 1} secuaces!"]
        else:
            self.combat_log = [f"¡Un {self.enemies[0].name} aparece frente a ti!"]

        player = self.game.player
        self.player_sprite = assets.get_character_sprite(
            getattr(player, "sprite_key", None), flip=False, scale=NORMAL_SCALE)
        self._set_front_enemy()

        btn_w, btn_h, gap = 220, MAIN_ROW_H, 30
        total = btn_w * 2 + gap
        start_x = (config.SCREEN_WIDTH - total) // 2
        y = MAIN_ROW_Y
        self.attack_button = Button((start_x, y, btn_w, btn_h), "Atacar", size=22)
        self.flee_button = Button((start_x + btn_w + gap, y, btn_w, btn_h), "Huir",
                                   size=22, base_color=config.PANEL, hover_color=config.PANEL_LIGHT)

        self._build_item_buttons()

    def _set_front_enemy(self):
        self.enemy = self.enemies[0]
        enemy_scale = BOSS_SCALE if self.enemy.is_boss else NORMAL_SCALE
        self.enemy_sprite = assets.get_character_sprite(
            getattr(self.enemy, "sprite_key", None), flip=True, scale=enemy_scale)

    def _build_item_buttons(self):
        player = self.game.player
        available = []
        if player.equipped_book:
            if player.mana >= FUEGO_COST:
                available.append(("fuego", "Fuego", self._use_fuego))
            if player.mana >= RAYO_COST:
                available.append(("rayo", "Rayo", self._use_rayo))
        if player.has_item("pocion_vida"):
            available.append(("pocion_vida", f"Vida (x{player.inventory['pocion_vida']})", self._use_pocion_vida))
        if player.has_item("pocion_mana"):
            available.append(("pocion_mana", f"Maná (x{player.inventory['pocion_mana']})", self._use_pocion_mana))
        if player.has_item("pocion_veneno"):
            available.append(("pocion_veneno", f"Veneno (x{player.inventory['pocion_veneno']})", self._use_pocion_veneno))
        if player.has_item("reloj"):
            available.append(("reloj", f"Reloj (x{player.inventory['reloj']})", self._use_reloj))
        if player.has_item("linterna"):
            available.append(("linterna", f"Linterna (x{player.inventory['linterna']})", self._use_linterna))
        if player.has_item("pistola"):
            available.append(("pistola", f"Pistola (x{player.inventory['pistola']})", self._use_pistola))

        self.item_buttons = []
        if not available:
            return
        gap = 8
        max_total = config.SCREEN_WIDTH - 60
        btn_w = min(120, (max_total - gap * (len(available) - 1)) // len(available))
        total = btn_w * len(available) + gap * (len(available) - 1)
        start_x = (config.SCREEN_WIDTH - total) // 2
        for i, (key, label, handler) in enumerate(available):
            rect = (start_x + i * (btn_w + gap), ITEM_ROW_Y, btn_w, ITEM_ROW_H)
            btn = Button(rect, label, size=12, base_color=config.PANEL, hover_color=config.PANEL_LIGHT)
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

    def _use_fuego(self):
        player = self.game.player
        if not player.spend_mana(FUEGO_COST):
            return
        self._build_item_buttons()
        self._player_attacks(mode="fuego")

    def _use_rayo(self):
        player = self.game.player
        if not player.spend_mana(RAYO_COST):
            return
        self._build_item_buttons()
        self._player_attacks(mode="rayo")

    def _use_pocion_vida(self):
        player = self.game.player
        if not player.consume_item("pocion_vida"):
            return
        healed = player.heal(POCION_VIDA_HEAL)
        self._add_log(f"Bebes una poción de vida y recuperas {healed} de vida.")
        self._build_item_buttons()
        self.phase = "enemy_pause"
        self.timer = ENEMY_PAUSE

    def _use_pocion_mana(self):
        player = self.game.player
        if not player.consume_item("pocion_mana"):
            return
        restored = player.restore_mana(POCION_MANA_RESTORE)
        self._add_log(f"Bebes una poción de maná y recuperas {restored} de maná.")
        self._build_item_buttons()
        self.phase = "enemy_pause"
        self.timer = ENEMY_PAUSE

    def _use_pocion_veneno(self):
        player = self.game.player
        if not player.consume_item("pocion_veneno"):
            return
        self.enemy.poison_remaining = POISON_TOTAL
        self.enemy.poison_tick = POISON_TICK
        self._add_log(f"Arrojas una poción de veneno sobre {self.enemy.name}. Empieza a envenenarse.")
        self._build_item_buttons()
        self.phase = "enemy_pause"
        self.timer = ENEMY_PAUSE

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

    def _spawn_effect(self, effect_key, anchor):
        frames = assets.get_effect_frames(effect_key)
        if not frames:
            return
        animator = Animator(frames, fps=EFFECT_FPS, loop=False)
        self.active_effects.append([animator, anchor])

    def _resolve_player_hit(self):
        player = self.game.player
        mode = self.pending_mode
        if mode == "fuego":
            dmg = FUEGO_DAMAGE
            self._spawn_effect("fuego", ENEMY_ANCHOR)
            self._add_log(f"Lanzas una bola de fuego a {self.enemy.name} y le causas {dmg} de daño mágico.")
        elif mode == "rayo":
            dmg = RAYO_DAMAGE
            self._spawn_effect("rayo", ENEMY_ANCHOR)
            self._add_log(f"Invocas un rayo sobre {self.enemy.name} y le causas {dmg} de daño mágico.")
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
            self.phase = "enemy_defeated_pause"
            self.timer = self._anim_duration(self.enemy_sprite, "death", fallback=DEFEAT_PAUSE)
            return
        if self.enemy_sprite:
            self.enemy_sprite.play("hurt")
        if self.paralysis_timer > 0:
            self._add_log(f"{self.enemy.name} sigue paralizado y no puede contraatacar.")
            self.phase = "player_turn"
        else:
            self.phase = "enemy_pause"
            self.timer = ENEMY_PAUSE

    def _enemy_defeated(self):
        defeated = self.enemies.pop(0)
        self.gold_earned += defeated.gold_reward
        if not self.enemies:
            self._finish("victory")
            return
        was_last_minion = (not defeated.is_boss and self.enemies[0].is_boss
                            and self.enemies[0].mechanic == "bones")
        self._set_front_enemy()
        if self.enemy_sprite:
            self.enemy_sprite.play("idle")
        if was_last_minion:
            heal = int(self.enemy.max_life * BOSS_REGEN_RATIO)
            self.enemy.heal(heal)
            self._add_log(f"¡{self.enemy.name} absorbe los huesos de sus siervos caídos y recupera {heal} de vida!")
        else:
            self._add_log(f"Derrotas a {defeated.name}.")
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

    def _tick_poison(self, character):
        remaining = character.poison_remaining
        if remaining <= 0:
            return False
        tick = min(character.poison_tick, remaining)
        character.take_damage(tick)
        character.poison_remaining = remaining - tick
        self._add_log(f"{character.name} sufre {tick} de daño por veneno.")
        return not character.is_alive

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
        # Tick any poison inflicted on a previous turn before possibly
        # inflicting a fresh one below, so a new hex doesn't also lose a
        # tick's worth of damage on the very turn it lands.
        if self._tick_poison(player):
            if self.player_sprite:
                self.player_sprite.play("death")
            self._finish("defeat")
            return

        if (self.enemy.mechanic == "hex" and player.poison_remaining <= 0
                and random.random() < HEX_CHANCE):
            player.poison_remaining = POISON_TOTAL
            player.poison_tick = POISON_TICK
            self._add_log(f"¡{self.enemy.name} te maldice con un hechizo venenoso!")
            self._spawn_effect(random.choice(["fuego", "rayo"]), PLAYER_ANCHOR)
        self.phase = "player_turn"

    def _finish(self, result):
        self.result = result
        self.phase = "resolved"
        death_sprite = self.enemy_sprite if result == "victory" else self.player_sprite
        self.timer = self._anim_duration(death_sprite, "death", fallback=END_DELAY) + 0.4
        if result == "victory":
            self.game.player.gold += self.gold_earned
            self._add_log(f"¡Has derrotado a {self.enemy.name}! Ganas {self.gold_earned} de oro.")

    def update(self, dt):
        if self.player_sprite:
            self.player_sprite.update(dt)
        if self.enemy_sprite:
            self.enemy_sprite.update(dt)
        if self.paralysis_timer > 0:
            self.paralysis_timer = max(0.0, self.paralysis_timer - dt)
        for effect in self.active_effects:
            effect[0].update(dt)
        self.active_effects = [e for e in self.active_effects if not e[0].finished]

        if self.phase == "player_attack":
            self.timer -= dt
            if self.timer <= 0:
                self._resolve_player_hit()
        elif self.phase == "enemy_pause":
            self.timer -= dt
            if self.timer <= 0:
                if self._tick_poison(self.enemy):
                    if self.enemy_sprite:
                        self.enemy_sprite.play("death")
                    self.phase = "enemy_defeated_pause"
                    self.timer = self._anim_duration(self.enemy_sprite, "death", fallback=DEFEAT_PAUSE)
                else:
                    self._start_enemy_attack()
        elif self.phase == "enemy_defeated_pause":
            self.timer -= dt
            if self.timer <= 0:
                self._enemy_defeated()
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
        self._draw_stat_panel(surface, (20, 324, 470, STAT_PANEL_H), player, player.class_name, config.GREEN)
        enemy_subtitle = self.enemy.classification
        if len(self.enemies) > 1:
            enemy_subtitle += f"  (+{len(self.enemies) - 1} más)"
        self._draw_stat_panel(surface, (config.SCREEN_WIDTH - 490, 324, 470, STAT_PANEL_H),
                               self.enemy, enemy_subtitle, config.RED)

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

        self.attack_button.enabled = self.phase == "player_turn"
        self.flee_button.enabled = self.phase == "player_turn"
        self.attack_button.draw(surface)
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

        for animator, anchor in self.active_effects:
            frame = animator.current_frame()
            rect = frame.get_rect(center=(anchor[0], anchor[1] - 70))
            surface.blit(frame, rect)

        draw_text(surface, "VS", (config.SCREEN_WIDTH // 2, ARENA_RECT.y + 30), size=32,
                  color=config.GOLD, bold=True, center=True)

    def _draw_stat_panel(self, surface, rect, character, subtitle, bar_color):
        draw_panel(surface, rect)
        x, y, w, h = rect
        draw_text(surface, character.name, (x + 16, y + 10), size=20, color=config.WHITE, bold=True)
        draw_text(surface, subtitle, (x + 16, y + 32), size=14, color=config.GRAY)
        draw_bar(surface, (x + 16, y + 52, w - 32, 18), character.life, character.max_life, bar_color,
                 label=f"{character.life}/{character.max_life} HP")
        if character.max_mana > 0:
            draw_bar(surface, (x + 16, y + 74, w - 32, 14), character.mana, character.max_mana, config.BLUE,
                     label=f"{character.mana}/{character.max_mana} MP")
        if character.poison_remaining > 0:
            draw_text(surface, f"Envenenado: {character.poison_remaining} de daño pendiente",
                      (x + 16, y + 92), size=12, color=config.PURPLE)
        draw_text(surface, f"{character.weapon.name} (+{character.weapon.damage})  |  "
                            f"{character.armor.name} (+{character.armor.defense})",
                  (x + 16, y + h - 20), size=13, color=config.LIGHT_GRAY)
