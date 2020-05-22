import math

import pygame


class HealthBar:
    def __init__(self, location, heart_sprite, empty_heart_sprite, scale, max_health, renderer, health_per_heart=20):
        self.heart_sprite = pygame.transform.scale(heart_sprite, (scale, scale))
        self.scale = scale
        self.empty_heart_sprite = pygame.transform.scale(empty_heart_sprite, (scale, scale))
        self.location = location
        self.max_health = max_health
        self.health_per_heart = health_per_heart
        self.renderer = renderer

    def update(self, current_health, max_health):
        total_heart_count = int(math.ceil(max_health / float(self.health_per_heart)))
        alive_heart_count = int(math.ceil(current_health / float(self.health_per_heart)))
        empty_heart_count = total_heart_count - alive_heart_count

        pos_x, pos_y = self.location

        for i in range(0, alive_heart_count):
            self.renderer.add_to_canvas(self.heart_sprite, (pos_x, pos_y), False)
            pos_y += self.scale + 30

        for i in range(0, empty_heart_count):
            self.renderer.add_to_canvas(self.empty_heart_sprite, (pos_x, pos_y), False)
            pos_y += self.scale + 30
