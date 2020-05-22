import pygame

from main_game.entities.character import Character


class Enemy(Character):
    def __init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health, grid, mapper, player,
                 pathfinding_skip_threshold=50,
                 attack_range=500, shoot_rate_decrease_percentage=50):
        Character.__init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health)
        self.grid = grid
        self.path = None
        self.mapper = mapper
        self.next_pt = None
        self.pathfinding_skip_threshold = pathfinding_skip_threshold
        self.attack_range = attack_range
        self.need_new_path = True
        self.weapon.shoot_rate *= 100.0 / shoot_rate_decrease_percentage
        self.player = player
        self.path_calculating = False

        self.next_update = 0

    def calculate_path(self):
        self.path_calculating = True
        self.mapper.get_enemy_path(self, self.finish_calc_path)

    def finish_calc_path(self, path):
        self.path = path
        self.path_calculating = False
        self.next_update = 1

    def move(self, offset):
        Character.move(self, (self.rect.topleft[0] + offset[0], self.rect.topleft[1] + offset[1]))

    def update_path(self, path):
        self.path = path

    def draw(self):
        Character.draw_to_renderer(self)

    def update(self, delta_time, kill_callback):
        if not self.path_calculating and self.next_update <= 0:
            self.calculate_path()

        if self.next_update > 0:
            self.next_update -= delta_time

        if self.health <= 0:
            kill_callback(self)
            return

        if self.hurt_change_timer <= 0:
            self.sprite = self.normal_sprite
        else:
            self.hurt_change_timer -= delta_time

        self_pos = pygame.Vector2(self.rect.center)
        if self.path is None:
            self.draw()
            return
        if self_pos.distance_to(pygame.Vector2(self.player.rect.center)) <= self.attack_range:
            self.draw()
            self.weapon.update(self.rect, self.player.rect.center - self_pos, True, delta_time)
        else:
            if self.next_pt is not None:
                if self.next_pt == self_pos:
                    self.pop_next_point()
                else:
                    dir = (self.next_pt - self_pos).normalize()
                    self.move(dir * self.speed * delta_time)
                    if self_pos.distance_to(self.next_pt) <= self.pathfinding_skip_threshold:
                        self.pop_next_point()
            elif self.path is not None and len(self.path.nodes) > 1:
                self.pop_next_point()
            self.draw()
            self.weapon.update(self.rect, self.player.rect.center - self_pos, False, delta_time)

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

    def duplicate_as_new(self, center_x, center_y):
        rect = pygame.Rect((0, 0), self.rect.size)
        rect.center = (center_x, center_y)
        return Enemy(self.normal_sprite, self.shadow_sprite, self.hurt_sprite, rect, self.renderer, self.speed,
                     self.weapon.duplicate(False), self.max_health,
                     self.grid, self.mapper, self.player, self.pathfinding_skip_threshold, self.attack_range)
