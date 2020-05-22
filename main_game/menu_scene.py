import sys

import pygame

from ui_assets import GraphicalControls

refresh = True

audio_manager = None
start_game_callback = None


def render(clock, surface, w, h, text_fonts, title_font, _audio_manager, _start_game_callback):
    global audio_manager
    global start_game_callback

    start_game_callback = _start_game_callback
    audio_manager = _audio_manager
    audio_manager.play_music('menu_music', volume=0.1)

    title_font.set_bold(False)

    title_text = title_font.render('Shape Shooter', True, pygame.Color(0, 0, 0))
    title_text_rect = title_text.get_rect()
    title_text_rect.center = (w // 2, h // 4)

    play_button = GraphicalControls.Button('Play')
    play_button.surface = surface
    play_button.font = text_fonts[0]
    play_button.rim_color = pygame.Color('MEDIUMSPRINGGREEN')
    play_button.pressed_color = pygame.Color("PALEGREEN")

    quit_button = GraphicalControls.Button('Quit Game')
    quit_button.surface = surface
    quit_button.font = text_fonts[0]
    quit_button.rim_color = pygame.Color("RED")
    quit_button.pressed_color = pygame.Color("FIREBRICK")

    play_button_size = (w // 6, h // 10)
    quit_button_size = (w // 6, h // 14)
    play_button.Rect = pygame.Rect((w // 2 - play_button_size[0] // 2, int(h // 2) - play_button_size[1] // 2),
                                   play_button_size)
    play_button.subscribe_on_click(on_play_button_clicked)
    play_button.subscribe_on_mouse_over(play_mouse_over_sound)

    quit_button.Rect = pygame.Rect((w // 2 - quit_button_size[0] // 2, int(h // 1.5) + quit_button_size[1] // 2),
                                   quit_button_size)
    quit_button.subscribe_on_click(quit_game)
    quit_button.subscribe_on_mouse_over(play_mouse_over_sound)

    while refresh:
        pygame.event.pump()

        surface.fill((255, 255, 255))

        play_button.refresh()
        quit_button.refresh()

        surface.blit(title_text, title_text_rect)

        pygame.display.flip()
        clock.tick(60)


def play_mouse_over_sound():
    audio_manager.play_ui_sound("mouse_over_button_audio")


def on_play_button_clicked():
    global start_game_callback
    global refresh
    audio_manager.play_ui_sound("button_clicked_audio")
    refresh = False
    start_game_callback()


def quit_game():
    audio_manager.play_ui_sound("button_clicked_audio")
    pygame.quit()
    sys.exit(0)
