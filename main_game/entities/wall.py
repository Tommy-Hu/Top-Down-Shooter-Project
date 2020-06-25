import pygame


# Defines a wall
class Wall:
    def __init__(self, rect, renderer, color=pygame.Color("BLACK"), breakable=False):
        self.rect = pygame.Rect(rect)
        self.renderer = renderer
        self.color = color
        self.breakable = breakable
        self.surface = pygame.Surface((rect.width, rect.height))
        self.surface.fill(color)
        self.tile_sprite = None

    # Creates a wall with scale tile_scale
    def create_with_tiles(self, tile_scale):
        self.tile_sprite = pygame.transform.scale(self.tile_sprite, (tile_scale, tile_scale))
        for y in range(0, self.rect.height, tile_scale):
            for x in range(0, self.rect.width, tile_scale):
                self.surface.blit(self.tile_sprite, (x, y))

    # Renders itself
    def update_to_renderer(self):
        self.renderer.add_to_canvas(self.surface, self.rect.topleft)

    # Moves itself
    def refresh_location(self, offset):
        self.rect.topleft = self.rect.topleft + offset

    # Collision detection with a point
    def check_collision_point(self, point):
        point = pygame.Vector2(point)
        return self.rect.collidepoint(point.x, point.y)

    # Check if two rects collide
    def check_collision_rect(self, rect):
        rect = pygame.Rect(rect)
        return self.rect.colliderect(rect)
