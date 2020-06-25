import pygame

from coordinate_system import coordinate


# Probably the most important class in all the files
# Logic: 1. When add_to_canvas, convert the coordinates from world coordinates to screen coordinates using my
# coordinate.py module.
#        2. Always draw into a memory canvas, and then draw everything on to the screen at once. (called double-
#        buffering)
class Renderer:
    def __init__(self):
        # Sounds and renderer init
        pygame.mixer.pre_init(44100, -16, 10, 1024)
        pygame.mixer.init(44100, -16, 10, 1024)
        pygame.init()
        pygame.font.init()

        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.w, self.h = self.surface.get_size()
        self.half_w, self.half_h = self.w // 2, self.h // 2

        self.canvas = pygame.Surface((self.w, self.h))
        self.center_point_on_screen_in_world_coord = pygame.Vector2(0, 0)
        self.heart_beats = False
        self.heart_beat_progress = -0.00001
        self.heart_increase = False

    # Fills canvas with color
    def clear_canvas(self, color=pygame.Color(255, 255, 255)):
        self.canvas.fill(color)

    # THE KEY METHOD IN THIS GAME!!!! RENDERS SOURCE CORRECTLY USING GLOBAL COORDS
    def add_to_canvas(self, source, top_left_pos, is_global=True):
        if is_global:
            # Convert to screen coords
            top_left_pos = coordinate.Coordinate.convert_to_screen(top_left_pos,
                                                                   self.center_point_on_screen_in_world_coord,
                                                                   pygame.Vector2(self.half_w, self.half_h))
        self.canvas.blit(source, top_left_pos)

    # same as add_to_canvas, but add_to_canvas adds a surface with a top-left coord, while this with a center coord.
    def add_to_canvas_center(self, source, center, is_global=True):
        if is_global:
            center = coordinate.Coordinate.convert_to_screen(center, self.center_point_on_screen_in_world_coord,
                                                             pygame.Vector2(self.half_w, self.half_h))
        rect = pygame.Rect((0, 0), source.get_rect().size)
        rect.center = center
        self.canvas.blit(source, rect.topleft)

    # For alpha and transparency purposes
    def add_to_canvas_rgba_add(self, source, top_left_pos, is_global=True):
        if is_global:
            top_left_pos = coordinate.Coordinate.convert_to_screen(top_left_pos,
                                                                   self.center_point_on_screen_in_world_coord,
                                                                   pygame.Vector2(self.half_w, self.half_h))
        self.canvas.blit(source, top_left_pos, special_flags=pygame.BLEND_RGBA_ADD)

    # Draws a line
    def draw_line(self, p1, p2, width, color):
        pygame.draw.line(self.canvas, color,
                         coordinate.Coordinate.convert_to_screen(p1, self.center_point_on_screen_in_world_coord,
                                                                 pygame.Vector2(self.half_w, self.half_h)),
                         coordinate.Coordinate.convert_to_screen(p2, self.center_point_on_screen_in_world_coord,
                                                                 pygame.Vector2(self.half_w, self.half_h)), width)

    # Draws UI >>>>>>
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

    def draw_text_ui_topright(self, text, font, color, topright):
        txt = font.render(text, True, color)
        t_rect = txt.get_rect()
        t_rect.topright = topright
        self.canvas.blit(txt, t_rect)

    # <<<<<<Draws UI

    # THIS SHOULD ONLY BE CALLED ONCE PER FRAME. This renders the memory canvas onto the screen.
    def render(self):
        if self.heart_beats or self.heart_beat_progress > 0:
            scale = self.heart_beat_progress / 50.0 + 1
            new_surface = pygame.transform.scale(self.canvas, (int(self.w * scale), int(self.h * scale)))
            difference = ((self.w - new_surface.get_width()) // 2, (self.h - new_surface.get_height()) // 2)
            self.surface.blit(new_surface, difference)
        else:
            self.surface.blit(self.canvas, (0, 0))
        pygame.display.flip()

    # Sets conversion factor
    def set_center_point_on_screen_in_world_coord(self, world_coord):
        self.center_point_on_screen_in_world_coord = world_coord

    # Grabs and returns the imported pygame package
    def get_pygame(self):
        return pygame

    # Is rect on the screen?  I.E Can you see rect on the screen?
    def on_screen(self, rect, is_world):
        if is_world:
            rect.topleft = coordinate.Coordinate.convert_to_screen(rect.topleft,
                                                                   self.center_point_on_screen_in_world_coord,
                                                                   pygame.Vector2(self.half_w, self.half_h))
        return self.canvas.get_rect().colliderect(rect)
