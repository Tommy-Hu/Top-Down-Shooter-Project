import pygame.math

from main_game.entities.player import Player
from main_game.particle_system import particles_manager
from main_game.particle_system.paticle import Particle
from main_game.utils.calculations import *


class Projectile:
    def __init__(self, sprite, burst_sprite, pos, direction, speed, damage, spin, spin_speed, renderer,
                 destroy_callback,
                 audio_manager, is_player=False, life_time=1, sprite_scale_multiplier=1, burst_scale_multiplier=1):
        self.original_sprite = pygame.transform.scale(sprite, (
            sprite.get_width() * sprite_scale_multiplier, sprite.get_height() * sprite_scale_multiplier))
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
        self.damage = damage

        self.destroy_self = destroy_callback
        self.life_time = life_time
        self.life_left = life_time

        self.audio_manager = audio_manager
        self.is_player = is_player

        self.burst_sprite = pygame.transform.scale(burst_sprite, (
            burst_sprite.get_width() * burst_scale_multiplier, burst_sprite.get_height() * burst_scale_multiplier))

    def update(self, walls, characters_to_damage, delta_time):
        new_sprite, new_rect = rot_center(self.original_sprite, self.spun_degrees)
        new_rect.center = self.pos

        if self.life_left <= 0:
            self.destroy_self(self)
            self.shoot_particles(new_rect)

        for ch in characters_to_damage:
            is_instance_player = type(ch) == Player
            if (is_instance_player and not self.is_player) or (not is_instance_player and self.is_player):
                if new_rect.colliderect(ch.rect):
                    ch.damage(self.damage)
                    self.destroy_self(self)
                    self.shoot_particles(new_rect)
                    self.audio_manager.play_hit_sound('hit_1')
                    return

        for wall in walls:
            if wall.check_collision_rect(new_rect):
                self.destroy_self(self)
                self.shoot_particles(new_rect)
                self.audio_manager.play_hit_sound('hit_1')
                return

        self.pos += self.dir * self.speed * delta_time
        self.renderer.add_to_canvas(new_sprite, new_rect.topleft)
        self.spun_degrees += self.spin_speed
        self.life_left -= delta_time

    def duplicate(self, is_player):
        return Projectile(self.original_sprite, self.burst_sprite, self.pos, self.dir, self.speed, self.damage,
                          self.spin, self.spin_speed,
                          self.renderer, self.destroy_self, self.audio_manager, is_player, self.life_time)

    def shoot_particles(self, self_rect):
        if self.renderer.on_screen(self_rect, True):
            particles_manager.register_particle(Particle(self.burst_sprite, self.pos, 0.5, self.renderer))
