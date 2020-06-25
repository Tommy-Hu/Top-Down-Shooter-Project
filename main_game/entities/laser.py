import pygame

from entities.characters.enemy import Enemy
from entities.characters.player import Player
from utils import calculations


# A basic laser class
class Laser:
    # Calculates all the maths and initialize the laser instance
    def __init__(self, pos, dir, length, damage, renderer, is_player, color, width, destroy_callback,
                 through_walls=True):
        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(dir)
        self.length = length
        self.end = self.pos + (self.length * self.dir)
        self.renderer = renderer
        self.is_player = is_player
        self.color = color
        self.width = width
        self.through_walls = through_walls
        self.destroy_callback = destroy_callback
        self.damage = damage
        w, h = int(abs((self.pos - self.end).x)), int(abs((self.pos - self.end).y))
        self.surface = pygame.Surface((w, h))
        self.surface.fill(pygame.Color("BLACK"))
        self.surface.convert_alpha()
        self.surface.set_colorkey((0, 0, 0))

        self.real_top_left = self.pos
        #
        # Get which quadrant this laser is actually in. I'm not just using a pygame.draw.line because I want
        # the laser to fade out. That's why I am creating a new surface for each laser.
        #
        relative_end = (self.end - self.pos)
        if relative_end.x > 0 and relative_end.y > 0:
            pygame.draw.line(self.surface, self.color, (0, 0), (w, h), width)
            self.real_top_left = self.pos
        elif relative_end.x < 0 < relative_end.y:
            pygame.draw.line(self.surface, self.color, (w, 0), (0, h), width)
            self.real_top_left = pygame.Vector2(self.pos.x - w, self.pos.y)
        elif relative_end.x > 0 > relative_end.y:
            pygame.draw.line(self.surface, self.color, (0, h), (w, 0), width)
            self.real_top_left = pygame.Vector2(self.pos.x, self.pos.y - h)
        else:
            pygame.draw.line(self.surface, self.color, (w, h), (0, 0), width)
            self.real_top_left = pygame.Vector2(self.pos.x - w, self.pos.y - h)

        self.damaged = False
        self.total_life_time = 0.2
        self.life_time = 0.2

    # Updates this laser
    def update(self, walls, enemies, player, delta_time):
        self.life_time -= delta_time
        if self.life_time <= 0:
            self.destroy_callback(self)
            return
        alpha = int(self.life_time / self.total_life_time * 255.0)
        self.surface.set_alpha(alpha)
        self.renderer.add_to_canvas(self.surface, self.real_top_left)

        # Check if it hits anything
        if not self.damaged:
            if self.is_player:
                for enemy in enemies:
                    if calculations.segment_intersect_rect(enemy.rect, (self.pos, self.end)):
                        enemy.damage(self.damage)
            else:
                if calculations.segment_intersect_rect(player.rect, (self.pos, self.end)):
                    player.damage(self.damage)
            self.damaged = True

    # Clones a laser
    def duplicate(self, is_player, pos, dir, len):
        return Laser(pos, dir, len, self.damage, self.renderer, is_player, self.color, self.width,
                     self.destroy_callback, self.through_walls)
