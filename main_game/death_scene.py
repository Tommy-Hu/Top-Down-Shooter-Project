import pygame

from main_game.ui_assets.GraphicalControls import Button

run = True


def load(restart_callback, main_menu_callback, renderer, clock, big_font, small_font, enemies_killed):
    def restart():
        restart_callback()
        global run
        run = False

    def menu():
        main_menu_callback()
        global run
        run = False

    red_canvas = pygame.Surface(renderer.canvas.get_size())
    red_canvas.fill(pygame.Color('BLACK'))
    red_canvas.convert()
    red_canvas.set_alpha(5)
    for i in range(0, 120):
        pygame.event.pump()
        renderer.surface.blit(red_canvas, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    restart_button = Button("Restart")
    restart_button.surface = renderer.canvas
    restart_rect = pygame.Rect(0, 0, renderer.w // 8, renderer.h // 12)
    restart_rect.center = (renderer.half_w, renderer.h // 1.5)
    restart_button.size = pygame.Vector2(restart_rect.size)
    restart_button.position = pygame.Vector2(restart_rect.topleft)
    restart_button.subscribe_on_click(restart)
    restart_button.font_color = pygame.Color('DARKGREEN')
    restart_button.pressed_color = pygame.Color('DARKMAGENTA')
    restart_button.rim_color = pygame.Color('DARKSLATEBLUE')

    main_button = Button("Menu")
    main_button.surface = renderer.canvas
    main_rect = pygame.Rect(0, 0, renderer.w // 8, renderer.h // 12)
    main_rect.center = (renderer.half_w, renderer.h // 1.25)
    main_button.size = pygame.Vector2(main_rect.size)
    main_button.position = pygame.Vector2(main_rect.topleft)
    main_button.subscribe_on_click(menu)
    main_button.font_color = pygame.Color(220, 20, 60)
    main_button.pressed_color = pygame.Color('RED')
    main_button.rim_color = pygame.Color('FIREBRICK')

    while True:
        renderer.clear_canvas(pygame.Color('DARKRED'))

        renderer.draw_text_ui_center("YOU WERE SLAIN!", big_font,
                                     pygame.Color('BLACK'), (renderer.half_w, renderer.half_h // 4))
        renderer.draw_text_ui_center("YOU TRIED BUT NOT HARD ENOUGH! Enemies killed: " + str(enemies_killed),
                                     small_font, pygame.Color('BLACK'), (renderer.half_w, renderer.half_h // 1.25))
        restart_button.refresh()
        main_button.refresh()
        pygame.event.pump()

        renderer.render()
        global run
        if not run:
            break

        clock.tick(60)
