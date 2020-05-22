import pygame


class Statistics:
    def __init__(self, renderer, small_font):
        self.enemies_killed = 0

        self.small_font = small_font
        self.renderer = renderer

    def update(self):
        self.renderer.draw_text_ui_bottomleft("Enemies killed: " + str(self.enemies_killed), self.small_font,
                                              pygame.Color("WHITE"), (100, self.renderer.h - 15))
