import pygame

from entities.laser import Laser
from utils import calculations


# Defines a weapon
class Weapon:
    def __init__(self, sprite, projectile, shoot_rate, register_projectile, renderer, audio_manager,
                 sound_names=('shoot_1', 'shoot_2'), is_player_weapon=True):
        self.sprite = sprite
        self.sprite = pygame.transform.scale(self.sprite, (85, 85))
        if isinstance(projectile, Laser):
            self.projectile = projectile.duplicate(is_player_weapon, (0, 0), (1, 0), 1)
        else:
            self.projectile = projectile.duplicate(is_player_weapon)
        self.shoot_rate = shoot_rate

        self.sound_names = sound_names
        self.shoot_cooldown = 0
        # Register_projectile is a pointer pointing to a function that registers a projectile object.
        # This is used later when a weapon's ammo needs to burst
        self.register_projectile = register_projectile
        self.renderer = renderer
        self.audio_manager = audio_manager
        self.is_player_weapon = is_player_weapon

    # Updates and redraws itself
    def update(self, parent_rect, facing, shoot, delta_time):
        self_rect = pygame.Rect((0, 0), self.sprite.get_size())
        self_rect.center = parent_rect.center
        spin_angle = facing.angle_to(pygame.Vector2(1, 0))

        rotated_sprite, new_rect = calculations.rot_center(self.sprite, spin_angle)
        new_rect.center = self_rect.center
        self.renderer.add_to_canvas(rotated_sprite, new_rect.topleft)

        # Can shoot?
        if self.shoot_cooldown <= 0:
            if shoot:
                if facing.x != 0 and facing.y != 0:
                    # Shoot a projectile or a laser?
                    if isinstance(self.projectile, Laser):
                        new_p = self.projectile.duplicate(self.is_player_weapon, self_rect.center, facing.normalize(),
                                                          1200)
                    else:
                        new_p = self.projectile.duplicate(self.is_player_weapon)
                        new_p.dir = facing.normalize()
                        new_p.pos = self_rect.center
                    self.register_projectile(new_p)
                self.shoot_cooldown = self.shoot_rate
                self.audio_manager.play_random_sound_at_channel(self.audio_manager.projectiles_channel,
                                                                self.sound_names)
        else:
            self.shoot_cooldown -= delta_time

    # Duplicates this weapon
    def duplicate(self, is_player_weapon=False):
        return Weapon(self.sprite, self.projectile, self.shoot_rate, self.register_projectile, self.renderer,
                      self.audio_manager, self.sound_names, is_player_weapon)
