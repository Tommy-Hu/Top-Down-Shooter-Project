import pygame

from main_game.entities.character import Character


class Player(Character):
    def __init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health, die_callback):
        Character.__init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health)
        self.last_pos = (0, 0)
        self.die_callback = die_callback

    def move(self, offset):
        Character.move(self, (self.rect.topleft[0] + offset.x, self.rect.topleft[1] + offset.y))

    def update_with_input(self, input_pack, delta_time):
        if self.health <= 0:
            self.die_callback()
            return

        if self.hurt_change_timer <= 0:
            self.sprite = self.normal_sprite
        else:
            self.hurt_change_timer -= delta_time

        self.last_pos = self.rect.topleft
        amount = pygame.Vector2(input_pack.move_X * float(self.speed), input_pack.move_Y * float(self.speed))
        self.move(amount * delta_time)

    def draw_self(self, input_pack, delta_time):
        self.draw_to_renderer()
        facing = input_pack.mouse_pos - self.rect.center
        self.weapon.update(self.rect, facing, input_pack.mouse_buttons[0], delta_time)
