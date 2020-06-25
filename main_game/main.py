# The Last Defender, by Tommy Hu
# All this class does is to grab all the assets and load the appropriate scene

import pygame

from coordinate_system.renderer import Renderer
import game, menu_scene, game_loading_scene, splash_scene, audio
from entities.wall import Wall

game_name = "The Last Defender"

clock = pygame.time.Clock()
renderer = Renderer()

pygame = renderer.get_pygame()

# Grab all the assets
title_font = pygame.font.Font("Assets\\Fonts\\plexifont.ttf", renderer.h / 6)
text_fonts = (
    pygame.font.Font("Assets\\Fonts\\whitrabt.ttf", renderer.h / 20),  # small
    pygame.font.Font("Assets\\Fonts\\whitrabt.ttf", renderer.h / 15),  # mid
    pygame.font.Font("Assets\\Fonts\\whitrabt.ttf", renderer.h / 10))  # big

audio_root = 'Assets\\Audios\\'
soundFXs = {
    "splash_sound": pygame.mixer.Sound(audio_root + 'Music\\win.wav'),
    "mouse_over_button_audio": pygame.mixer.Sound(audio_root + 'SoundFX\\Mouse_Over_Button.ogg'),
    "button_clicked_audio": pygame.mixer.Sound(audio_root + 'SoundFX\\Interface Push Button.ogg'),
    "warning": pygame.mixer.Sound(audio_root + 'SoundFX\\Warning Sound.ogg'),
    "player_hurt_1": pygame.mixer.Sound(audio_root + 'SoundFX\\Player Hurt 1.wav'),
    "player_hurt_2": pygame.mixer.Sound(audio_root + 'SoundFX\\Player Hurt 2.wav'),
    "thunder": pygame.mixer.Sound(audio_root + 'SoundFX\\Thunder.ogg'),
    "coin_pickup": pygame.mixer.Sound(audio_root + 'SoundFX\\Coin Pickup.wav'),
    "shoot_1": pygame.mixer.Sound(audio_root + 'SoundFX\\Shoot 1.wav'),
    "shoot_2": pygame.mixer.Sound(audio_root + 'SoundFX\\Shoot 2.wav'),
    "shoot_3": pygame.mixer.Sound(audio_root + 'SoundFX\\Shoot 3.wav'),
    "shoot_4": pygame.mixer.Sound(audio_root + 'SoundFX\\Shoot 4.ogg'),
    "enemy_death_1": pygame.mixer.Sound(audio_root + 'SoundFX\\Squish 1.wav'),
    "enemy_death_2": pygame.mixer.Sound(audio_root + 'SoundFX\\Squish 2.wav'),
    "hit_1": pygame.mixer.Sound(audio_root + 'SoundFX\\misc-bassdrop.ogg'),
    "spike": pygame.mixer.Sound(audio_root + 'SoundFX\\Spike.wav'),
    "health_pickup": pygame.mixer.Sound(audio_root + 'SoundFX\\Health Pickup.wav')
}

musics = {
    "menu_music": pygame.mixer.Sound(audio_root + 'Music\\meet-the-princess.wav'),
    "loading_loop": pygame.mixer.Sound(audio_root + 'Music\\loading.wav'),
    "game_music": pygame.mixer.Sound(audio_root + 'Music\\slow-travel.wav')
}

audio_manager = audio.AudioManager(soundFXs, musics)

pygame.mouse.set_visible(False)
splash_scene.splash(clock, renderer.surface, title_font, text_fonts, audio_manager, game_name)
print "Splash Screen Finished"

pygame.mouse.set_visible(True)


