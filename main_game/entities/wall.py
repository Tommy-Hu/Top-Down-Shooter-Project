import pygame


class Wall:
    def __init__(self, rect, renderer, color=pygame.Color("DIMGRAY"), breakable=False):
        self.rect = pygame.Rect(rect)
        self.renderer = renderer
        self.color = color
        self.breakable = breakable
        self.surface = pygame.Surface((rect.width, rect.height))
        self.surface.fill(color)

    def update_to_renderer(self):
        self.renderer.add_to_canvas(self.surface, self.rect.topleft)

    def refresh_location(self, offset):
        self.rect.topleft = self.rect.topleft + offset
