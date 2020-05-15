import pygame

from main_game.coordinate_system import coordinate


class Renderer:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.w, self.h = self.surface.get_size()
        self.half_w, self.half_h = self.w // 2, self.h // 2

        self.canvas = pygame.Surface((self.w, self.h))
        self.center_point_on_screen_in_world_coord = pygame.Vector2(0, 0)

    def clear_canvas(self, color=pygame.Color(255, 255, 255)):
        self.canvas.fill(color)

    def add_to_canvas(self, source, top_left_pos, is_global=True):
        if is_global:
            top_left_pos = coordinate.Coordinate.convert_to_screen(top_left_pos,
                                                                   self.center_point_on_screen_in_world_coord,
                                                                   pygame.Vector2(self.half_w, self.half_h))
        source_rect = source.get_rect()
        source_rect.topleft = top_left_pos
        if source_rect.colliderect(self.canvas.get_rect()):
            self.canvas.blit(source, top_left_pos)

    def draw_line(self, p1, p2, width, color):
        pygame.draw.line(self.canvas, color,
                         coordinate.Coordinate.convert_to_screen(p1, self.center_point_on_screen_in_world_coord,
                                                                 pygame.Vector2(self.half_w, self.half_h)),
                         coordinate.Coordinate.convert_to_screen(p2, self.center_point_on_screen_in_world_coord,
                                                                 pygame.Vector2(self.half_w, self.half_h)), width)

    def render(self):
        self.surface.blit(self.canvas, (0, 0))
        pygame.display.flip()

    def set_center_point_on_screen_in_world_coord(self, world_coord):
        self.center_point_on_screen_in_world_coord = world_coord

    def get_pygame(self):
        return pygame
