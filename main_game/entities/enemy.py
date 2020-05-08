from pygame import Vector2

from main_game.entities.character import Character


class Enemy(Character):
    def __init__(self, sprite, rect, renderer, speed):
        Character.__init__(self, sprite, rect, renderer, speed)

    def move(self, offset):
        Character.move(self, self.rect.topleft + offset)

    def update_with_player_topleft(self, player_topleft):
        dir = Vector2(player_topleft.x - self.rect.topleft[0], player_topleft.y - self.rect.topleft[1]).normalize()
        self.move(dir * self.speed)
