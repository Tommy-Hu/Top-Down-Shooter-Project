import pygame


class Character(object):
    def __init__(self, sprite, rect, renderer, speed, default_weapon, scale=100):
        self.sprite = pygame.transform.scale(sprite, (scale, scale))
        self.rect = rect
        self.renderer = renderer
        self.speed = speed
        self.weapon = default_weapon

    def move(self, new_pos):
        self.rect.topleft = new_pos

    def draw_to_renderer(self):
        self.renderer.add_to_canvas(self.sprite, self.rect.topleft)
