import pygame


def splash(clock, surface, title_font, text_fonts):
    splash_sound = pygame.mixer.Sound('Assets\\Audios\\Music\\win.wav')
    splash_sound.set_volume(1)
    splash_sound.play()

    w, h = surface.get_size()

    surface.fill(pygame.Color(0, 0, 0))

    title_font.set_bold(False)
    text_fonts[0].set_bold(False)

    title_text = title_font.render('Shape Shooter', True, pygame.Color(0, 0, 0))
    title_text_rect = title_text.get_rect()

    author_text = text_fonts[0].render('By Tommy Hu', True, pygame.Color(0, 0, 0))
    author_text_rect = author_text.get_rect()

    title_text_rect.center = (w // 2, h // 4)
    author_text_rect.center = (int(w // 1.5), int(h // 1.5))

    for i in range(0, 127):
        pygame.event.pump()
        current_color = pygame.Color(i * 2, i * 2, i * 2)

        title_text = title_font.render('Shape Shooter', True, current_color)
        author_text = text_fonts[0].render('By Tommy Hu', True, current_color)

        surface.blit(title_text, title_text_rect)
        surface.blit(author_text, author_text_rect)

        pygame.display.flip()
        clock.tick(60)

    for i in range(0, 1):
        pygame.event.pump()
        clock.tick(1)

    for i in range(0, 127):
        pygame.event.pump()
        current_color = pygame.Color((127 - i) * 2, (127 - i) * 2, (127 - i) * 2)

        title_text = title_font.render('Shape Shooter', True, current_color)
        author_text = text_fonts[0].render('By Tommy Hu', True, current_color)

        surface.blit(title_text, title_text_rect)
        surface.blit(author_text, author_text_rect)

        pygame.display.flip()
        i += 2
        clock.tick(85)

    for i in range(0, 120):
        pygame.event.pump()

        surface.fill(pygame.Color(i * 2, i * 2, i * 2))

        current_color = pygame.Color((120 - i) * 2, (120 - i) * 2, (120 - i) * 2)
        title_text = title_font.render('Shape Shooter', True, current_color)
        surface.blit(title_text, title_text_rect)

        pygame.display.flip()
        clock.tick(60)

    surface.fill(pygame.Color(255, 255, 255))
    title_text = title_font.render('Shape Shooter', True, (0, 0, 0))
    surface.blit(title_text, title_text_rect)
    game_on_text = text_fonts[0].render('Game On!', True, (0, 0, 0))
    game_on_text_rect = game_on_text.get_rect()
    game_on_text_rect.center = (w // 2, int(h // 1.8))
    surface.blit(game_on_text, game_on_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(0, 0, 0))
    title_text = title_font.render('Shape Shooter', True, (255, 255, 255))
    surface.blit(title_text, title_text_rect)
    game_on_text = text_fonts[0].render('Game On!', True, (255, 255, 255))
    surface.blit(game_on_text, game_on_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(255, 255, 255))
    title_text = title_font.render('Shape Shooter', True, (0, 0, 0))
    surface.blit(title_text, title_text_rect)
    game_on_text = text_fonts[1].render('Game On!', True, (0, 0, 0))
    game_on_text_rect = game_on_text.get_rect()
    game_on_text_rect.center = (w // 2, int(h // 1.8))
    surface.blit(game_on_text, game_on_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(0, 0, 0))
    title_text = title_font.render('Shape Shooter', True, (255, 255, 255))
    surface.blit(title_text, title_text_rect)
    game_on_text = text_fonts[1].render('Game On!', True, (255, 255, 255))
    surface.blit(game_on_text, game_on_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(255, 255, 255))
    title_text = title_font.render('Shape Shooter', True, (0, 0, 0))
    surface.blit(title_text, title_text_rect)
    game_on_text = text_fonts[2].render('Game On!', True, (0, 0, 0))
    game_on_text_rect = game_on_text.get_rect()
    game_on_text_rect.center = (w // 2, int(h // 1.8))
    surface.blit(game_on_text, game_on_text_rect)
    pygame.display.flip()
    clock.tick(10)

    surface.fill(pygame.Color(0, 0, 0))
    title_text = title_font.render('Shape Shooter', True, (255, 255, 255))
    surface.blit(title_text, title_text_rect)
    game_on_text = text_fonts[2].render('Game On!', True, (255, 255, 255))
    surface.blit(game_on_text, game_on_text_rect)
    pygame.display.flip()
    clock.tick(1.5)