# Load into the game
def load_to_game():
    walls = [Wall(pygame.Rect(-100, -200, 300, 100), renderer),
             Wall(pygame.Rect(100, 200, 300, 100), renderer),
             Wall(pygame.Rect(-300, -500, 500, 200), renderer),
             Wall(pygame.Rect(600, -200, 400, 100), renderer),
             Wall(pygame.Rect(-500, -800, 300, 600), renderer),
             Wall(pygame.Rect(-1600, -1600, 200, 1000), renderer),
             Wall(pygame.Rect(-1600, 1600, 1000, 200), renderer),
             Wall(pygame.Rect(1600, 1600, 1000, 200), renderer),
             Wall(pygame.Rect(1600, -1600, 1000, 200), renderer),
             Wall(pygame.Rect(-2000, -3700, 300, 1000), renderer),
             Wall(pygame.Rect(-2000, 3700, 300, 1000), renderer),
             Wall(pygame.Rect(2000, 3700, 300, 1000), renderer),
             Wall(pygame.Rect(2000, -3700, 300, 1000), renderer),
             Wall(pygame.Rect(4300, -4300, 100, 100), renderer),
             Wall(pygame.Rect(-2000, -2900, 100, 100), renderer),
             Wall(pygame.Rect(4500, -900, 100, 100), renderer),
             Wall(pygame.Rect(400, -500, 100, 100), renderer),
             Wall(pygame.Rect(-1400, 4500, 100, 100), renderer),
             Wall(pygame.Rect(3800, -2900, 100, 100), renderer),
             Wall(pygame.Rect(-1900, 3100, 100, 100), renderer),
             Wall(pygame.Rect(-4700, 4400, 100, 100), renderer),
             Wall(pygame.Rect(-4300, 2300, 100, 100), renderer),
             Wall(pygame.Rect(-2300, 2000, 100, 100), renderer),
             Wall(pygame.Rect(-1200, -4800, 100, 100), renderer),
             Wall(pygame.Rect(1100, -3000, 100, 100), renderer),
             Wall(pygame.Rect(1500, -3400, 100, 100), renderer),
             Wall(pygame.Rect(3600, 4600, 100, 100), renderer),
             Wall(pygame.Rect(3700, 800, 100, 100), renderer),
             Wall(pygame.Rect(-4500, -3400, 100, 100), renderer),
             Wall(pygame.Rect(2000, 2000, 100, 100), renderer),
             Wall(pygame.Rect(4800, -4700, 100, 100), renderer),
             Wall(pygame.Rect(-1500, 3000, 100, 100), renderer),
             Wall(pygame.Rect(-1700, 2700, 100, 100), renderer),
             Wall(pygame.Rect(4300, 3600, 100, 100), renderer),
             Wall(pygame.Rect(4600, 2300, 100, 100), renderer),
             Wall(pygame.Rect(2700, 3700, 100, 100), renderer),
             Wall(pygame.Rect(-1400, 3700, 100, 100), renderer),
             Wall(pygame.Rect(500, -1100, 100, 100), renderer),
             Wall(pygame.Rect(3900, -4100, 100, 100), renderer),
             Wall(pygame.Rect(2900, -4900, 100, 100), renderer),
             Wall(pygame.Rect(4600, -1300, 100, 100), renderer),
             Wall(pygame.Rect(4300, 2000, 100, 100), renderer),
             Wall(pygame.Rect(3700, -1200, 100, 100), renderer),

             # Boundaries
             Wall(pygame.Rect(-5000, -5000, 100, 10000), renderer),
             Wall(pygame.Rect(-5000, -5000, 10000, 100), renderer),
             Wall(pygame.Rect(-5000, 4900, 10000, 100), renderer),
             Wall(pygame.Rect(4900, -5000, 100, 10000), renderer)
             ]

    # This dictionary contains all the paths of the picture assets
    s_paths = {"Circle": "Assets\\Sprites\\Circle.png",
               "Rect": "Assets\\Sprites\\Rectangle.png",
               "Smoke 1": "Assets\\Sprites\\Smoke 1.png",
               "Wall": "Assets\\Sprites\\Wall.png",
               "Rock 1": "Assets\\Sprites\\Rock 1.png",
               "Coin 1": "Assets\\Sprites\\Coin 1.png",
               "Coin 2": "Assets\\Sprites\\Coin 2.png",
               "Coin 3": "Assets\\Sprites\\Coin 3.png",
               "Coin 4": "Assets\\Sprites\\Coin 4.png",
               "Boss Bar": "Assets\\Sprites\\Boss Bar.png",
               "Boss Bar Sides": "Assets\\Sprites\\Boss Bar Sides.png",
               "Boss Bar Part": "Assets\\Sprites\\Boss Bar Part.png",
               "Heart": "Assets\\Sprites\\Heart.png",
               "Empty Heart": "Assets\\Sprites\\Empty Heart.png",
               "Onion": "Assets\\Sprites\\Onion.png",
               "Durian": "Assets\\Sprites\\Durian.png",
               "Mirror": "Assets\\Sprites\\Mirror.png",
               "Entity Shadow": "Assets\\Sprites\\Entity Shadow.png",
               "Enemy Spawner": "Assets\\Sprites\\Enemy Spawner.png",
               "Player": "Assets\\Sprites\\Player.png",
               "Alien Ammo": "Assets\\Sprites\\Alien Ammo.png",
               "Alien Ammo Burst": "Assets\\Sprites\\Alien Ammo Burst.png",
               "Squishy Enemy": "Assets\\Sprites\\Squishy Enemy.png",
               "Crimson 1": "Assets\\Sprites\\Crimson 1.png",
               "Crimson 2": "Assets\\Sprites\\Crimson 2.png",
               "Crimson 3": "Assets\\Sprites\\Crimson 3.png",
               "Angry Enemy 1": "Assets\\Sprites\\Angry Enemy 1.png",
               "Angry Enemy 2": "Assets\\Sprites\\Angry Enemy 2.png",
               "Slimy Enemy": "Assets\\Sprites\\Slimy Enemy.png",
               "Yummy Enemy 1": "Assets\\Sprites\\Yummy Monster F1.png",
               "Yummy Enemy 2": "Assets\\Sprites\\Yummy Monster F2.png",
               "Alien Launcher": "Assets\\Sprites\\Alien Launcher.png",
               "Tile 1": "Assets\\Sprites\\Grass Tile 1.png",
               "Tile 2": "Assets\\Sprites\\Grass Tile 2.png",
               "Blood 1": "Assets\\Sprites\\Blood 1.png",
               "Blood 2": "Assets\\Sprites\\Blood 2.png",
               }
    game_loading_scene.start_loading(audio_manager, s_paths, start_game, renderer,
                                     text_fonts[1], clock, walls)


