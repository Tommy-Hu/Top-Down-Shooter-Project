from random import randint

from main_game import pause_menu, death_scene
from entities.player import Player
from entities.enemy import Enemy
from entities.input import input_package
from main_game.coordinate_system.coordinate import Coordinate
from main_game.entities.projectile import Projectile
from main_game.entities.spawner import Spawner
from main_game.entities.weapon import Weapon
from main_game.particle_system import particles_manager
from main_game.ui_system.bars import HealthBar
from main_game.ui_system.statistics import Statistics

run_game = True
paused = False
clock = None
renderer = None
pygame = None
sprites = {}
audio_manager = None
menu_callback = None
restart_callback = None
bg = None
fonts = []
statistics = None


def stop_game():
    global run_game
    run_game = False
    audio_manager.fade_out_music()


def continue_game():
    global paused
    paused = False
    audio_manager.play_music('game_music')


def back_to_menu():
    global run_game
    global paused
    global menu_callback

    paused = False
    run_game = False
    menu_callback()


def player_die_callback():
    global run_game
    global menu_callback
    run_game = False
    death_scene.load(restart_callback, menu_callback, renderer, clock, fonts[1], fonts[0], statistics.enemies_killed)


def clear():
    global run_game
    global paused
    global clock
    global renderer
    global pygame
    global sprites
    global audio_manager
    global menu_callback

    run_game = True
    paused = False
    clock = None
    renderer = None
    pygame = None
    sprites = {}
    audio_manager = None
    menu_callback = None
    particles_manager.clear()


def loop(walls, grid, paths_mapper):
    global paused
    global sprites
    global statistics

    projectiles = []

    def add_projectile(p):
        projectiles.append(p)

    def destroy_projectile(p):
        try:
            projectiles.remove(p)
        except ValueError:
            pass

    weapons = {
        "Alien Launcher": Weapon(sprites["Alien Launcher"],
                                 Projectile(sprites["Alien Ammo"], sprites["Alien Ammo Burst"], (0, 0), (0, 0), 2000,
                                            10, True, 10, renderer,
                                            destroy_projectile, audio_manager, sprite_scale_multiplier=3,
                                            burst_scale_multiplier=3),
                                 0.2, add_projectile, renderer, audio_manager, sound_names=("shoot_1", "shoot_2")),
        "Durian": Weapon(sprites["Durian"],
                         Projectile(sprites["Durian"], sprites["Durian"], (0, 0), (0, 0), 1000,
                                    45, True, 10, renderer,
                                    destroy_projectile, audio_manager, sprite_scale_multiplier=6,
                                    burst_scale_multiplier=3),
                         0.2, add_projectile, renderer, audio_manager, sound_names=("shoot_4",)),
    }

    player = Player(sprites["Player"], sprites["Entity Shadow"], None, pygame.Rect(-50, -50, 100, 100), renderer, 425.0,
                    weapons["Durian"].duplicate(True), 200, player_die_callback)

    paths_mapper.player = player
    paths_mapper.start_thread()

    enemy_prefabs = {
        "Slimy": Enemy(sprites["Slimy Enemy"], sprites["Entity Shadow"], None, pygame.Rect(0, 0, 100, 100), renderer,
                       325.0, weapons["Alien Launcher"].duplicate(False), 100, grid, paths_mapper, player),

        "Yummy": Enemy(sprites["Yummy Enemy 1"], sprites["Entity Shadow"], sprites["Yummy Enemy 2"],
                       pygame.Rect(0, 0, 100, 100), renderer, 400.0, weapons["Alien Launcher"].duplicate(False), 100,
                       grid, paths_mapper, player),

        "Angry": Enemy(sprites["Angry Enemy 1"], sprites["Entity Shadow"], sprites["Angry Enemy 2"],
                       pygame.Rect(0, 0, 100, 100), renderer, 450.0, weapons["Durian"].duplicate(False), 100, grid,
                       paths_mapper, player),

        "Squishy": Enemy(sprites["Squishy Enemy"], sprites["Entity Shadow"], None, pygame.Rect(0, 0, 100, 100),
                         renderer, 300.0, weapons["Alien Launcher"].duplicate(False), 100, grid, paths_mapper, player),
    }

    enemies = [
        enemy_prefabs["Slimy"].duplicate_as_new(-1000, -1000),
        enemy_prefabs["Yummy"].duplicate_as_new(1000, -1000),
    ]

    spawners = [
        Spawner(sprites["Enemy Spawner"], (1000, 1000), (100, 100), renderer, list(enemy_prefabs.values()), 15, 3, 300,
                enemies.append),
        Spawner(sprites["Enemy Spawner"], (-1000, 1000), (100, 100), renderer, list(enemy_prefabs.values()), 15, 3, 300,
                enemies.append),
        Spawner(sprites["Enemy Spawner"], (-1000, -1000), (100, 100), renderer, list(enemy_prefabs.values()), 15, 3,
                300,
                enemies.append),
        Spawner(sprites["Enemy Spawner"], (1000, -1000), (100, 100), renderer, list(enemy_prefabs.values()), 15, 3, 300,
                enemies.append),
    ]

    health_bar = HealthBar((100, 100), sprites["Heart"], sprites["Empty Heart"], 50, player.max_health, renderer,
                           health_per_heart=20)

    mob_cap = 10
    statistics = Statistics(renderer, fonts[0])

    def kill_enemy(enemy):
        enemies.remove(enemy)
        statistics.enemies_killed += 1

    audio_manager.play_music('game_music')
    while True:
        global run_game

        if not run_game:
            break

        delta_time = clock.tick(120) / 1000.0
        print clock.get_fps()
        x, y = 0, 0

        # Initialize Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        audio_manager.fade_out_music()
                    else:
                        audio_manager.play_music('game_music')
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

        # update pause menu
        if paused:
            renderer.surface.fill((200, 200, 200))
            pause_menu.refresh_buttons(paused)
            continue

        # initialize environment
        renderer.clear_canvas()

        if bg is not None:
            renderer.add_to_canvas(bg, (-5000, -5000))

        package = input_package(float(x), float(y), keys, pygame.mouse.get_pressed(),
                                Coordinate.convert_to_global(pygame.mouse.get_pos(), player.rect.center,
                                                             (renderer.half_w, renderer.half_h)))

        player.update_with_input(package, delta_time)  # This needs to be the first in order to calculate world coord.
        renderer.set_center_point_on_screen_in_world_coord(player.rect.center)

        update_spawners(spawners, delta_time, len(enemies), mob_cap)
        update_walls(walls, player)
        update_enemies(enemies, player, delta_time, kill_enemy)

        player.draw_self(package, delta_time)
        update_projectiles(projectiles, walls, enemies, player, delta_time)
        particles_manager.draw_particles(delta_time)
        # ^^^ These needs to be the last because otherwise the spawners would appear above the player

        # UI update
        health_bar.update(player.health, player.max_health)
        statistics.update()

        renderer.render()
    projectiles = []
    enemies = []
    del grid
    del paths_mapper


