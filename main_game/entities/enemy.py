import pygame

from main_game.entities.character import Character


class Enemy(Character):
    def __init__(self, sprite, rect, renderer, speed, weapon, grid, pathfinding_skip_threshold=50, attack_range=500):
        Character.__init__(self, sprite, rect, renderer, speed, weapon)
        self.grid = grid
        self.path = None
        self.next_pt = None
        self.pathfinding_skip_threshold = pathfinding_skip_threshold
        self.attack_range = attack_range
        self.need_new_path = True

    def move(self, offset):
        Character.move(self, (self.rect.topleft[0] + offset[0], self.rect.topleft[1] + offset[1]))

    def update_path(self, path):
        self.path = path

    def draw(self):
        Character.draw_to_renderer(self)

    def update(self, player):
        self_pos = pygame.Vector2(self.rect.center)
        if self_pos.distance_to(pygame.Vector2(player.rect.center)) <= self.attack_range:
            pass
        else:
            if self.next_pt is not None:
                if self.next_pt == self_pos:
                    self.pop_next_point()
                if self.next_pt == self_pos:
                    print "error at enemy update!"
                else:
                    dir = (self.next_pt - self_pos).normalize()
                    self.move(dir * self.speed)
                    if self_pos.distance_to(self.next_pt) <= self.pathfinding_skip_threshold:
                        self.pop_next_point()
            elif self.path is not None and len(self.path.nodes) > 1:
                self.pop_next_point()

        self.draw()

    def pop_next_point(self):
        if self.path is None or self.path.nodes is None:
            self.next_pt = None
            return
        if len(self.path.nodes) > 0:
            last_p = self.next_pt
            new_node = self.path.nodes.pop()
            self.next_pt = pygame.Vector2(new_node.x, new_node.y)
            if self.next_pt == last_p:
                if len(self.path.nodes) > 0:
                    new_node = self.path.nodes.pop()
                    self.next_pt = pygame.Vector2(new_node.x, new_node.y)
                else:
                    self.next_pt = None