# Starts the game
def start_game(sprites, grid, paths_mapper, walls):
    game.run_game = True
    game.clear()
    pygame.event.pump()
    print "Loaded Into Game!"
    pygame.mouse.set_visible(True)
    game.start_game(renderer, pygame.quit, clock, pygame, sprites, walls, grid, paths_mapper, audio_manager, show_menu,
                    load_to_game, text_fonts)


# load into main game scene
def show_menu():
    game.clear()
    menu_scene.refresh = True
    menu_scene.render(clock, renderer.surface, renderer.w, renderer.h, text_fonts, title_font,
                      audio_manager, load_to_game, game_name)


# This is where the program first goes to
show_menu()
pygame.mouse.set_visible(False)
print "Loading Sprites"

load_to_game()

# On a distant planet, the citizens lived a peaceful and rich life. However, a group of terrorists, called "The
# Invaders", entered their planet. The Invaders took away gradually the planet's fortune, and they kill everything
# that stands in their way. Now, they want to take the planet's core, which can greatly endanger the planet. A group
# of royal members quickly decided to form a union called "The Defenders", which is a group full of skilled citizens who
# wants to defend their poor planet.

# The group split into half, and each half defends one side of the planet. However, almost all your quadrant had been
# killed by the ruthless Invaders. You are one of the few who survived, and your job is to defend the East until the
# back up comes. Can you save the planet?
