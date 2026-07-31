import pygame

from .. import config
from .fonts import get_font


class Button:
    def __init__(self, rect, text, size=24, base_color=config.PANEL_LIGHT,
                 hover_color=config.PANEL_BORDER, text_color=config.WHITE, bold=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = get_font(size, bold=bold)
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.enabled = True

    def handle_event(self, event):
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        if not self.enabled:
            color = (55, 55, 62)
            text_color = config.GRAY
        elif self.hovered:
            color = self.hover_color
            text_color = self.text_color
        else:
            color = self.base_color
            text_color = self.text_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, config.BLACK, self.rect, 2, border_radius=8)
        label = self.font.render(self.text, True, text_color)
        surface.blit(label, label.get_rect(center=self.rect.center))


def draw_bar(surface, rect, value, max_value, fg_color, bg_color=config.DARK,
             border_color=config.PANEL_BORDER, label=None, font=None):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, bg_color, rect, border_radius=4)
    ratio = 0 if max_value <= 0 else max(0.0, min(1.0, value / max_value))
    fill_rect = rect.copy()
    fill_rect.width = int(rect.width * ratio)
    if fill_rect.width > 0:
        pygame.draw.rect(surface, fg_color, fill_rect, border_radius=4)
    pygame.draw.rect(surface, border_color, rect, 2, border_radius=4)
    if label:
        font = font or get_font(16, bold=True)
        text = font.render(label, True, config.WHITE)
        surface.blit(text, text.get_rect(center=rect.center))


def draw_text(surface, text, pos, size=20, color=config.WHITE, bold=False, center=False):
    font = get_font(size, bold=bold)
    label = font.render(text, True, color)
    if center:
        surface.blit(label, label.get_rect(center=pos))
    else:
        surface.blit(label, pos)
    return label.get_rect(topleft=pos)


def draw_text_wrapped(surface, text, rect, size=16, color=config.WHITE, line_spacing=4):
    font = get_font(size)
    words = text.split(" ")
    rect = pygame.Rect(rect)
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if font.size(candidate)[0] > rect.width and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)

    y = rect.y
    for line in lines:
        label = font.render(line, True, color)
        surface.blit(label, (rect.x, y))
        y += label.get_height() + line_spacing
    return y


def draw_panel(surface, rect, color=config.PANEL, border=config.PANEL_BORDER, radius=10):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, 2, border_radius=radius)
