from main_game.entities.character import Character


class Player(Character):
    def __init__(self, sprite, rect, renderer, speed):
        Character.__init__(self, sprite, rect, renderer, speed)

    def move(self, offset):
        Character.move(self, (self.rect.topleft[0] + offset[0], self.rect.topleft[1] + offset[1]))

    def update_with_input(self, input_pack):
        self.move((input_pack.move_X * self.speed, input_pack.move_Y * self.speed))
