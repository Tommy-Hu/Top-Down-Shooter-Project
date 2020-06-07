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
            pos_x += self.scale + 30

        for i in range(0, empty_heart_count):
            self.renderer.add_to_canvas(self.empty_heart_sprite, (pos_x, pos_y), False)
            pos_x += self.scale + 30


class BossBar:
    def __init__(self, location_center, side_sprite, main_sprite, part_sprite, scale_x, scale_y, size_dif_half, maximum,
                 renderer):
        self.side_sprite = side_sprite
        self.main_sprite = main_sprite
        self.part_sprite = part_sprite
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.size_dif_half = size_dif_half
        self.renderer = renderer
        self.maximum = maximum
        self.location_center = location_center
        self.surface = None
        self.redraw_surface(maximum)

    def redraw_surface(self, current):
        self.surface = pygame.Surface((self.scale_x, self.scale_y))
        self.surface.set_colorkey((0, 0, 0))
        self.part_sprite = self.part_sprite
        self.surface.blit(
            pygame.transform.scale(self.main_sprite, (self.scale_x, self.scale_y - 2 * self.size_dif_half)),
            (0, self.size_dif_half))
        size_x = int(float(current) / self.maximum * self.scale_x)
        self.surface.blit(
            pygame.transform.scale(self.part_sprite, (max(size_x, 0), max(self.scale_y - 2 * self.size_dif_half, 0))),
            (0, self.size_dif_half))
        self.surface.blit(pygame.transform.scale(self.side_sprite, (self.scale_y, self.scale_y)), (0, 0))
        self.surface.blit(
            pygame.transform.flip(pygame.transform.scale(self.side_sprite, (self.scale_y, self.scale_y)), True, True),
            (self.scale_x - self.scale_y, 0))

    def update(self, current):
        self.redraw_surface(current)
        self.renderer.add_to_canvas_center(self.surface, self.location_center, False)
