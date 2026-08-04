import sys

import pygame

from . import config
from .entities.wallet import Wallet
from .states.menu import MenuState
from .states.character_select import CharacterSelectState
from .states.dungeon import DungeonState
from .states.combat import CombatState
from .states.shop import ShopState
from .states.game_over import GameOverState


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(config.TITLE)
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Persists across runs (survives reset_run and death) -- gold earned
        # combat after combat is banked here, not on the disposable Player.
        self.wallet = Wallet.load()

        # Session data shared across states.
        self.player = None
        self.depth = 1
        self.message_log = []
        self.victory = False

        # Modo supervivencia: elegido en el menú, persiste entre partidas
        # hasta que el jugador lo cambie. En este modo el jefe reaparece
        # cada BOSS_DEPTH salas en lugar de terminar la partida.
        self.survival_mode = False
        self.next_boss_depth = config.BOSS_DEPTH
        self.rounds_survived = 0

        self.states = {
            "menu": MenuState(self),
            "character_select": CharacterSelectState(self),
            "dungeon": DungeonState(self),
            "combat": CombatState(self),
            "shop": ShopState(self),
            "game_over": GameOverState(self),
        }
        self.state = None
        self.change_state("menu")

    def change_state(self, name, **kwargs):
        if self.state is not None:
            self.state.exit()
        self.state = self.states[name]
        self.state.enter(**kwargs)

    def log(self, text):
        self.message_log.append(text)
        self.message_log = self.message_log[-6:]

    def reset_run(self):
        self.player = None
        self.depth = 1
        self.message_log = []
        self.victory = False
        self.next_boss_depth = config.BOSS_DEPTH
        self.rounds_survived = 0

    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.state.handle_event(event)
            self.state.update(dt)
            self.state.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
        sys.exit()
