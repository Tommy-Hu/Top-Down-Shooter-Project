import random

import pygame

from particle_system.paticle import Particle

particles = []
sprites = {}
renderer = None


# this module controls ALL THE PARTICLES


# Initialize the module
def init(_sprites, _renderer):
    global sprites
    global renderer

    renderer = _renderer
    sprites = _sprites


# Redraws all the particles
def draw_particles(delta_time):
    for particle in particles:
        particle.update(delta_time, destroy_particle)


# Kill all the particles
def clear():
    global particles
    particles = []


# Registers a particle
def register_particle(particle):
    particles.append(particle)


# Kills a specific particle
def destroy_particle(particle):
    try:
        particles.remove(particle)
    except ValueError:
        print "Failed to destroy particle"


# Creates a blood particle
def create_blood_particle(position, size=45, duration=0.7, amount=7):
    sprite = random.choice((sprites["Blood 1"], sprites["Blood 2"]))
    sprite = pygame.transform.scale(sprite, (size, size))
    particles.append(Particle(sprite, position, duration, renderer, speed=300,
                              entities_count=amount))
