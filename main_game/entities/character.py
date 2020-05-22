import pygame


class Character(object):
    def __init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, default_weapon, health, scale=100,
                 hurt_size_increase_multipliers=1.5):
        self.normal_sprite = pygame.transform.scale(sprite, (scale, scale))
        self.sprite = pygame.transform.scale(sprite, (scale, scale))
        self.rect = rect
        self.renderer = renderer
        self.speed = speed
        self.health = health
        self.max_health = health
        self.weapon = default_weapon
        self.shadow_sprite = pygame.transform.scale(shadow_sprite, (scale, scale))
        if hurt_sprite is not None:
            self.hurt_sprite = pygame.transform.scale(hurt_sprite, (
                int(scale * hurt_size_increase_multipliers), int(scale * hurt_size_increase_multipliers)))
        else:
            self.hurt_sprite = None

        self.hurt_change_timer = 0

    def move(self, new_pos):
        self.rect.topleft = new_pos

    def draw_to_renderer(self):
        self.renderer.add_to_canvas(self.shadow_sprite, (self.rect.left, self.rect.centery))
        self.renderer.add_to_canvas_center(self.sprite, self.rect.center)

    def damage(self, amount):
        self.health -= amount
        if self.hurt_sprite is not None:
            self.sprite = self.hurt_sprite
            self.hurt_change_timer = 0.5

    def heal(self, amount):
        self.health += amount
