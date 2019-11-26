
class GameCharacter:

    speed = 5

    def __init__(self, name, width, height, x_pos, y_pos):
        self.name = name
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move(self, by_x_amount, by_y_amount):
        self.x_pos += by_x_amount
        self.y_pos += by_y_amount

# Player subclass

class PlayerCharacter(GameCharacter):

    speed = 10

    def __init__(self, x_pos, y_pos):
        super().__init__('P1', 100, 100, x_pos, y_pos)

    def move(self, by_y_amount):
        super().move(0, by_y_amount)

player_character = PlayerCharacter(500, 500)
player_character.move(122)
print(player_character.y_pos)