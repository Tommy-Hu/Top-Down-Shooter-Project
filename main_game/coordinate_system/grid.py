import Queue
import math
import sys
import threading

import pygame

from utils import calculations


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

    def __init__(self, _walls, renderer, _from_vec=(-5000, -5000), _to_vec=(5000, 5000), grid_density=100):
        self.density = grid_density
        self.walls = _walls
        self.from_vec = _from_vec
        self.to_vec = _to_vec
        self.renderer = renderer
        self.nodes = []
        self.recalculate()
        self.LOCK = threading.Lock()

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

    def get_closest_available_node(self, node):
        nodes_to_do = [node]
        while True:
            if len(nodes_to_do) == 0:
                return None
            nd = nodes_to_do.pop(0)
            if nd.walkable:
                return nd
            x = nd.x
            y = nd.y

            if x - 1 >= 0:
                nodes_to_do.append(self.nodes[nd.x // self.density - 1][nd.y // self.density])
            if x + 1 < len(self.nodes):
                nodes_to_do.append(self.nodes[nd.x // self.density + 1][nd.y // self.density])
            if y - 1 >= 0:
                nodes_to_do.append(self.nodes[nd.x // self.density][nd.y // self.density - 1])
            if y + 1 < len(self.nodes):
                nodes_to_do.append(self.nodes[nd.x // self.density][nd.y // self.density + 1])

    def get_path(self, start, end):
        start = self.get_closest_available_node(start)
        end = self.get_closest_available_node(end)
        if start is None or end is None:
            return None

        with self.LOCK:
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

            with self.LOCK:
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

            with self.LOCK:
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
        self.grid = grid
        self.LOCK = threading.Lock()
        self.queues = (
            Queue.deque(),
            Queue.deque(),
        )
        self.player = None
        self.calc_thread_1 = threading.Thread(target=self.get_paths, args=(self.queues[0],))
        self.calc_thread_1.daemon = True
        self.calc_thread_2 = threading.Thread(target=self.get_paths, args=(self.queues[1],))
        self.calc_thread_2.daemon = True
        self.run_thread = True

    def get_paths(self, queue):
        while self.run_thread:
            with self.LOCK:
                if len(queue) <= 0:
                    continue
                enemy, finish_callback = queue.pop()
            if enemy is not None:
                path = self.grid.get_path_global_pos(enemy.rect.center, self.player.rect.center)
                if enemy is not None and finish_callback is not None:
                    finish_callback(path)

    def get_enemy_path(self, enemy, finish_callback):
        if len(self.queues[0]) > len(self.queues[1]):
            self.queues[1].appendleft((enemy, finish_callback))
        else:
            self.queues[0].appendleft((enemy, finish_callback))

    def start_thread(self):
        self.calc_thread_1.start()
        self.calc_thread_2.start()

    def stop_threads(self):
        self.run_thread = False
