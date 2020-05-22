import random

import pygame


class Spawner:
    def __init__(self, sprite, location, scale, renderer, enemies_to_spawn, spawn_interval, spawn_amount, spawn_range,
                 add_enemy_callback):
        self.location = location
        self.sprite = pygame.transform.scale(sprite, scale)
        self.renderer = renderer
        self.enemies_to_spawn = enemies_to_spawn
        self.spawn_interval, self.spawn_amount, self.spawn_range = spawn_interval, spawn_amount, spawn_range
        self.add_enemy_callback = add_enemy_callback

        self.spawn_timer = 0

    def get_random_location_in_range(self):
        return self.location[0] + random.randint(-self.spawn_range, self.spawn_range), self.location[
            1] + random.randint(-self.spawn_range, self.spawn_range)

    def update(self, delta_time, current_count, mob_cap):
        self.renderer.add_to_canvas(self.sprite, self.location)

        if current_count >= mob_cap:
            return current_count
        if self.spawn_timer <= 0:
            self.spawn_timer = self.spawn_interval
            spawn_count = random.randint(1, self.spawn_amount)
            for i in range(0, spawn_count):
                self.add_enemy_callback(
                    random.choice(self.enemies_to_spawn).duplicate_as_new(*self.get_random_location_in_range()))
                current_count += 1
                if current_count >= mob_cap:
                    return current_count

        self.spawn_timer -= delta_time
        return current_count
