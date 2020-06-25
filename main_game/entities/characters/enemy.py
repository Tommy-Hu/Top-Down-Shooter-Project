import random

import pygame

from entities.characters.character import Character
from entities.pickups.weapon_pickup import WeaponPickUp


# Basic enemy class that inherits from the character class
class Enemy(Character):
    def __init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health, grid, mapper, player,
                 pathfinding_skip_threshold=50, attack_range=500, shoot_rate_decrease_percentage=50, death_audios=None,
                 health_drop_amount_max=1, scale=100, coin_drop_amount_max=2):
        self.weapon_original_shoot_rate = weapon.shoot_rate + 0.0

        Character.__init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health, scale,
                           death_audios=death_audios)
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
        self.health_drop_amount_max = health_drop_amount_max
        self.coin_drop_amount_max = coin_drop_amount_max

        # Check when to calculate a new path. You cannot calculate a new path all the time because your computer's
        # CPU would start burning. Only update the path when next_update is zero, otherwise, just decrease it by the FPS
        # / 1000.0
        self.next_update = 0

    # Requests a new path from paths_mapper
    def calculate_path(self):
        self.path_calculating = True
        self.mapper.get_enemy_path(self, self.finish_calc_path)

    # Callback that sets the current path to path
    def finish_calc_path(self, path):
        self.path = path
        self.path_calculating = False
        self.next_update = 1

    # Moves this enemy
    def move(self, offset):
        Character.move(self, (self.rect.topleft[0] + offset[0], self.rect.topleft[1] + offset[1]))

    def update_path(self, path):
        self.path = path

    # Renders this enemy.
    def draw(self):
        # This function is written in the super class: Character
        Character.draw_to_renderer(self)

    # Updates itself
    def update(self, delta_time, kill_callback, weapon_pickup_list):
        if not self.path_calculating and self.next_update <= 0:
            self.calculate_path()

        if self.next_update > 0:
            self.next_update -= delta_time

        if self.health <= 0:
            percentage = random.randint(1, 10)
            if percentage <= 1:
                weapon_pickup_list.append(
                    WeaponPickUp(self.weapon, self.rect.center, weapon_pickup_list.remove,
                                 self.weapon_original_shoot_rate, self.renderer))
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

        # Attack
        if self_pos.distance_to(pygame.Vector2(self.player.rect.center)) <= self.attack_range:
            self.draw()
            self.weapon.update(self.rect, self.player.rect.center - self_pos, True, delta_time)
        else:
            # Use a stack to push/pop new points
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

    # pop from the stack
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

    # Gets a random death sound
    def get_random_death_audio(self):
        if self.death_audios is not None and len(self.death_audios) > 0:
            return random.choice(self.death_audios)
        else:
            return None

    # Clones this enemy
    def duplicate_as_new(self, center_x, center_y):
        rect = pygame.Rect((0, 0), self.rect.size)
        rect.center = (center_x, center_y)
        weapon = self.weapon.duplicate(False)
        weapon.shoot_rate = self.weapon_original_shoot_rate
        return Enemy(self.normal_sprite, self.shadow_sprite, self.hurt_sprite, rect, self.renderer, self.speed,
                     weapon, self.max_health, self.grid, self.mapper, self.player,
                     self.pathfinding_skip_threshold, self.attack_range, death_audios=self.death_audios,
                     health_drop_amount_max=self.health_drop_amount_max, coin_drop_amount_max=self.coin_drop_amount_max)


# A special variant of enemy: Boss
class Boss(Enemy):
    def __init__(self, _sprites, scale, shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health, grid, mapper,
                 player, finish_callback):

        sprites = []
        for sprite in _sprites:
            sprites.append(pygame.transform.scale(sprite, (scale, scale)))

        super(Boss, self).__init__(sprites[0], shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health, grid,
                                   mapper, player, scale=scale)
        self.teleport_cooldown = 4.5
        self.current_tel_cooldown = 0.0
        self.attack_range = 1000
        self.path = None
        self.sprite_index = 0
        self.sprites = sprites
        self.sprite_change_timer = 0.5
        self.increase = True
        self.scale = scale
        self.finish_callback = finish_callback

    # The boss can teleport anywhere between 5 to 10 blocks to the player
    def teleport(self):
        player_x, player_y = self.player.rect.center[0], self.player.rect.center[1]
        self.rect.center = (
            player_x + random.randint(500, 1000) * self.get_random_pn1(),
            player_y + random.randint(500, 1000) * self.get_random_pn1())

    # Gets random positive-negative-1
    def get_random_pn1(self):
        return random.choice((-1, 1))

    # Updates this enemy
    def update(self, delta_time, kill_callback, pickups):
        self.sprite_change_timer -= delta_time
        if self.sprite_change_timer <= 0:
            self.sprite_change_timer = 0.5
            self.sprite = self.sprites[self.sprite_index]
            self.normal_sprite = self.sprites[self.sprite_index]
            if self.increase:
                self.sprite_index += 1
                if self.sprite_index >= len(self.sprites):
                    self.increase = False
                    self.sprite_index = len(self.sprites) - 1
            else:
                self.sprite_index -= 1
                if self.sprite_index < 0:
                    self.increase = True
                    self.sprite_index = 0

        # calls the super's update
        super(Boss, self).update(delta_time, kill_callback, pickups)
        if self.health <= 0:
            self.finish_callback()

        self.current_tel_cooldown -= delta_time
        if self.current_tel_cooldown <= 0:
            self.teleport()
            self.current_tel_cooldown = self.teleport_cooldown

    # Clone
    def duplicate_as_new(self, center_x, center_y):
        rect = pygame.Rect((0, 0), self.rect.size)
        rect.center = (center_x, center_y)
        return Boss(self.sprites, self.scale, self.shadow_sprite, self.hurt_sprite, self.rect, self.renderer,
                    self.speed, self.weapon.duplicate(False), self.max_health, self.grid, self.mapper, self.player,
                    self.finish_callback)
