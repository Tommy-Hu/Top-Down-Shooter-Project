from main_game.entities.character import Character


class Player(Character):
    def __init__(self, sprite, rect, renderer, speed, weapon):
        Character.__init__(self, sprite, rect, renderer, speed, weapon)
        self.last_move_amount = (0, 0)

    def move(self, offset):
        Character.move(self, (self.rect.topleft[0] + offset[0], self.rect.topleft[1] + offset[1]))

    def update_with_input(self, input_pack):
        amount = (input_pack.move_X * self.speed, input_pack.move_Y * self.speed)
        self.move(amount)
        self.last_move_amount = amount
        self.draw_to_renderer()

        facing = input_pack.mouse_pos - self.rect.center

        self.weapon.update(self.rect, facing, input_pack.mouse_buttons[0])
