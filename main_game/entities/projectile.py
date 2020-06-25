import pygame.math

from entities.characters.player import Player
from particle_system import particles_manager
from particle_system.paticle import Particle
from utils.calculations import *


# Defines a projectile
class Projectile:
    def __init__(self, sprite, burst_sprite, pos, direction, speed, damage, spin, spin_speed, renderer,
                 destroy_callback, hit_sound,
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
        self.hit_sound = hit_sound

        self.destroy_self = destroy_callback
        self.life_time = life_time
        self.life_left = life_time

        self.audio_manager = audio_manager
        self.is_player = is_player

        self.burst_sprite = pygame.transform.scale(burst_sprite, (
            burst_sprite.get_width() * burst_scale_multiplier, burst_sprite.get_height() * burst_scale_multiplier))

    # Updates and redraws the projectile
    def update(self, walls, enemies, player, delta_time):
        new_sprite, new_rect = rot_center(self.original_sprite, self.spun_degrees)
        new_rect.center = self.pos

        if self.life_left <= 0:
            self.destroy_self(self)
            self.shoot_particles(new_rect)

        # Check collision
        if self.is_player:
            for enemy in enemies:
                if new_rect.colliderect(enemy.rect):
                    enemy.damage(self.damage)
                    self.shoot_particles(new_rect)
                    self.audio_manager.play_hit_sound(self.hit_sound)
                    self.destroy_self(self)
                    return
        else:
            if new_rect.colliderect(player.rect):
                player.damage(self.damage)
                self.shoot_particles(new_rect)
                self.audio_manager.play_hit_sound(self.hit_sound)
                self.destroy_self(self)
                return

        for wall in walls:
            if wall.check_collision_rect(new_rect):
                self.destroy_self(self)
                self.shoot_particles(new_rect)
                self.audio_manager.play_hit_sound(self.hit_sound)
                return

        # Move
        self.pos += self.dir * self.speed * delta_time
        self.renderer.add_to_canvas(new_sprite, new_rect.topleft)
        self.spun_degrees += self.spin_speed
        self.life_left -= delta_time

    # Clone
    def duplicate(self, is_player):
        return Projectile(self.original_sprite, self.burst_sprite, self.pos, self.dir, self.speed, self.damage,
                          self.spin, self.spin_speed,
                          self.renderer, self.destroy_self, self.hit_sound, self.audio_manager, is_player,
                          self.life_time)

    # Burst out particles handled in the particle system
    def shoot_particles(self, self_rect):
        if self.renderer.on_screen(self_rect, True):
            particles_manager.register_particle(Particle(self.burst_sprite, self.pos, 0.5, self.renderer))
