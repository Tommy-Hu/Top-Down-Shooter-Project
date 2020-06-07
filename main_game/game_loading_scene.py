import threading

import pygame

from coordinate_system.grid import Grid, PathsMapper

total = 0
LOCK = threading.Lock()
current = 0
images_result = {}
grid_result = None
paths_mapper_result = None

draw_text = ""


def load_images(images):
    global images_result
    images_result = {}

    def load_image(path):
        return pygame.image.load(path)

    for image in images:
        images_result[image] = load_image(images[image])
        update_progress()
        pygame.time.delay(10)


def load_walls(walls):
    wall_sprite = images_result["Wall"].convert_alpha()
    for wall in walls:
        wall.tile_sprite = wall_sprite
        wall.create_with_tiles(100)


def load_grid(walls, renderer):
    global grid_result
    global paths_mapper_result
    grid_result = None
    paths_mapper_result = None
    grid_result = Grid(walls, renderer, grid_density=100)
    update_progress()
    paths_mapper_result = PathsMapper(grid_result)
    update_progress()


def update_progress():
    with LOCK:
        global current
        current += 1


def update_text(t):
    global draw_text
    draw_text = t


def load(walls, images, renderer, change_text_callback):
    change_text_callback("Tidying up the grid...")
    load_grid(walls, renderer)
    change_text_callback("Painting visuals and sprites...")
    load_images(images)
    update_progress()
    change_text_callback("Loading Walls")
    load_walls(walls)
    update_progress()
    change_text_callback("Finalizing...")
    pygame.time.delay(1024)
    update_progress()


def clear():
    global total
    global LOCK
    global current
    global images_result
    global grid_result
    global paths_mapper_result
    global draw_text
    total = 0
    LOCK = threading.Lock()
    current = 0
    images_result = {}
    grid_result = None
    paths_mapper_result = None
    draw_text = ""


def start_loading(audio_manager, images, finished_loading_callback, renderer, loading_text_font, clock, walls):
    clear()
    audio_manager.play_music('loading_loop')

    global total
    total = len(images) + 5

    load_thread = threading.Thread(target=load, args=(walls, images, renderer, update_text))
    load_thread.daemon = True
    load_thread.start()

    draw_pos = (renderer.half_w, renderer.h // 1.5)
    last_factor = 0
    increase_factor = True

    while True:
        global current
        global draw_text
        pygame.event.pump()

        if increase_factor:
            last_factor += 0.005
            if last_factor >= 1:
                increase_factor = False
        else:
            last_factor -= 0.005
            if last_factor <= 0:
                increase_factor = True

        bg_color = lerp_color(pygame.Color("GOLD"), pygame.Color("DARKORCHID"), last_factor)
        text_color = lerp_color(pygame.Color("SEAGREEN"), pygame.Color("LIMEGREEN"), last_factor)

        renderer.clear_canvas(bg_color)

        renderer.draw_text_ui_center(draw_text + "\n" + str(current) + "/" + str(total), loading_text_font,
                                     text_color, draw_pos)

        renderer.render()
        clock.tick(60)
        if current >= total:
            break

    global images_result
    finished_loading_callback(images_result, grid_result, paths_mapper_result, walls)


def lerp_color(color, to_color, factor):
    r = [color.r, color.g, color.b]
    cur = [color.r, color.g, color.b]
    to = [to_color.r, to_color.g, to_color.b]
    for i in range(0, 3):
        r[i] = round(r[i] + factor * (to[i] - cur[i]))
    return pygame.Color(int(r[0]), int(r[1]), int(r[2]))
