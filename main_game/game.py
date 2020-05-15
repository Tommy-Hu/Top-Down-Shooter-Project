from main_game import pause_menu
from entities.player import Player
from entities.enemy import Enemy
from entities.input import input_package
from entities.wall import Wall
from main_game.coordinate_system.coordinate import Coordinate
from main_game.coordinate_system.grid import Grid, PathsMapper
from main_game.entities.projectile import Projectile
from main_game.entities.weapon import Weapon

run_game = True
paused = False
clock = None
renderer = None
pygame = None


def stop_game():
    global run_game
    run_game = False


def continue_game():
    global paused
    paused = False


def loop():
    global paused

    sprites = {
        "Circle": pygame.image.load("Assets\\Sprites\\Circle.png"),
        "Rect": pygame.image.load("Assets\\Sprites\\Rectangle.png"),
        "Onion": pygame.image.load("Assets\\Sprites\\Onion.png"),
        "Ammo 1": pygame.image.load("Assets\\Sprites\\Ammo 1.png"),
        "Enemy 1": pygame.image.load("Assets\\Sprites\\Enemy 1.png"),
        "Alien Launcher": pygame.image.load("Assets\\Sprites\\Alien Launcher.png")
    }

    projectiles = []

    def add_projectile(p):
        projectiles.append(p)

    def destroy_projectile(p):
        projectiles.remove(p)

    walls = [Wall(pygame.Rect(-100, -200, 300, 100), renderer),
             Wall(pygame.Rect(100, 200, 300, 100), renderer),
             Wall(pygame.Rect(-300, -500, 500, 200), renderer),
             Wall(pygame.Rect(600, -200, 400, 100), renderer),
             Wall(pygame.Rect(-500, -800, 300, 600), renderer)]

    grid = Grid(walls, renderer, grid_density=50)
    paths_mapper = PathsMapper(grid)

    weapons = {
        "Alien Launcher": Weapon(sprites["Alien Launcher"],
                                 Projectile(sprites["Ammo 1"], (0, 0), (0, 0), 15, True, 10, renderer,
                                            destroy_projectile),
                                 10, add_projectile, renderer)
    }
    enemies = [
        Enemy(sprites["Enemy 1"], pygame.Rect(-1000, -1000, 100, 100), renderer, 4, weapons["Alien Launcher"], grid),
        Enemy(sprites["Enemy 1"], pygame.Rect(1000, -1000, 100, 100), renderer, 4, weapons["Alien Launcher"], grid),
        Enemy(sprites["Enemy 1"], pygame.Rect(-1000, 1000, 100, 100), renderer, 4, weapons["Alien Launcher"], grid),
        Enemy(sprites["Enemy 1"], pygame.Rect(1000, 1000, 100, 100), renderer, 4, weapons["Alien Launcher"], grid),
        Enemy(sprites["Enemy 1"], pygame.Rect(-2000, -2000, 100, 100), renderer, 4, weapons["Alien Launcher"], grid),
        Enemy(sprites["Enemy 1"], pygame.Rect(2000, -2000, 100, 100), renderer, 4, weapons["Alien Launcher"], grid),
        Enemy(sprites["Enemy 1"], pygame.Rect(-2000, 2000, 100, 100), renderer, 4, weapons["Alien Launcher"], grid),
        Enemy(sprites["Enemy 1"], pygame.Rect(2000, 2000, 100, 100), renderer, 4, weapons["Alien Launcher"], grid)
    ]

    player = Player(sprites["Onion"], pygame.Rect(-50, -50, 100, 100), renderer, 5, weapons["Alien Launcher"])

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

        package = input_package(x, y, keys, pygame.mouse.get_pressed(),
                                Coordinate.convert_to_global(pygame.mouse.get_pos(), player.rect.center,
                                                             (renderer.half_w, renderer.half_h)))
        if paths_mapper.is_finished:
            paths_mapper.get_all_enemy_paths(enemies, player)

        player.update_with_input(package)
        update_walls(walls, player)
        update_projectiles(projectiles, walls)
        update_enemies(enemies, player)

        renderer.render()
        clock.tick(60)


def start_game(_renderer, exit_callback, _clock, _pygame):
    global renderer
    global clock
    global pygame

    pygame = _pygame
    clock = _clock
    renderer = _renderer
    pygame.event.pump()

    pause_menu.surface = renderer.surface
    pause_menu.set_buttons(renderer.w, renderer.h, stop_game, continue_game)

    loop()

    exit_callback()


def update_walls(walls, player):
    for wall in walls:
        wall.update_to_renderer()
        if wall.check_collision_rect(player.rect):
            player.move(-pygame.Vector2(player.last_move_amount))


def update_projectiles(projectiles, walls):
    for p in projectiles:
        p.update(walls)


def update_enemies(enemies, player):
    for enemy in enemies:
        enemy.update(player)
