import pygame

from ui_assets import GraphicalControls

surface = None
pause_quit_button = None
pause_continue_button = None


def set_buttons(w, h, stop_game_callback, continue_game_callback):
    button_size = (w // 7, h // 10)

    global pause_quit_button
    global pause_continue_button

    pause_quit_button = GraphicalControls.Button("Menu")
    pause_continue_button = GraphicalControls.Button("Continue")

    pause_quit_button.surface = surface
    pause_quit_button.Rect = pygame.Rect((w // 2 - button_size[0] // 2, int(h // 1.5) - button_size[1] // 2),
                                         button_size)
    pause_quit_button.subscribe_on_click(stop_game_callback)

    pause_continue_button.surface = surface
    pause_continue_button.Rect = pygame.Rect((w // 2 - button_size[0] // 2, h // 2 - button_size[1] // 2), button_size)
    pause_continue_button.subscribe_on_click(continue_game_callback)


def refresh_buttons(paused):
    if not paused:
        return

    global pause_quit_button
    global pause_continue_button

    pause_continue_button.refresh()
    pause_quit_button.refresh()

    pygame.display.flip()
