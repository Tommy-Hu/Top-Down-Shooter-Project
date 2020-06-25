import random
import pygame

from entities.characters.character import Character


# Defines the player
class Player(Character):
    def __init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health, die_callback,
                 audio_manager):
        Character.__init__(self, sprite, shadow_sprite, hurt_sprite, rect, renderer, speed, weapon, health)
        self.last_pos = (0, 0)
        self.die_callback = die_callback
        self.audio_manager = audio_manager

    def move(self, offset):
        Character.move(self, (self.rect.topleft[0] + offset.x, self.rect.topleft[1] + offset.y))

    # Updates the player with input_pack. Delta_time is the time it takes in seconds for the game to run 1 frame,
    # so multiplying everything with delta_time provides a smooth movement.
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

    # Render
    def draw_self(self, input_pack, delta_time):
        self.draw_to_renderer()
        facing = input_pack.mouse_pos - self.rect.center
        self.weapon.update(self.rect, facing, input_pack.mouse_buttons[0], delta_time)

    # Damage itself with amount damage
    def damage(self, amount):
        Character.damage(self, amount)
        self.audio_manager.play_hit_sound(random.choice(("player_hurt_1", "player_hurt_2")))
