import pygame

from .base_state import BaseState
from .. import config, data, assets
from ..ui.widgets import Button, draw_text, draw_panel, draw_text_wrapped
from ..ui.background import draw_dungeon_background

VENDOR_ANCHOR = (150, 470)
VENDOR_SCALE = 2.4

CARD_W, CARD_H = 280, 170
CARD_GAP = 16
GRID_ORIGIN = (330, 170)
CARDS_PER_ROW = 2


class ShopState(BaseState):
    def enter(self, **kwargs):
        self.vendor_sprite = assets.get_character_sprite("vendedor", flip=False, scale=VENDOR_SCALE)
        if self.vendor_sprite:
            self.vendor_sprite.play("greet")

        self.active_category = data.SHOP_CATEGORIES[0][0]
        self.feedback = ""

        self.tab_buttons = []
        tab_w, tab_gap = 180, 16
        x = GRID_ORIGIN[0]
        for key, label in data.SHOP_CATEGORIES:
            rect = (x, 130, tab_w, 42)
            self.tab_buttons.append((key, Button(rect, label, size=18)))
            x += tab_w + tab_gap

        self.back_button = Button((30, config.SCREEN_HEIGHT - 70, 160, 44), "Volver", size=20,
                                   base_color=config.PANEL, hover_color=config.PANEL_LIGHT)

        self._build_item_cards()

    def _items_in_category(self):
        return [item for item in data.SHOP_ITEMS if item["category"] == self.active_category]

    def _build_item_cards(self):
        self.item_cards = []
        for i, item in enumerate(self._items_in_category()):
            col = i % CARDS_PER_ROW
            row = i // CARDS_PER_ROW
            x = GRID_ORIGIN[0] + col * (CARD_W + CARD_GAP)
            y = GRID_ORIGIN[1] + row * (CARD_H + CARD_GAP)
            rect = pygame.Rect(x, y, CARD_W, CARD_H)
            buy_btn = Button((rect.x + 20, rect.bottom - 42, rect.width - 40, 32),
                              f"Comprar ({item['price']} oro)", size=15)
            self.item_cards.append((item, rect, buy_btn))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state("dungeon")
            return

        if self.back_button.handle_event(event):
            self.game.change_state("dungeon")
            return

        for key, button in self.tab_buttons:
            if button.handle_event(event) and key != self.active_category:
                self.active_category = key
                self.feedback = ""
                self._build_item_cards()
                return

        for item, rect, buy_btn in self.item_cards:
            if buy_btn.handle_event(event):
                self._buy(item)

    def _buy(self, item):
        player = self.game.player
        if player.gold < item["price"]:
            self.feedback = f"No tienes suficiente oro para {item['name']}."
            return
        player.gold -= item["price"]
        player.add_item(item["key"])
        self.feedback = f"Compraste {item['name']}."
        self.game.log(f"Compras {item['name']} en la tienda.")

    def update(self, dt):
        if self.vendor_sprite:
            self.vendor_sprite.update(dt)

    def draw(self, surface):
        draw_dungeon_background(surface)
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        draw_text(surface, "Tienda del Vendedor", (config.SCREEN_WIDTH // 2, 40),
                  size=32, color=config.GOLD, bold=True, center=True)

        self._draw_vendor(surface)
        self._draw_hud(surface)

        for key, button in self.tab_buttons:
            if key == self.active_category:
                button.base_color = config.PANEL_BORDER
            else:
                button.base_color = config.PANEL
            button.draw(surface)

        for item, rect, buy_btn in self.item_cards:
            draw_panel(surface, rect)
            icon = assets.get_item_icon(item["icon"], scale=2.5)
            icon_rect = icon.get_rect(topleft=(rect.x + 16, rect.y + 14))
            surface.blit(icon, icon_rect)
            draw_text(surface, item["name"], (icon_rect.right + 14, rect.y + 18),
                      size=17, color=config.WHITE, bold=True)
            draw_text_wrapped(surface, item["description"],
                               (rect.x + 16, rect.y + 58, rect.width - 32, 56),
                               size=13, color=config.LIGHT_GRAY)
            buy_btn.draw(surface)

        if self.feedback:
            draw_text(surface, self.feedback, (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 76),
                      size=16, color=config.GOLD, center=True)

        self.back_button.draw(surface)

    def _draw_vendor(self, surface):
        panel_rect = (20, 130, 250, 420)
        draw_panel(surface, panel_rect)
        if self.vendor_sprite:
            self.vendor_sprite.draw(surface, VENDOR_ANCHOR)
        else:
            draw_text(surface, "Vendedor", (panel_rect[0] + 125, 300), size=18,
                      color=config.WHITE, bold=True, center=True)
        draw_text_wrapped(surface, "¿Buscas algo en particular, aventurero?",
                           (panel_rect[0] + 16, 150, panel_rect[2] - 32, 40),
                           size=13, color=config.LIGHT_GRAY)

    def _draw_hud(self, surface):
        player = self.game.player
        coin_icon = assets.get_item_icon((1, 1), scale=1.6)
        icon_pos = (config.SCREEN_WIDTH - 200, 34)
        surface.blit(coin_icon, icon_pos)
        draw_text(surface, str(player.gold), (icon_pos[0] + coin_icon.get_width() + 8, 40),
                  size=22, color=config.GOLD, bold=True)
