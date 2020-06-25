import pygame


# Defines a weapon that can be picked up by the player
class WeaponPickUp:
    def __init__(self, weapon_target, location, destroy_callback, weapon_original_shoot_rate, renderer):
        self.weapon_target = weapon_target.duplicate(True)
        self.weapon_target.shoot_rate = weapon_original_shoot_rate
        self.sprite = pygame.transform.scale(weapon_target.sprite, (150, 150))
        self.rect = pygame.Rect(self.sprite.get_rect())
        self.rect.center = location
        self.destroy_callback = destroy_callback
        self.renderer = renderer
        self.timer = 15

    # Redraws and updates this weapon pickup
    def update(self, player, delta_time):
        self.timer -= delta_time
        if self.rect.colliderect(player.rect):
            player.weapon = self.weapon_target
            self.destroy_callback(self)
            return
        if self.timer <= 0:
            self.destroy_callback(self)
            return

        self.renderer.add_to_canvas_center(self.sprite, self.rect.center)
