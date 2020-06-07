import pygame


def splash(clock, surface, title_font, text_fonts, audio_manager, game_name):
    audio_manager.play_quick_FX("splash_sound")

    w, h = surface.get_size()

    surface.fill(pygame.Color(0, 0, 0))

    title_font.set_bold(False)
    text_fonts[0].set_bold(False)

    title_text = title_font.render(game_name, True, pygame.Color("DEEPSKYBLUE"))
    title_text_rect = title_text.get_rect()

    author_text = text_fonts[0].render('By Tommy Hu', True, pygame.Color(0, 0, 0))
    author_text_rect = author_text.get_rect()

    title_text_rect.center = (w // 2, h // 4)
    author_text_rect.center = (int(w // 1.5), int(h // 1.5))

    for i in range(0, 127):
        pygame.event.pump()
        current_color = pygame.Color(i * 2, i * 2, 255)

        title_text = title_font.render(game_name, True, current_color)
        author_text = text_fonts[0].render('By Tommy Hu', True, current_color)

        surface.blit(title_text, title_text_rect)
        surface.blit(author_text, author_text_rect)

        pygame.display.flip()
        clock.tick(60)

    for i in range(0, 1):
        pygame.event.pump()
        clock.tick(1)

    for i in range(0, 75):
        pygame.event.pump()
        current_color = pygame.Color((75 - i) * 3, 255, (75 - i) * 3)

        title_text = title_font.render(game_name, True, current_color)
        author_text = text_fonts[0].render('By Tommy Hu', True, current_color)

        surface.blit(title_text, title_text_rect)
        surface.blit(author_text, author_text_rect)

        pygame.display.flip()
        i += 2
        clock.tick(85)

    for i in range(0, 120):
        pygame.event.pump()

        surface.fill(pygame.Color(i * 2, 0, 0))

        current_color = pygame.Color(0, (120 - i) * 2, 0)
        title_text = title_font.render(game_name, True, current_color)
        surface.blit(title_text, title_text_rect)

        pygame.display.flip()
        clock.tick(60)

    audio_manager.play_quick_FX('thunder')

    surface.fill(pygame.Color(133, 9, 9))
    title_text = title_font.render(game_name, True, (84, 0, 0))
    surface.blit(title_text, title_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(0, 0, 0))
    title_text = title_font.render(game_name, True, (230, 32, 32))
    surface.blit(title_text, title_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(255, 255, 255))
    title_text = title_font.render(game_name, True, (84, 0, 0))
    surface.blit(title_text, title_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(0, 0, 0))
    title_text = title_font.render(game_name, True, (255, 0, 0))
    surface.blit(title_text, title_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(133, 9, 9))
    title_text = title_font.render(game_name, True, (84, 0, 0))
    surface.blit(title_text, title_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(0, 0, 0))
    title_text = title_font.render(game_name, True, (255, 255, 255))
    surface.blit(title_text, title_text_rect)
    pygame.display.flip()
    pygame.event.pump()
    clock.tick(0.5)
