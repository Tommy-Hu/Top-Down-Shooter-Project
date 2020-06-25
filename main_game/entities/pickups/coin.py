import pygame


# Basic coin class
class Coin:
    def __init__(self, location, sprites, coin_size, renderer, destroy_callback):
        self.location = location
        self.coin_size = coin_size
        self.sprites = []
        for sprite in sprites:
            self.sprites.append(pygame.transform.scale(sprite, (coin_size, coin_size)))
        self.current_sprite_index = 0
        self.sprite_change_timer = 0.2
        self.renderer = renderer
        self.destroy_callback = destroy_callback

    def update(self, player, delta_time):
        # Plays the coins animation png by png
        self.sprite_change_timer -= delta_time
        if self.sprite_change_timer <= 0:
            self.sprite_change_timer = 0.2
            self.current_sprite_index += 1
            if self.current_sprite_index >= len(self.sprites):
                self.current_sprite_index = 0

        self_rect = self.sprites[self.current_sprite_index].get_rect()
        self_rect.center = self.location

        if self_rect.colliderect(player.rect):
            self.destroy_callback(self)

        self.renderer.add_to_canvas_center(self.sprites[self.current_sprite_index], self.location)

    def duplicate(self, pos):
        return Coin(pos, self.sprites, self.coin_size, self.renderer, self.destroy_callback)
