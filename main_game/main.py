import pygame

from coordinate_system.renderer import Renderer
from main_game import game, menu_scene, game_loading_scene, splash_scene, audio
from main_game.coordinate_system.grid import Grid, PathsMapper
from main_game.entities.wall import Wall

clock = pygame.time.Clock()
renderer = Renderer()

pygame = renderer.get_pygame()

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
    "shoot_1": pygame.mixer.Sound(audio_root + 'SoundFX\\Shoot 1.wav'),
    "shoot_2": pygame.mixer.Sound(audio_root + 'SoundFX\\Shoot 2.wav'),
    "shoot_3": pygame.mixer.Sound(audio_root + 'SoundFX\\Shoot 3.wav'),
    "shoot_4": pygame.mixer.Sound(audio_root + 'SoundFX\\Shoot 4.ogg'),
    "hit_1": pygame.mixer.Sound(audio_root + 'SoundFX\\misc-bassdrop.ogg')
}

musics = {
    "menu_music": pygame.mixer.Sound(audio_root + 'Music\\meet-the-princess.wav'),
    "loading_loop": pygame.mixer.Sound(audio_root + 'Music\\loading.wav'),
    "game_music": pygame.mixer.Sound(audio_root + 'Music\\slow-travel.wav')
}

audio_manager = audio.AudioManager(soundFXs, musics)


# pygame.mouse.set_visible(False)
# splash_scene.splash(clock, renderer.surface, title_font, text_fonts, audio_manager)
# print "Splash Screen Finished"
#
# pygame.mouse.set_visible(True)


def load_to_game():
    walls = [Wall(pygame.Rect(-100, -200, 300, 100), renderer),
             Wall(pygame.Rect(100, 200, 300, 100), renderer),
             Wall(pygame.Rect(-300, -500, 500, 200), renderer),
             Wall(pygame.Rect(600, -200, 400, 100), renderer),
             Wall(pygame.Rect(-500, -800, 300, 600), renderer),
             # Boundaries
             Wall(pygame.Rect(-5000, -5000, 100, 10000), renderer),
             Wall(pygame.Rect(-5000, -5000, 10000, 100), renderer),
             Wall(pygame.Rect(-5000, 4900, 10000, 100), renderer),
             Wall(pygame.Rect(4900, -5000, 100, 10000), renderer)
             ]

    s_paths = {"Circle": "Assets\\Sprites\\Circle.png",
               "Rect": "Assets\\Sprites\\Rectangle.png",
               "Heart": "Assets\\Sprites\\Heart.png",
               "Empty Heart": "Assets\\Sprites\\Empty Heart.png",
               "Onion": "Assets\\Sprites\\Onion.png",
               "Durian": "Assets\\Sprites\\Durian.png",
               "Entity Shadow": "Assets\\Sprites\\Entity Shadow.png",
               "Enemy Spawner": "Assets\\Sprites\\Enemy Spawner.png",
               "Player": "Assets\\Sprites\\Player.png",
               "Alien Ammo": "Assets\\Sprites\\Alien Ammo.png",
               "Alien Ammo Burst": "Assets\\Sprites\\Alien Ammo Burst.png",
               "Squishy Enemy": "Assets\\Sprites\\Squishy Enemy.png",
               "Angry Enemy 1": "Assets\\Sprites\\Angry Enemy 1.png",
               "Angry Enemy 2": "Assets\\Sprites\\Angry Enemy 2.png",
               "Slimy Enemy": "Assets\\Sprites\\Slimy Enemy.png",
               "Yummy Enemy 1": "Assets\\Sprites\\Yummy Monster F1.png",
               "Yummy Enemy 2": "Assets\\Sprites\\Yummy Monster F2.png",
               "Alien Launcher": "Assets\\Sprites\\Alien Launcher.png",
               "Tile": "Assets\\Sprites\\Grass Tile.png",
               }
    game_loading_scene.start_loading(audio_manager, s_paths, start_game, renderer,
                                     text_fonts[1], clock, walls)


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
                      audio_manager, load_to_game)


show_menu()
pygame.mouse.set_visible(False)
print "Loading Sprites"

load_to_game()

# On a distant planet, the Vainqits found our tiny blue planet.
# We became friends, and we traded goods.
# Our two kingdoms became the richest in our galaxy.
# Suddenly, a large group of Invaders came to the Vainqits.
# The Invaders slain the Vainqits' king, and scared away the citizens.
# The Invaders took all the treasure, and are heading towards our planet.
# You are our last hope to defend our planet.
# Now, wake up and take back what's lost!
