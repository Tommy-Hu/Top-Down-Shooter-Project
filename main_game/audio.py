from random import randint

import pygame


class AudioManager:
    # Creates a audio manager. The audio manager controls all the channels.
    def __init__(self, soundFXs, musics):
        self.soundFXs = soundFXs
        self.musics = musics
        pygame.mixer.set_num_channels(10)
        self.music_channel_1 = pygame.mixer.Channel(0)
        self.music_channel_2 = pygame.mixer.Channel(1)
        self.ui_fx_channel = pygame.mixer.Channel(2)
        self.projectiles_channel = pygame.mixer.Channel(3)
        self.hit_channel1 = pygame.mixer.Channel(4)
        self.hit_channel2 = pygame.mixer.Channel(5)
        self.death_channel = pygame.mixer.Channel(6)
        self.warnings_channel = pygame.mixer.Channel(7)
        self.pick_ups_channel = pygame.mixer.Channel(8)
        self.current_music_channel = 1

        self.music_channel_1.set_volume(0.3)
        self.music_channel_2.set_volume(0.3)
        self.projectiles_channel.set_volume(0.1)
        self.hit_channel1.set_volume(0.3)
        self.hit_channel2.set_volume(0.3)
        self.warnings_channel.set_volume(0.25)
        self.death_channel.set_volume(0.3)

    # Plays music on the music channel
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

    # As name suggests
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

    # Plays a sound on a random and free channel
    def play_quick_FX(self, key):
        self.soundFXs[key].play()

    def play_death_sound(self, key):
        self.death_channel.play(self.soundFXs[key])

    def play_warning_sound(self, key):
        self.warnings_channel.play(self.soundFXs[key])

    def play_pickup_sound(self, key):
        self.pick_ups_channel.play(self.soundFXs[key])

    # Plays a random sound in a list on a specific channel
    def play_random_sound_at_channel(self, channel, keys):
        key = randint(0, len(keys) - 1)
        channel.play(self.soundFXs[keys[key]])
