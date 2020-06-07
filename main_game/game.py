from random import randint, choice

import pause_menu, death_scene
from entities.characters.player import Player
from entities.characters.enemy import Enemy, Boss
from entities.input import input_package
from coordinate_system.coordinate import Coordinate
from entities.laser import Laser
from entities.pickups.health_container import HealthContainer
from entities.projectile import Projectile
from entities.characters.spawner import Spawner
from entities.weapon import Weapon
from particle_system import particles_manager
from ui_system.bars import HealthBar, BossBar
from ui_system.statistics import Statistics

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
is_boss_fight = False
load_death_next = False


def finish_boss_fight():
    global is_boss_fight
    is_boss_fight = False


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

    paused = False
    run_game = False


def player_die_callback():
    global run_game
    global menu_callback
    run_game = False
    stop_game()
    global load_death_next
    load_death_next = True


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
    particles_manager.init(sprites, renderer)

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
                                            destroy_projectile, 'hit_1', audio_manager, sprite_scale_multiplier=3,
                                            burst_scale_multiplier=3),
                                 0.1, add_projectile, renderer, audio_manager, sound_names=("shoot_1", "shoot_2")),
        "Durian": Weapon(sprites["Durian"], Projectile(sprites["Durian"], sprites["Durian"], (0, 0), (0, 0), 1000,
                                                       45, True, 10, renderer,
                                                       destroy_projectile, 'spike', audio_manager,
                                                       sprite_scale_multiplier=6,
                                                       burst_scale_multiplier=3),
                         0.2, add_projectile, renderer, audio_manager, sound_names=("shoot_4",)),
        "Magic Mirror": Weapon(sprites["Mirror"],
                               Laser((0, 0), (0, 0), 1, 15, renderer, False, pygame.Color("LIGHTBLUE"), 20,
                                     destroy_projectile), 0.07, add_projectile, renderer, audio_manager)
    }

    player = Player(sprites["Player"], sprites["Entity Shadow"], None, pygame.Rect(-50, -50, 100, 100), renderer, 425.0,
                    weapons["Alien Launcher"].duplicate(True), 400, player_die_callback, audio_manager)

    paths_mapper.player = player
    paths_mapper.start_thread()

    normal_death_audios = ("enemy_death_1", "enemy_death_2")

    enemy_prefabs = {
        "Slimy": Enemy(sprites["Slimy Enemy"], sprites["Entity Shadow"], sprites["Slimy Enemy"],
                       pygame.Rect(0, 0, 100, 100), renderer, 325.0, weapons["Alien Launcher"].duplicate(False), 100,
                       grid, paths_mapper, player, death_audios=normal_death_audios),

        "Yummy": Enemy(sprites["Yummy Enemy 1"], sprites["Entity Shadow"], sprites["Yummy Enemy 2"],
                       pygame.Rect(0, 0, 100, 100), renderer, 400.0, weapons["Alien Launcher"].duplicate(False), 100,
                       grid, paths_mapper, player, death_audios=normal_death_audios),

        "Angry": Enemy(sprites["Angry Enemy 1"], sprites["Entity Shadow"], sprites["Angry Enemy 2"],
                       pygame.Rect(0, 0, 100, 100), renderer, 450.0, weapons["Durian"].duplicate(False), 100, grid,
                       paths_mapper, player, death_audios=normal_death_audios),

        "Squishy": Enemy(sprites["Squishy Enemy"], sprites["Entity Shadow"], sprites["Squishy Enemy"],
                         pygame.Rect(0, 0, 100, 100), renderer, 300.0, weapons["Magic Mirror"].duplicate(False), 100,
                         grid, paths_mapper, player, death_audios=normal_death_audios),
    }

    boss_prefabs = {
        "Crimson": Boss((sprites["Crimson 1"], sprites["Crimson 2"], sprites["Crimson 3"]), 400,
                        sprites["Entity Shadow"], sprites["Crimson 1"], pygame.Rect(0, 0, 400, 400), renderer, 0,
                        weapons["Magic Mirror"].duplicate(False), 1555, grid, paths_mapper, player, finish_boss_fight)
    }

    enemies = [
        enemy_prefabs["Slimy"].duplicate_as_new(-1000, -1000),
        enemy_prefabs["Yummy"].duplicate_as_new(1000, -1000),
    ]

    sprites["Smoke 1"] = sprites["Smoke 1"].convert()

    spawners = [
        Spawner(sprites["Enemy Spawner"], (1000, 1000), (100, 100), renderer, list(enemy_prefabs.values()), 15, 3, 300,
                enemies.append, sprites['Smoke 1'], particles_manager.register_particle),
        Spawner(sprites["Enemy Spawner"], (-1000, 1000), (100, 100), renderer, list(enemy_prefabs.values()), 15, 3, 300,
                enemies.append, sprites['Smoke 1'], particles_manager.register_particle),
        Spawner(sprites["Enemy Spawner"], (-1000, -1000), (100, 100), renderer, list(enemy_prefabs.values()), 15, 3,
                300,
                enemies.append, sprites['Smoke 1'], particles_manager.register_particle),
        Spawner(sprites["Enemy Spawner"], (1000, -1000), (100, 100), renderer, list(enemy_prefabs.values()), 15, 3, 300,
                enemies.append, sprites['Smoke 1'], particles_manager.register_particle),
    ]

    pickups = [

    ]

    def destroy_pickup(pickup):
        pickups.remove(pickup)

    health_bar = HealthBar((100, 75), sprites["Heart"], sprites["Empty Heart"], 50, player.max_health, renderer,
                           health_per_heart=20)
    boss_bar = BossBar((renderer.half_w, renderer.h - 300), sprites["Boss Bar Sides"].convert_alpha(),
                       sprites["Boss Bar"].convert_alpha(), sprites["Boss Bar Part"].convert_alpha(), renderer.half_w,
                       150, 50, 100, renderer)

    health_container = HealthContainer(sprites["Heart"], (0, 0), 50, 25, renderer, destroy_pickup, "health_pickup",
                                       audio_manager)

    current_boss = None
    mob_cap = 10
    statistics = Statistics(renderer, fonts[0])

    def kill_enemy(enemy):
        health_count = randint(0, enemy.health_drop_amount_max)
        for i in range(0, health_count):
            pickups.append(health_container.duplicate(enemy.rect.center))
        enemies.remove(enemy)
        statistics.enemies_killed += 1
        sound = enemy.get_random_death_audio()
        if sound is not None:
            audio_manager.play_death_sound(sound)

    audio_manager.play_music('game_music')
    while True:
        global run_game
        global is_boss_fight

        if not run_game:
            break

        delta_time = clock.tick(120) / 1000.0
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

        if player.health / float(player.max_health) < 0.25:
            renderer.heart_beats = True
            if renderer.heart_increase:
                renderer.heart_beat_progress += delta_time * 2
                if renderer.heart_beat_progress > 1:
                    renderer.heart_increase = False
                    renderer.heart_beat_progress = 1
            else:
                renderer.heart_beat_progress -= delta_time * 2
                if renderer.heart_beat_progress < 0:
                    renderer.heart_increase = True
                    renderer.heart_beat_progress = 0
                    audio_manager.play_warning_sound("warning")
        elif renderer.heart_beats:
            renderer.heart_beat_progress -= delta_time * 2
            if renderer.heart_beat_progress < 0:
                renderer.heart_increase = True
                renderer.heart_beat_progress = 0
                renderer.heart_beats = False

        player.update_with_input(package, delta_time)  # This needs to be the first in order to calculate world coord.
        renderer.set_center_point_on_screen_in_world_coord(player.rect.center)

        update_walls(walls, player)
        if not is_boss_fight and statistics.enemies_killed % 20 == 0 and statistics.enemies_killed > 19:
            del enemies[:]
            current_boss = boss_prefabs["Crimson"].duplicate_as_new(0, 0)
            enemies.append(current_boss)
            update_spawners(spawners, delta_time, len(enemies), mob_cap, False)
            is_boss_fight = True
        elif not is_boss_fight:
            current_boss = None
            update_spawners(spawners, delta_time, len(enemies), mob_cap, True)
        update_enemies(enemies, player, delta_time, kill_enemy, pickups)

        player.draw_self(package, delta_time)
        update_projectiles(projectiles, walls, enemies, player, delta_time)
        update_pickups(pickups, player, delta_time)
        particles_manager.draw_particles(delta_time)
        # ^^^ These needs to be the last because otherwise the spawners would appear above the player

        # UI update
        health_bar.update(player.health, player.max_health)
        if is_boss_fight and current_boss is not None:
            boss_bar.maximum = current_boss.max_health
            boss_bar.update(current_boss.health)
        statistics.update()

        renderer.render()
    projectiles = []
    enemies = []
    paths_mapper.stop_threads()
    del grid
    del paths_mapper
    if load_death_next:
        death_scene.load(restart_callback, menu_callback, renderer, clock, fonts[1], fonts[0],
                         statistics.enemies_killed)
    else:
        menu_callback()


