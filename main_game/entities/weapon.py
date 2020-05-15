import pygame

from main_game.utils import calculations


class Weapon:
    def __init__(self, sprite, projectile, shoot_rate_in_frames, register_projectile, renderer):
        self.sprite = sprite
        self.projectile = projectile
        self.shoot_rate_in_frames = shoot_rate_in_frames

        self.shoot_cooldown = 0
        self.register_projectile = register_projectile
        self.renderer = renderer

    def update(self, parent_rect, facing, shoot):
        self_rect = pygame.Rect((0, 0), self.sprite.get_size())
        self_rect.center = parent_rect.center
        spin_angle = facing.angle_to(pygame.Vector2(1, 0))

        rotated_sprite, new_rect = calculations.rot_center(self.sprite, spin_angle)
        new_rect.center = self_rect.center
        self.renderer.add_to_canvas(rotated_sprite, new_rect.topleft)

        if self.shoot_cooldown <= 0:
            if shoot:
                new_p = self.projectile.duplicate()
                new_p.dir = facing.normalize()
                new_p.pos = self_rect.center
                self.register_projectile(new_p)
                self.shoot_cooldown = self.shoot_rate_in_frames
        else:
            self.shoot_cooldown -= 1
