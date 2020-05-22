from main_game.particle_system.paticle import Particle

particles = []


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
