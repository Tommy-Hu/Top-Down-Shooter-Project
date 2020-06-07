import random

import pygame

from particle_system.paticle import Particle


class Spawner:
    def __init__(self, sprite, location, scale, renderer, enemies_to_spawn, spawn_interval, spawn_amount, spawn_range,
                 add_enemy_callback, smoke_sprite, add_particle_callback):
        self.location = location
        self.sprite = pygame.transform.scale(sprite, scale)
        self.renderer = renderer
        self.enemies_to_spawn = enemies_to_spawn
        self.spawn_interval, self.spawn_amount, self.spawn_range = spawn_interval, spawn_amount, spawn_range
        self.add_enemy_callback = add_enemy_callback
        self.add_particle_callback = add_particle_callback

        self.smoke_sprite = pygame.transform.scale(smoke_sprite, (75, 75))
        self.spawn_timer = 0

    def get_random_location_in_range(self):
        return self.location[0] + random.randint(-self.spawn_range, self.spawn_range), self.location[
            1] + random.randint(-self.spawn_range, self.spawn_range)

    def update(self, delta_time, current_count, mob_cap, spawn):
        self.renderer.add_to_canvas(self.sprite, self.location)

        if spawn:
            spawned_poses = []

            def check(_pos):
                for position in spawned_poses:
                    if position.distance_to(_pos) < 85:
                        return False
                return True

            if current_count >= mob_cap:
                return current_count
            if self.spawn_timer <= 0:
                self.spawn_timer = self.spawn_interval
                spawn_count = random.randint(1, self.spawn_amount)
                for i in range(0, spawn_count):
                    pos = self.get_random_location_in_range()
                    if not check(pos):
                        continue
                    spawned_poses.append(pygame.Vector2(pos))
                    self.add_particle_callback(Particle(self.smoke_sprite, pos, 0.5, self.renderer, 300, 5))
                    self.add_enemy_callback(random.choice(self.enemies_to_spawn).duplicate_as_new(*pos))
                    current_count += 1
                    if current_count >= mob_cap:
                        return current_count

            self.spawn_timer -= delta_time
        else:
            self.spawn_timer = 0
        return current_count
