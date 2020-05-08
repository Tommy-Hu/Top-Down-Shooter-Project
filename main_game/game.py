import pygame

from main_game import pause_menu
from main_game.entities.player import Player
from main_game.entities.enemy import Enemy
from main_game.entities.input import input_package
from main_game.entities.wall import Wall

run_game = True
paused = False
clock = None
renderer = None

sprites = {
    "Rect": pygame.image.load("Assets\\Sprites\\Rectangle.png")
}


def stop_game():
    global run_game
    run_game = False


def continue_game():
    global paused
    paused = False


def loop():
    global paused

    player = Player(sprites["Rect"], pygame.Rect(-50, -50, 100, 100), renderer, 5)

    while run_game:

        x, y = 0, 0

        # Initialize Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    pause_menu.refresh_buttons(paused)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            y -= 1
        if keys[pygame.K_s]:
            y += 1
        if keys[pygame.K_d]:
            x += 1
        if keys[pygame.K_a]:
            x -= 1

        if paused:
            renderer.surface.fill((200, 200, 200))
            pause_menu.refresh_buttons(paused)
            clock.tick(60)
            continue

        renderer.clear_canvas()
        renderer.set_center_point_on_screen_in_world_coord(player.rect.center)

        package = input_package(x, y, keys, pygame.mouse.get_pressed(), pygame.mouse.get_pos())
        player.update_with_input(package)

        player.draw_to_renderer()

        renderer.render()

        clock.tick(60)


def start_game(_renderer, exit_callback, _clock):
    global renderer
    global clock
    clock = _clock
    renderer = _renderer
    pygame.event.pump()

    pause_menu.surface = renderer.surface
    pause_menu.set_buttons(renderer.w, renderer.h, stop_game, continue_game)

    loop()

    exit_callback()
