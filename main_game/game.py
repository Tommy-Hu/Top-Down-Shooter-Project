from random import randint, choice

import pause_menu, death_scene
from coins_system import coins_manager
from entities.characters.player import Player
from entities.characters.enemy import Enemy, Boss
from entities.input import input_package
from coordinate_system.coordinate import Coordinate
from entities.laser import Laser
from entities.pickups.coin import Coin
from entities.pickups.health_container import HealthContainer
from entities.projectile import Projectile
from entities.characters.spawner import Spawner
from entities.weapon import Weapon
from particle_system import particles_manager
from ui_system.bars import HealthBar, BossBar
from ui_system.statistics import Statistics

# Parameters to control the game's flow
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


# Below are callback methods that are invoked on other threads and other files. Passed as delegates
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
    coins_manager.write_to_file()

    global run_game
    global paused

    paused = False
    run_game = False


def player_die_callback():
    coins_manager.write_to_file()

    global run_game
    global menu_callback
    run_game = False
    stop_game()
    global load_death_next
    load_death_next = True


# Above are callback methods


# Release the memory used. This is called when the game ends.
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


# Main loop of the game. Called from the (main.py) script.
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

    # A dictionary of weapons, as prefabs. Later in the game, they are instantiated to create new instances of
    # themselves.
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

    # The player. Instantiated with Alien Launcher as a starting weapon. All other parameters are just for info
    # transfer.
    player = Player(sprites["Player"], sprites["Entity Shadow"], None, pygame.Rect(-50, -50, 100, 100), renderer, 425.0,
                    weapons["Alien Launcher"].duplicate(True), 400, player_die_callback, audio_manager)

    # Initialize paths mapper. Paths mapper calculates a path using A* algorithm.
    paths_mapper.player = player
    paths_mapper.start_thread()

    # Initialize death audio.
    normal_death_audios = ("enemy_death_1", "enemy_death_2")

    # Create enemy prefabs. Later spawn them in (or clone them) with spawners.
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

    # Creates a boss prefab dictionary. Currently, the only boss is called "Crimson".
    boss_prefabs = {
        "Crimson": Boss((sprites["Crimson 1"], sprites["Crimson 2"], sprites["Crimson 3"]), 400,
                        sprites["Entity Shadow"], sprites["Crimson 1"], pygame.Rect(0, 0, 400, 400), renderer, 0,
                        weapons["Magic Mirror"].duplicate(False), 1555, grid, paths_mapper, player, finish_boss_fight)
    }

    # A list of pickups such as weapons and hearts. Nothing is there when the game starts, so initialize it to an empty
    # List.
    pickups = [
    ]

    # A callback that removes a coin from the pickups list. Also add 1 to the total coins count.
    def remove_coin(coin):
        audio_manager.play_pickup_sound("coin_pickup")
        coins_manager.coins_count += 1
        pickups.remove(coin)

    # Prefab of a coin object. Later clone it when enemies die.
    coin_prefab = Coin((0, 0), (
        sprites["Coin 1"], sprites["Coin 2"], sprites["Coin 3"], sprites["Coin 4"]), 64, renderer, remove_coin)

    # A list of current alive enemies. Looping through them and updating them to make them move and render.
    enemies = [
        enemy_prefabs["Slimy"].duplicate_as_new(-1000, -1000),
        enemy_prefabs["Yummy"].duplicate_as_new(1000, -1000),
    ]

    # Smoke sprite has alpha, so convert it.
    sprites["Smoke 1"] = sprites["Smoke 1"].convert()

    # The four spawners on the ground. They only spawn enemies when there are less than mob_cap enemies in the arena.
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

    # Destroys a pickup
    def destroy_pickup(pickup):
        pickups.remove(pickup)

    # UI prefabs>>
    health_bar = HealthBar((100, 75), sprites["Heart"], sprites["Empty Heart"], 50, player.max_health, renderer,
                           health_per_heart=20)
    boss_bar = BossBar((renderer.half_w, renderer.h - 300), sprites["Boss Bar Sides"].convert_alpha(),
                       sprites["Boss Bar"].convert_alpha(), sprites["Boss Bar Part"].convert_alpha(), renderer.half_w,
                       150, 50, 100, renderer)
    # <<UI prefabs

    # Health container prefab(as a pickup)
    health_container = HealthContainer(sprites["Heart"], (0, 0), 50, 25, renderer, destroy_pickup, "health_pickup",
                                       audio_manager)

    # As the name suggests, it is the current boss.
    current_boss = None
    # Mob_cap is the maximum number of mobs that can be on the arena.
    mob_cap = 10
    # Initialize statistics class. Statistics class contains the player's statistics such as enemy kill count
    statistics = Statistics(renderer, fonts[0])

    # A callback that kills an enemy.
    def kill_enemy(enemy):
        health_count = randint(0, enemy.health_drop_amount_max)
        for i in range(0, health_count):
            pickups.append(health_container.duplicate(enemy.rect.center))
        coins_count = randint(0, enemy.coin_drop_amount_max)
        for i in range(0, coins_count):
            pickups.append(coin_prefab.duplicate((enemy.rect.center[0] + randint(-40, 40),
                                                  enemy.rect.center[1] + randint(-40, 40))))
        enemies.remove(enemy)
        statistics.enemies_killed += 1
        sound = enemy.get_random_death_audio()
        if sound is not None:
            audio_manager.play_death_sound(sound)

    # Play game music with my own audio manager class.
    audio_manager.play_music('game_music')
    while True:
        global run_game
        global is_boss_fight

        if not run_game:
            break

        # FPS
        delta_time = clock.tick(120) / 1000.0
        x, y = 0, 0

        # Initialize Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    # Fade out music when paused
                    if paused:
                        audio_manager.fade_out_music()
                    else:
                        audio_manager.play_music('game_music')
                    pause_menu.refresh_buttons(paused)

        # Grab the input
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

        # Render the ground (the purple grass)
        if bg is not None:
            renderer.add_to_canvas(bg, (-5000, -5000))

        # Creates an input package(my own class) instance that is passed to multiple objects.
        package = input_package(float(x), float(y), keys, pygame.mouse.get_pressed(),
                                Coordinate.convert_to_global(pygame.mouse.get_pos(), player.rect.center,
                                                             (renderer.half_w, renderer.half_h)))

        # The warning sound simulator when health is below a quarter
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

        # Updates the player's stats with input package.
        player.update_with_input(package, delta_time)  # This needs to be the first in order to calculate world coord.

        # Sets the conversion factor in the world coord.
        # !!!!!!!!!!!!!THIS IS EXTREMELY IMPORTANT AS EVERYTHING IS BASED ON MY OWN WORLD COORDINATE SYSTEM!
        # NOT THE WINDOWED PIXEL COORD SYSTEM!!!!!
        renderer.set_center_point_on_screen_in_world_coord(player.rect.center)

        # Updates all the walls
        update_walls(walls, player)
        if not is_boss_fight and statistics.enemies_killed % 20 == 0 and statistics.enemies_killed > 19:
            del enemies[:]  # Release memory and delete all enemies.
            current_boss = boss_prefabs["Crimson"].duplicate_as_new(0, 0)
            enemies.append(current_boss)
            update_spawners(spawners, delta_time, len(enemies), mob_cap, False)
            is_boss_fight = True
        elif not is_boss_fight:
            current_boss = None
            update_spawners(spawners, delta_time, len(enemies), mob_cap, True)

        # Updates all enemies
        update_enemies(enemies, player, delta_time, kill_enemy, pickups)

        # Renders player
        player.draw_self(package, delta_time)
        # Updates all projectiles
        update_projectiles(projectiles, walls, enemies, player, delta_time)
        # Update all pickups
        update_pickups(pickups, player, delta_time)
        # Renders all particles
        particles_manager.draw_particles(delta_time)
        # ^^^ These needs to be the last because otherwise the spawners would appear above the player

        # UI update
        health_bar.update(player.health, player.max_health)
        if is_boss_fight and current_boss is not None:
            boss_bar.maximum = current_boss.max_health
            boss_bar.update(current_boss.health)
        # Updates the statistics
        statistics.update()
        # Renders coin count
        renderer.draw_text_ui_topright("Coins: " + str(coins_manager.coins_count), fonts[0], pygame.Color("WHITE"),
                                       (renderer.w - 30, 30))
        # MOST IMPORTANT LINE OF ALL<<<<<RENDERS EVERYTHING ON THE WINDOW. WITHOUT THIS LINE, THE GAME RUNS WITHOUT GFX.
        renderer.render()

    # After game exits, clean up the memory, otherwise running the game again and again may result in memory overflow.
    projectiles = []
    enemies = []
    paths_mapper.stop_threads()
    del grid
    del paths_mapper
    # If player died, load death scene, else, load menu
    if load_death_next:
        death_scene.load(restart_callback, menu_callback, renderer, clock, fonts[1], fonts[0],
                         statistics.enemies_killed)
    else:
        menu_callback()


