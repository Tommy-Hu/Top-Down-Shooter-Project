from random import randint

import pygame


class AudioManager:
    def __init__(self, soundFXs, musics):
        self.soundFXs = soundFXs
        self.musics = musics
        self.music_channel_1 = pygame.mixer.Channel(0)
        self.music_channel_2 = pygame.mixer.Channel(1)
        self.ui_fx_channel = pygame.mixer.Channel(2)
        self.projectiles_channel = pygame.mixer.Channel(3)
        self.hit_channel1 = pygame.mixer.Channel(4)
        self.hit_channel2 = pygame.mixer.Channel(5)
        self.others_channel = pygame.mixer.Channel(6)
        self.current_music_channel = 1

        self.music_channel_1.set_volume(0.3)
        self.music_channel_2.set_volume(0.3)
        self.projectiles_channel.set_volume(0.1)
        self.hit_channel1.set_volume(0.3)
        self.hit_channel2.set_volume(0.3)

    def play_music(self, key, loop=True, fade_time=2000, volume=0.3):
        music = self.musics[key]
        if self.current_music_channel == 1:
            self.music_channel_1.fadeout(fade_time)
            self.current_music_channel = 2
            self.music_channel_2.set_volume(volume)
            if loop:
                self.music_channel_2.play(Sound=music, loops=-1, fade_ms=fade_time)
            else:
                self.music_channel_2.play(Sound=music, fade_ms=fade_time)
        else:
            self.music_channel_2.fadeout(fade_time)
            self.current_music_channel = 1
            self.music_channel_1.set_volume(volume)
            if loop:
                self.music_channel_1.play(Sound=music, loops=-1, fade_ms=fade_time)
            else:
                self.music_channel_1.play(Sound=music, fade_ms=fade_time)

    def fade_out_music(self, time=2000):
        self.music_channel_1.fadeout(time)
        self.music_channel_2.fadeout(time)

    def play_ui_sound(self, key):
        self.ui_fx_channel.play(self.soundFXs[key])

    def play_projectile_sound(self, key):
        self.projectiles_channel.play(self.soundFXs[key])

    def play_hit_sound(self, key):
        if self.hit_channel2.get_busy():
            self.hit_channel1.play(self.soundFXs[key])
        else:
            self.hit_channel2.play(self.soundFXs[key])

    def play_quick_FX(self, key):
        self.soundFXs[key].play()

    def play_random_sound_at_channel(self, channel, keys):
        key = randint(0, len(keys) - 1)
        channel.play(self.soundFXs[keys[key]])
