from pygame import Vector2


# LOTS OF MATH and basically converts screen coords to my own world coords. This is done so that the game
# "follows" the player.
class Coordinate:

    @staticmethod
    def convert_to_global(screen_coordinate, current_center_point_in_global, center_point_in_screen):
        screen_coordinate = Vector2(screen_coordinate)
        current_center_point_in_global = Vector2(current_center_point_in_global)
        center_point_in_screen = Vector2(center_point_in_screen)
        return Vector2(
            screen_coordinate.x - center_point_in_screen.x + current_center_point_in_global.x,
            screen_coordinate.y - center_point_in_screen.y + current_center_point_in_global.y)

    @staticmethod
    def convert_to_screen(global_coordinate, current_center_point_in_global, center_point_in_screen):
        global_coordinate = Vector2(global_coordinate)
        current_center_point_in_global = Vector2(current_center_point_in_global)
        center_point_in_screen = Vector2(center_point_in_screen)
        return Vector2(
            global_coordinate.x + center_point_in_screen.x - current_center_point_in_global.x,
            global_coordinate.y + center_point_in_screen.y - current_center_point_in_global.y)
