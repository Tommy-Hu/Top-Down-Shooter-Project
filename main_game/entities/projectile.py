import pygame.math

from main_game.utils.calculations import *


class Projectile:
    def __init__(self, sprite, pos, direction, speed, from_color, to_color, lerp_factor, renderer):
        self.sprite = sprite
        self.pos = pos
        self.dir, self.speed, self.color, self.to_color, self.lerp_factor \
            = direction.normalize(), speed, from_color, to_color, lerp_factor
        self.renderer = renderer

    def update(self):
        self.lerp_color(self.lerp_factor)

        self.pos += self.dir * self.speed
        self.renderer.add_to_canvas(self.sprite,
                                    pygame.Vector2(self.pos.x - self.sprite.get_width(),
                                                   self.pos.y - self.sprite.get_height()))

    def lerp_color(self, factor):
        result = [self.color.r, self.color.g, self.color.b]
        cur = [self.color.r, self.color.g, self.color.b]
        to = [self.to_color.r, self.to_color.g, self.to_color.b]
        for i in range(0, 3):
            result[i] = round(result[i] + factor * (to[i] - cur[i]))
        self.color = pygame.Color(int(result[0]), int(result[1]), int(result[2]))
