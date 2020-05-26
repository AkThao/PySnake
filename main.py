#!/usr/bin/env python3

import pygame as pg
from random import randint

# Define window parameters
BLOCK_SIZE = 20  # Size of single block
WIN_SIZE = 500  # Width and height of window
UPDATE_FRAMES = 4  # How often to update snake position, controls game speed


class Head():
    blue = (0, 0, 255)  # Colour of snake
    start_params = (BLOCK_SIZE * 0.05, BLOCK_SIZE * 0.05,
                    BLOCK_SIZE * 0.9, BLOCK_SIZE * 0.9)

    def __init__(self, x, y):
        """Head of snake"""
        self.x, self.y = x, y
        self.last_x: int = self.x
        self.last_y: int = self.y
        self.direction: Tuple[int, int] = (0, -1)
        self.square: pg.Surface = None

    def make_block(self):
        """
        Create a surface to contain a square
        Draw a square Rect object onto said surface
        """
        self.square = pg.Surface((BLOCK_SIZE, BLOCK_SIZE), pg.SRCALPHA)
        # Draw a square onto the "square" surface
        pg.draw.rect(self.square, self.blue, self.start_params)

    def update_pos(self):
        """Last coords are used to update next block in the snake"""
        self.last_x = self.x
        self.last_y = self.y
        self.x += self.direction[0] * BLOCK_SIZE
        self.y += self.direction[1] * BLOCK_SIZE

    def change_direction(self, new_dir):
        """Change direction of snake without allowing it to go backwards"""
        # North/South
        if new_dir[1] != -self.direction[1]:
            self.direction = new_dir

        # East/West
        elif new_dir[0] != -self.direction[0]:
            self.direction = new_dir

    def check_collision(self, pos_list):
        """Check if snake collides with wall or itself"""
        if self.x in (0, WIN_SIZE) or self.y in (0, WIN_SIZE):
            return True

        if (self.x, self.y) in pos_list[1:]:
            return True

        return False

    def get_last_pos(self):
        return (self.last_x, self.last_y)

    def get_current_pos(self):
        return (self.x, self.y)


class Block(Head):
    def __init__(self, next_block):
        """Body of snake"""
        self.next = next_block
        self.x, self.y = next_block.get_last_pos()
        self.last_x: int = self.x
        self.last_y: int = self.y
        self.ready = 0

    def update_pos(self):
        """Use position of next block in snake to update current position"""
        self.last_x = self.x
        self.last_y = self.y
        self.x, self.y = self.next.get_last_pos()


def add_block(snake_arr):
    """Extend snake by adding a snake block to the snake array"""
    snake_arr.append(Block(snake_arr[-1]))
    snake_arr[-1].make_block()

    return snake_arr


def check_keypress(input_event, block_object):
    """
    Take input event and change direction if arrow key
    or quit game if esc key or other exit signal
    """
    if input_event.type == pg.QUIT:
        return True
    elif input_event.type == pg.KEYDOWN:
        if input_event.key == pg.K_ESCAPE:
            return True
        elif input_event.key == pg.K_UP:
            block_object.change_direction([0, -1])
        elif input_event.key == pg.K_DOWN:
            block_object.change_direction([0, 1])
        elif input_event.key == pg.K_LEFT:
            block_object.change_direction([-1, 0])
        elif input_event.key == pg.K_RIGHT:
            block_object.change_direction([1, 0])

    return False


class Food():
    def __init__(self):
        """Food block, created in the same way as a snake block"""
        self.exists = False
        self.x = None
        self.y = None
        self.square = None

    def add_food(self):
        """If no food present, create a new food block with random position"""
        if self.exists is False:
            # Create a surface to contain a square
            self.square = pg.Surface((BLOCK_SIZE, BLOCK_SIZE), pg.SRCALPHA)
            # Draw a square onto the "square" surface
            pg.draw.rect(self.square, (255, 0, 0),
                         (BLOCK_SIZE * 0.05, BLOCK_SIZE * 0.05,
                          BLOCK_SIZE * 0.9, BLOCK_SIZE * 0.9))

            self.x = randint(1, (WIN_SIZE - BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
            self.y = randint(1, (WIN_SIZE - BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE
            self.exists = True

    def check_if_eaten(self, snake_head):
        """If snake head is in food block, food is eaten"""
        snake_x, snake_y = snake_head.get_last_pos()
        if (self.x <= snake_x < self.x + BLOCK_SIZE) and (self.y <= snake_y < self.y + BLOCK_SIZE):
            self.exists = False
            return True

        return False


def main():
    # Initialise PyGame
    pg.init()

    clock = pg.time.Clock()

    size = (WIN_SIZE, WIN_SIZE)  # Size of window, (width, height)
    black = (0, 0, 0)  # Background colour of window

    # Place head of snake in centre of window
    start_coord = (WIN_SIZE / 2) - (BLOCK_SIZE / 2)

    # Create window
    screen = pg.display.set_mode(size)

    head = Head(start_coord, start_coord)
    head.make_block()

    # Make first three blocks of snake
    snake = []
    snake.append(head)
    snake = add_block(snake)
    snake = add_block(snake)

    ticker = 0
    game_over = False
    food = Food()
    # Game loop
    while game_over is False:
        # Run game at 30 FPS
        clock.tick(30)
        # Monitor events and check for keypresses
        for event in pg.event.get():
            game_over = check_keypress(event, head)
        if game_over is True:
            continue


        # Update snake position every 4 frames
        if ticker == UPDATE_FRAMES - 1:
            for s in snake:
                s.update_pos()
            snake_pos = [block.get_current_pos() for block in snake]
            game_over = head.check_collision(snake_pos)
            ticker = 0
        ticker += 1

        food.add_food()
        eaten = food.check_if_eaten(head)
        if eaten is True:
            snake = add_block(snake)

        # Clear the window before the next frame
        screen.fill(black)
        # Draw block to window
        screen.blit(food.square, [food.x, food.y])
        for s in snake:
            screen.blit(s.square, [s.x, s.y])
        # Swap buffers
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
