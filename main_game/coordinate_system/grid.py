import math
import sys
import threading

import pygame

from main_game.utils import calculations


class Node:
    def __init__(self, x, y, walkable, renderer):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.renderer = renderer
        self.sprite = pygame.Surface((10, 10), pygame.SRCALPHA, 32)
        self.sprite.convert_alpha()
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0
        self.parent = None

    def draw(self):
        if self.walkable:
            pygame.draw.circle(self.sprite, pygame.Color("BLUE"), (5, 5), 5)
        else:
            pygame.draw.circle(self.sprite, pygame.Color("RED"), (5, 5), 5)

        self.renderer.add_to_canvas(self.sprite,
                                    pygame.Vector2(self.x, self.y) - pygame.Vector2(self.sprite.get_size()) // 2)

    def duplicate_without_costs(self):
        return Node(self.x, self.y, self.walkable, self.renderer)

    def __str__(self):
        return str(self.x) + ", " + str(self.y)

    def __eq__(self, other):
        return other is not None and isinstance(other, Node) and self.x == other.x and self.y == other.y


class Grid:

    def __init__(self, _walls, renderer, _from_vec=(-10000, -10000), _to_vec=(10000, 10000), grid_density=100):
        self.density = grid_density
        self.walls = _walls
        self.from_vec = _from_vec
        self.to_vec = _to_vec
        self.renderer = renderer
        self.nodes = []
        self.recalculate()

    def recalculate(self):
        for y in range(self.from_vec[1], self.to_vec[1] + self.density, self.density):
            line = []
            for x in range(self.from_vec[0], self.to_vec[0] + self.density, self.density):
                line.append(Node(x, y, self.check_walkable(x, y), self.renderer))
            self.nodes.append(line)

    def check_walkable(self, x, y):
        for wall in self.walls:
            if wall.check_collision_point(pygame.Vector2(x, y)) or calculations.on_rect(wall.rect, (x, y)):
                return False
        return True

    def refresh(self):
        for line in self.nodes:
            for node in line:
                node.draw()

    def get_path(self, start, end):
        if not start.walkable or not end.walkable:
            return None

        start = start.duplicate_without_costs()
        end = end.duplicate_without_costs()

        open_set = []
        closed_set = []
        start.len = 0
        open_set.append(start)

        offset = [self.from_vec[0] // self.density, self.from_vec[1] // self.density]

        while True:
            if len(open_set) <= 0:
                return None

            node = None
            smallest_f = sys.maxint
            smallest_h = sys.maxint
            for n in open_set:
                if n.fcost < smallest_f:
                    smallest_f = n.fcost
                    node = n
                    smallest_h = n.hcost
                elif n.fcost == smallest_f:
                    if n.hcost < smallest_h:
                        smallest_h = n.hcost
                        node = n

            open_set.remove(node)
            closed_set.append(node)

            if node.__eq__(end):
                path = Path()
                n = node
                while True:
                    path.nodes.append(n)
                    n = n.parent
                    if n is None:
                        break

                return path

            x = node.x // self.density - offset[0]
            y = node.y // self.density - offset[1]

            neighbors = self.get_walkable_neighbors(x, y, closed_set)
            for neighbor in neighbors:
                if node.gcost + 1 < neighbor.gcost or neighbor not in open_set:
                    neighbor = neighbor.duplicate_without_costs()
                    neighbor.gcost = node.gcost + 1
                    neighbor.hcost = Grid.heuristic(neighbor, end)
                    neighbor.fcost = neighbor.gcost + neighbor.hcost
                    neighbor.parent = node
                    if neighbor not in open_set:
                        open_set.append(neighbor)

            neighbors = self.get_walkable_neighbors_diagonal(x, y, closed_set)
            for neighbor in neighbors:
                if node.gcost + 1 < neighbor.gcost or neighbor not in open_set:
                    neighbor = neighbor.duplicate_without_costs()
                    neighbor.gcost = node.gcost + 1.4
                    neighbor.hcost = Grid.heuristic(neighbor, end)
                    neighbor.fcost = neighbor.gcost + neighbor.hcost
                    neighbor.parent = node
                    if neighbor not in open_set:
                        open_set.append(neighbor)

    def get_path_global_pos(self, start, end):
        start_gp = self.convert_to_grid_point(start)
        end_gp = self.convert_to_grid_point(end)
        return self.get_path(self.nodes[int(start_gp.y)][int(start_gp.x)], self.nodes[int(end_gp.y)][int(end_gp.x)])

    def draw_path(self, path):
        if path is None:
            return
        last_node = None
        for node in path.nodes:
            if last_node is not None:
                self.renderer.draw_line((node.x, node.y),
                                        (last_node.x, last_node.y),
                                        10, pygame.Color("GREEN"))
            last_node = node

    def is_walkable(self, x, y, closed_set):
        if 0 <= x <= (self.to_vec[0] - self.from_vec[0]) // self.density and 0 <= y <= (
                self.to_vec[1] - self.from_vec[1]) // self.density:
            nd = self.nodes[y][x]
            if nd.walkable and nd not in closed_set:
                return True

    def get_walkable_neighbors(self, x, y, closed_set):
        ans_set = []
        if self.is_walkable(x - 1, y, closed_set):
            ans_set.append(self.nodes[y][x - 1])
        if self.is_walkable(x + 1, y, closed_set):
            ans_set.append(self.nodes[y][x + 1])
        if self.is_walkable(x, y - 1, closed_set):
            ans_set.append(self.nodes[y - 1][x])
        if self.is_walkable(x, y + 1, closed_set):
            ans_set.append(self.nodes[y + 1][x])

        return ans_set

    def get_walkable_neighbors_diagonal(self, x, y, closed_set):
        ans_set = []

        if self.is_walkable(x - 1, y - 1, closed_set):
            ans_set.append(self.nodes[y - 1][x - 1])
        if self.is_walkable(x + 1, y + 1, closed_set):
            ans_set.append(self.nodes[y + 1][x + 1])
        if self.is_walkable(x + 1, y - 1, closed_set):
            ans_set.append(self.nodes[y - 1][x + 1])
        if self.is_walkable(x - 1, y + 1, closed_set):
            ans_set.append(self.nodes[y + 1][x - 1])

        return ans_set

    def get_dis(self, node1, node2):
        node1 = pygame.Vector2(node1.x // self.density, node1.y // self.density)
        node2 = pygame.Vector2(node2.x // self.density, node2.y // self.density)
        return node1.distance_to(node2)

    def roundup_to_density(self, x):
        return int(math.ceil(x / float(self.density))) * self.density

    def convert_to_grid_point(self, world_point):
        wp = pygame.Vector2(world_point)
        wp = wp // self.density
        wp.x = wp.x - self.from_vec[0] // self.density
        wp.y = wp.y - self.from_vec[1] // self.density
        return wp

    @staticmethod
    def heuristic(a, b):
        x1, y1 = a.x, a.y
        x2, y2 = b.x, b.y
        return abs(x1 - x2) + abs(y1 - y2)


class Path:
    def __init__(self):
        self.nodes = []
        self.len = 0


class PathsMapper:
    def __init__(self, grid):
        self.map = []
        self.is_finished = True
        self.enemies_left = 0
        self.grid = grid
        self.LOCK = threading.Lock()
        self.threads_running = []

    def get_enemy_path(self, enemy, player, finish_callback):
        if enemy.next_pt is None:
            finish_callback(enemy, self.grid.get_path_global_pos(enemy.rect.center, player.rect.center))
        else:
            finish_callback(enemy, self.grid.get_path_global_pos(enemy.next_pt, player.rect.center))

    def finish_callback(self, enemy, path):
        with self.LOCK:
            self.enemies_left -= 1
            enemy.update_path(path)
            self.map.append([enemy, path])
        if self.enemies_left == 0:
            self.is_finished = True

    def get_all_enemy_paths(self, enemies, player):
        self.map = []
        self.threads_running = []
        self.is_finished = False
        self.enemies_left = len(enemies)
        for enemy in enemies:
            new_thread = threading.Thread(target=self.get_enemy_path, args=(enemy, player, self.finish_callback))
            new_thread.daemon = True
            self.threads_running.append(new_thread)
            new_thread.start()