def create_bg(tile_sprite, normalized_size=100):
    tile_sprite = pygame.transform.scale(tile_sprite, (normalized_size, normalized_size))

    global bg
    bg = pygame.Surface((normalized_size * 100, normalized_size * 100))
    half = normalized_size * 100 // 2
    for y in range(-49, 49):
        for x in range(-49, 49):
            bg.blit(get_random_90_rot(tile_sprite), (y * normalized_size + half, x * normalized_size + half))


def get_random_90_rot(sprite):
    degrees = randint(0, 3) * 90
    return pygame.transform.rotate(sprite, degrees)


def start_game(_renderer, exit_callback, _clock, _pygame, _sprites, walls, grid, paths_mapper, _audio_manager,
               _menu_callback, _restart_callback, _fonts):
    clear()
    global renderer
    global clock
    global pygame
    global sprites
    global audio_manager
    global menu_callback
    global restart_callback
    global fonts

    fonts = _fonts
    restart_callback = _restart_callback
    menu_callback = _menu_callback
    audio_manager = _audio_manager
    sprites = _sprites
    pygame = _pygame
    clock = _clock
    renderer = _renderer
    pygame.event.pump()

    create_bg(_sprites['Tile'])

    pause_menu.surface = renderer.surface
    pause_menu.set_buttons(renderer.w, renderer.h, back_to_menu, continue_game)

    loop(walls, grid, paths_mapper)

    exit_callback()


def update_walls(walls, player):
    collide = False
    for wall in walls:
        wall.update_to_renderer()
        if wall.check_collision_rect(player.rect):
            collide = True

    if collide:
        player.rect.topleft = player.last_pos


def update_projectiles(projectiles, walls, enemies, player, delta_time):
    ch = list(enemies)
    ch.append(player)
    for p in projectiles:
        p.update(walls, ch, delta_time)


def update_enemies(enemies, player, delta_time, kill_callback):
    for enemy in enemies:
        enemy.update(delta_time, kill_callback)


def update_spawners(spawners, delta_time, current, mob_cap):
    for spawner in spawners:
        current = spawner.update(delta_time, current, mob_cap)
