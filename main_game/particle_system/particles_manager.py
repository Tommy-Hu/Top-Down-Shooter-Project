import random

import pygame

from particle_system.paticle import Particle

particles = []
sprites = {}
renderer = None


def init(_sprites, _renderer):
    global sprites
    global renderer

    renderer = _renderer
    sprites = _sprites


def draw_particles(delta_time):
    for particle in particles:
        particle.update(delta_time, destroy_particle)


def clear():
    global particles
    particles = []


def register_particle(particle):
    particles.append(particle)


def destroy_particle(particle):
    try:
        particles.remove(particle)
    except ValueError:
        print "Failed to destroy particle"


def create_blood_particle(position, size=45, duration=0.7, amount=7):
    sprite = random.choice((sprites["Blood 1"], sprites["Blood 2"]))
    sprite = pygame.transform.scale(sprite, (size, size))
    particles.append(Particle(sprite, position, duration, renderer, speed=300,
                              entities_count=amount))
