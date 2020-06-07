import pygame


class HealthContainer:
    def __init__(self, sprite, pos, scale, value, renderer, destroy_callback, pick_up_sound, audio_manager):
        self.sprite = pygame.transform.scale(sprite, (scale, scale))
        self.pos = pos
        self.rect = pygame.Rect(pos, (scale, scale))
        self.scale = scale
        self.value = value
        self.renderer = renderer
        self.destroy_callback = destroy_callback

        self.current_size_percentage = 0
        self.increase_size = True
        self.life_time = 10
        self.pick_up_sound = pick_up_sound
        self.audio_manager = audio_manager

    def update(self, player, delta_time):
        self.life_time -= delta_time
        if self.life_time <= 0:
            self.destroy_callback(self)
            return
        if self.increase_size:
            self.current_size_percentage += delta_time
            if self.current_size_percentage >= 1:
                self.increase_size = False
        else:
            self.current_size_percentage -= delta_time
            if self.current_size_percentage <= 0:
                self.increase_size = True

        self.renderer.add_to_canvas_center(pygame.transform.scale(self.sprite, (
            int(self.scale * (self.current_size_percentage + 1)),
            int(self.scale * (self.current_size_percentage + 1)))), self.pos)
        if player.rect.colliderect(self.rect):
            player.heal(self.value)
            self.audio_manager.play_pickup_sound(self.pick_up_sound)
            self.destroy_callback(self)

    def duplicate(self, pos):
        return HealthContainer(self.sprite, pos, self.scale, self.value, self.renderer, self.destroy_callback,
                               self.pick_up_sound, self.audio_manager)
