# Game development with pygame
# Giuseppe Bellisano
# from Zenva tutorial

import pygame

SCREEN_TITLE = 'Crossy RPG' 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
clock = pygame.time.Clock()
#font
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:

    TICK_RATE = 60

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE_COLOR)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))
        #self.game_screen.fill(self.image)

        pygame.display.set_caption(title)

    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharacter('player.png', 375, 700, 50, 50)
        enemy_0 = NonPlayerCharacter('enemy.png', 20, 600, 50, 50)
        enemy_0.SPEED *= level_speed
        enemy_1 = NonPlayerCharacter('enemy.png', 20, 400, 50, 50)
        enemy_1.SPEED *= level_speed
        enemy_2 = NonPlayerCharacter('enemy.png', 20, 200, 50, 50)
        enemy_2.SPEED *= level_speed
        enemies = [enemy_0, enemy_1, enemy_2]
        treasure = GameObject('treasure.png', 375, 50, 50, 50)

        while not is_game_over:
            # A loop to get all of the events occuring at any given time
            # Events are most often mouse movement, mouse and button clicks, or exit events
            for event in pygame.event.get():
                # If we have a quite type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # Move up if up key pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    # Move down if down key pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                print(event)

            # Redraw the screen to be a blank white window
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0, 0))

            # Update the player position
            player_character.move(direction, self.height)
            player_character.draw(self.game_screen)

            # Update the enemy position
            # enemy_0.move(self.width)
            # enemy_0.draw(self.game_screen)
            for i in enemies:
                i.move(self.width)
                i.draw(self.game_screen)

            # Update treasure position
            treasure.draw(self.game_screen)

            # Verify collision
            if player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('You Win! :)', True, BLACK_COLOR)
                self.game_screen.blit(text, (275,350))
                pygame.display.update()
                clock.tick(1)
                break
            else:
                for i in enemies:
                    if player_character.detect_collision(i):
                        is_game_over = True
                        did_win = False
                        text = font.render('You Lose! :(', True, BLACK_COLOR)
                        self.game_screen.blit(text, (275,350))
                        pygame.display.update()
                        clock.tick(1)
                        break

            # Update all game graphics
            pygame.display.update()

            # Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)

        # Restart game loop if we won
        # Break out of game loop and quit if we lose
        if did_win:
            self.run_game_loop(level_speed + 0.5)
        else:
            return

# Generic game object class to subclassed by other objects in the game
class GameObject:

    def __init__(self, image_path, x, y, width, height):

        # Scale image
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))

        # Position
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    # Draw the object into background
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

# Class to represent the character controlled by the player
class PlayerCharacter(GameObject):

    SPEED = 10

    def __init_(self, image_path, x, y, width, height):
        super().__init_(image_path, x, y, width, height)

    # Move function will move character up if direction > 0 and down if < 0
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED

        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40

    def detect_collision(self, other_body):

        # Collision y-axis
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        # Collision x-axis
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        return True

# Class to represent the enemies moving left to right and right to left
class NonPlayerCharacter(GameObject):

    SPEED = 10

    def __init_(self, image_path, x, y, width, height):
        super().__init_(image_path, x, y, width, height)

    # Move function will move character right once it hits the far left of the
    # screen and left once it hits the far right of the screen
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

# Start Game
pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

# quit program
pygame.quit()
quit()