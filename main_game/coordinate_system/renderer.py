import pygame

from main_game.coordinate_system import coordinate


class Renderer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 1024)
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
        self.canvas.blit(source, top_left_pos)

    def add_to_canvas_center(self, source, center):
        center = coordinate.Coordinate.convert_to_screen(center, self.center_point_on_screen_in_world_coord,
                                                         pygame.Vector2(self.half_w, self.half_h))
        rect = pygame.Rect((0, 0), source.get_rect().size)
        rect.center = center
        self.canvas.blit(source, rect.topleft)

    def add_to_canvas_rgba_add(self, source, top_left_pos, is_global=True):
        if is_global:
            top_left_pos = coordinate.Coordinate.convert_to_screen(top_left_pos,
                                                                   self.center_point_on_screen_in_world_coord,
                                                                   pygame.Vector2(self.half_w, self.half_h))
        self.canvas.blit(source, top_left_pos, special_flags=pygame.BLEND_RGBA_ADD)

    def draw_line(self, p1, p2, width, color):
        pygame.draw.line(self.canvas, color,
                         coordinate.Coordinate.convert_to_screen(p1, self.center_point_on_screen_in_world_coord,
                                                                 pygame.Vector2(self.half_w, self.half_h)),
                         coordinate.Coordinate.convert_to_screen(p2, self.center_point_on_screen_in_world_coord,
                                                                 pygame.Vector2(self.half_w, self.half_h)), width)

    def draw_text_ui_center(self, text, font, color, center):
        txt = font.render(text, True, color)
        t_rect = txt.get_rect()
        t_rect.center = center
        self.canvas.blit(txt, t_rect)

    def draw_text_ui_topleft(self, text, font, color, topleft):
        txt = font.render(text, True, color)
        t_rect = txt.get_rect()
        t_rect.topleft = topleft
        self.canvas.blit(txt, t_rect)

    def draw_text_ui_bottomleft(self, text, font, color, bottomleft):
        txt = font.render(text, True, color)
        t_rect = txt.get_rect()
        t_rect.bottomleft = bottomleft
        self.canvas.blit(txt, t_rect)

    def render(self):
        self.surface.blit(self.canvas, (0, 0))
        pygame.display.flip()

    def set_center_point_on_screen_in_world_coord(self, world_coord):
        self.center_point_on_screen_in_world_coord = world_coord

    def get_pygame(self):
        return pygame

    def on_screen(self, rect, is_world):
        if is_world:
            rect.topleft = coordinate.Coordinate.convert_to_screen(rect.topleft,
                                                                   self.center_point_on_screen_in_world_coord,
                                                                   pygame.Vector2(self.half_w, self.half_h))
        return self.canvas.get_rect().colliderect(rect)
