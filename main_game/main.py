import pygame

from coordinate_system.renderer import Renderer

from main_game import splash_scene, menu_scene, game

clock = pygame.time.Clock()
renderer = Renderer()

pygame = renderer.get_pygame()

title_font = pygame.font.Font("Assets\\Fonts\\plexifont.ttf", renderer.h / 6)
text_fonts = (
    pygame.font.Font("Assets\\Fonts\\whitrabt.ttf", renderer.h / 20),  # small
    pygame.font.Font("Assets\\Fonts\\whitrabt.ttf", renderer.h / 15),  # mid
    pygame.font.Font("Assets\\Fonts\\whitrabt.ttf", renderer.h / 10))  # big

mouse_over_button_audio = pygame.mixer.Sound('Assets\\Audios\\SoundFX\\Mouse_Over_Button.ogg')
button_clicked_audio = pygame.mixer.Sound('Assets\\Audios\\SoundFX\\Interface Push Button.ogg')

# splash_scene.splash(clock, renderer.surface, title_font, text_fonts)
# print "Splash Screen Finished"

# load into main game scene
menu_scene.render(clock, renderer.surface, renderer.w, renderer.h, text_fonts, title_font, mouse_over_button_audio,
                  button_clicked_audio)
print "Loaded Into Game!"

game.start_game(renderer, pygame.quit, clock)
