class Character(object):
    def __init__(self, sprite, rect, renderer, speed):
        self.sprite = sprite
        self.rect = rect
        self.renderer = renderer
        self.speed = speed

    def move(self, new_pos):
        self.rect.topleft = new_pos

    def draw_to_renderer(self):
        self.renderer.add_to_canvas(self.sprite, self.rect.topleft)