def create_bg(tile_sprite_1, tile_sprite_2, normalized_size=100):
    tile_sprite_1 = pygame.transform.scale(tile_sprite_1, (normalized_size, normalized_size))
    tile_sprite_2 = pygame.transform.scale(tile_sprite_2, (normalized_size, normalized_size))

    def get_random_tile():
        return choice((tile_sprite_1, tile_sprite_2))

    global bg
    bg = pygame.Surface((normalized_size * 100, normalized_size * 100))
    half = normalized_size * 100 // 2
    for y in range(-49, 49):
        for x in range(-49, 49):
            bg.blit(get_random_90_rot(get_random_tile()), (y * normalized_size + half, x * normalized_size + half))


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

    create_bg(_sprites['Tile 1'], _sprites['Tile 2'])

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
    for p in projectiles:
        p.update(walls, enemies, player, delta_time)


def update_enemies(enemies, player, delta_time, kill_callback, pickups):
    for enemy in enemies:
        enemy.update(delta_time, kill_callback, pickups)


def update_spawners(spawners, delta_time, current, mob_cap, spawn):
    for spawner in spawners:
        current = spawner.update(delta_time, current, mob_cap, spawn)


def update_pickups(pickups, player, delta_time):
    for pickup in pickups:
        pickup.update(player, delta_time)
