from random import Random

import pygame


# Define one set of particles (that is, one burst of particles).
class Particle:
    def __init__(self, sprite, location, duration, renderer, speed=500, entities_count=5):
        self.sprite = sprite
        self.location = location
        self.duration = duration
        self.life_left = duration
        self.renderer = renderer
        self.entities_count = entities_count
        self.particle_entities = []
        self.speed = speed
        for i in range(0, entities_count):
            self.particle_entities.append(
                ParticleEntity(self.location, self.get_random_dir().normalize() * speed,
                               self.get_sprite_with_random_rot(sprite), renderer))

    # Gets a random vector
    def get_random_dir(self):
        random = Random()
        return pygame.Vector2(random.uniform(-100, 100), random.uniform(-100, 100))

    # Gets a random angle
    def get_random_rot(self):
        random = Random()
        return random.uniform(0, 360)

    # Returns the sprite in a randomly rotated form
    def get_sprite_with_random_rot(self, sprite):
        return pygame.transform.rotate(sprite, self.get_random_rot())

    # Redraws the particle
    def update(self, delta_time, destroy_callback):
        self.life_left -= delta_time
        if self.life_left <= 0:
            destroy_callback(self)
            return
        alpha = int(self.life_left / self.duration * 255)
        for entity in self.particle_entities:
            entity.update_and_draw(delta_time, alpha)

    # Clones a particle
    def duplicate(self):
        return Particle(self.sprite, self.location, self.duration, self.renderer, self.entities_count)


# Defines all the particle entities
# This is what you see on the screen while the class at the top is just a definition
class ParticleEntity:
    def __init__(self, center_pos, vector, sprite, renderer):
        self.rect = sprite.get_rect()
        self.rect.center = center_pos
        self.vector = pygame.Vector2(vector)
        self.sprite = sprite.convert()
        self.sprite.set_colorkey((0, 0, 0))

        self.renderer = renderer

    def update_and_draw(self, delta_time, alpha):
        self.sprite.set_alpha(alpha)
        self.rect.topleft += self.vector * delta_time
        self.renderer.add_to_canvas(self.sprite, self.rect.topleft)
