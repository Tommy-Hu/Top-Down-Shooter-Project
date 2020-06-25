import pygame

from particle_system import particles_manager


# Defines a base Character class. Later inherited by Enemy and Player (and Boss but Boss inherits from Enemy)
class Character(object):
    def __init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, default_weapon, health, scale=100,
                 hurt_size_increase_multipliers=1.5, death_audios=None):
        self.normal_sprite = pygame.transform.scale(sprite, (scale, scale))
        self.sprite = pygame.transform.scale(sprite, (scale, scale))
        self.rect = rect
        self.renderer = renderer
        self.speed = speed
        self.health = health
        self.max_health = health
        self.weapon = default_weapon
        self.death_audios = death_audios
        self.shadow_sprite = pygame.transform.scale(shadow_sprite, (scale, scale))
        if hurt_sprite is not None:
            self.hurt_sprite = pygame.transform.scale(hurt_sprite, (
                int(scale * hurt_size_increase_multipliers), int(scale * hurt_size_increase_multipliers)))
        else:
            self.hurt_sprite = None

        self.hurt_change_timer = 0

    # Moves itself to new_pos
    def move(self, new_pos):
        self.rect.topleft = new_pos

    # Re-renders itself
    def draw_to_renderer(self):
        self.renderer.add_to_canvas(self.shadow_sprite, (self.rect.left, self.rect.centery))
        self.renderer.add_to_canvas_center(self.sprite, self.rect.center)

    # Damage amount points of damage to this character
    def damage(self, amount):
        self.health -= amount
        particles_manager.create_blood_particle(self.rect.center)
        if self.hurt_sprite is not None:
            self.sprite = self.hurt_sprite
            self.hurt_change_timer = 0.5

    # Heal amount points of health
    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