# Creates a new bg surface object. This is the purple grass stuff(or the ground if you may).
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


# Some math to rotate one purple grass tile randomly so that it doesn't look repeated. Learned from >>Minecraft<<.
def get_random_90_rot(sprite):
    degrees = randint(0, 3) * 90
    return pygame.transform.rotate(sprite, degrees)


# Starts the game
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
    # Pumping the event system so that the game window is not "Not Responding". Learned from the pygame wiki.
    pygame.event.pump()

    create_bg(_sprites['Tile 1'], _sprites['Tile 2'])

    pause_menu.surface = renderer.surface
    pause_menu.set_buttons(renderer.w, renderer.h, back_to_menu, continue_game)

    # Starts the loop method above
    loop(walls, grid, paths_mapper)

    exit_callback()


# Just updates the walls
def update_walls(walls, player):
    collide = False
    for wall in walls:
        wall.update_to_renderer()
        if wall.check_collision_rect(player.rect):
            collide = True

    if collide:
        player.rect.topleft = player.last_pos


# Just updates the projectiles
def update_projectiles(projectiles, walls, enemies, player, delta_time):
    for p in projectiles:
        p.update(walls, enemies, player, delta_time)


# Just updates the enemies
def update_enemies(enemies, player, delta_time, kill_callback, pickups):
    enemiesToKill = []
    for enemy in enemies:
        enemy.update(delta_time, kill_callback, pickups)
        if abs(enemy.rect.center[0] - player.rect.center[0]) > 2000 and abs(
                enemy.rect.center[1] - player.rect.center[1] > 2000) and not is_boss_fight:
            enemiesToKill.append(enemy)

    for enemy in enemiesToKill:
        if enemy in enemies:
            enemies.remove(enemy)


# Just updates the spawners
def update_spawners(spawners, delta_time, current, mob_cap, spawn):
    for spawner in spawners:
        current = spawner.update(delta_time, current, mob_cap, spawn)


# Just updates all the pickups
def update_pickups(pickups, player, delta_time):
    for pickup in pickups:
        pickup.update(player, delta_time)
