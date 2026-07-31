import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Dungeon of Shadows"

# How many rooms must be cleared before the boss door appears
BOSS_DEPTH = 5

# --- Colors -----------------------------------------------------------
BLACK = (12, 12, 16)
WHITE = (235, 235, 240)
DARK = (22, 22, 30)
PANEL = (34, 34, 46)
PANEL_LIGHT = (50, 50, 66)
PANEL_BORDER = (70, 70, 90)

RED = (200, 64, 64)
DARK_RED = (110, 28, 28)
GREEN = (86, 178, 96)
DARK_GREEN = (32, 92, 44)
GOLD = (223, 178, 79)
BLUE = (86, 140, 220)
GRAY = (130, 130, 140)
LIGHT_GRAY = (180, 180, 190)
PURPLE = (150, 96, 210)
STONE_A = (28, 28, 36)
STONE_B = (34, 34, 44)
