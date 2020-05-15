import pygame.math

from main_game.utils.calculations import *


class Projectile:
    def __init__(self, sprite, pos, direction, speed, spin, spin_speed, renderer, destroy_callback):
        self.original_sprite = sprite
        self.pos = pos
        if pygame.Vector2(direction) == pygame.Vector2(0, 0):
            self.dir = pygame.Vector2(0, 0)
        else:
            self.dir = pygame.Vector2(direction).normalize()
        self.speed = speed
        self.spin = spin
        self.renderer = renderer
        self.spun_degrees = 0
        self.spin_speed = spin_speed

        self.destroy_self = destroy_callback
        self.frames_to_live = 300

    def update(self, walls):
        # self.lerp_color(self.lerp_factor)

        if self.frames_to_live <= 0:
            self.destroy_self(self)

        new_sprite, new_rect = rot_center(self.original_sprite, self.spun_degrees)

        new_rect.center = self.pos

        for wall in walls:
            if wall.check_collision_rect(new_rect):
                self.destroy_self(self)

        self.pos += self.dir * self.speed
        self.renderer.add_to_canvas(new_sprite, new_rect.topleft)
        self.spun_degrees += self.spin_speed
        self.frames_to_live -= 1

    def duplicate(self):
        return Projectile(self.original_sprite, self.pos, self.dir, self.speed, self.spin, self.spin_speed,
                          self.renderer, self.destroy_self)

    # def lerp_color(self, factor):
    #     result = [self.color.r, self.color.g, self.color.b]
    #     cur = [self.color.r, self.color.g, self.color.b]
    #     to = [self.to_color.r, self.to_color.g, self.to_color.b]
    #     for i in range(0, 3):
    #         result[i] = round(result[i] + factor * (to[i] - cur[i]))
    #     self.color = pygame.Color(int(result[0]), int(result[1]), int(result[2]))
