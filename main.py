#!/usr/bin/env python3

import pygame as pg

BLOCK_SIZE = 20
WIN_SIZE = 500


class Block():
    def __init__(self, colour, start_params, pos):
        self.colour = colour
        self.start = start_params
        self.x = pos[0]
        self.y = pos[1]
        self.direction = [0, -BLOCK_SIZE]

    def make_block(self):
        # Create a surface to contain a square
        square = pg.Surface((BLOCK_SIZE, BLOCK_SIZE), pg.SRCALPHA)
        # Draw a square onto the "square" surface
        pg.draw.rect(square, self.colour, self.start)

        return square

    def update_pos(self):
        self.x += self.direction[0]
        self.y += self.direction[1]

    def change_direction(self, new_dir):
        if new_dir == 'u':
            self.direction = [0, -BLOCK_SIZE]
        elif new_dir == 'd':
            self.direction = [0, BLOCK_SIZE]
        elif new_dir == 'l':
            self.direction = [-BLOCK_SIZE, 0]
        elif new_dir == 'r':
            self.direction = [BLOCK_SIZE, 0]

    def check_collision(self):
        if self.x in (0, WIN_SIZE) or self.y in (0, WIN_SIZE):
            return True

        return False


def check_keypress(input_event, block_object):
    if input_event.type == pg.QUIT:
        return True
    elif input_event.type == pg.KEYDOWN:
        if input_event.key == pg.K_ESCAPE:
            return True
        elif input_event.key == pg.K_UP:
            block_object.change_direction('u')
        elif input_event.key == pg.K_DOWN:
            block_object.change_direction('d')
        elif input_event.key == pg.K_LEFT:
            block_object.change_direction('l')
        elif input_event.key == pg.K_RIGHT:
            block_object.change_direction('r')

    return False


def main():
    # Initialise PyGame
    pg.init()

    clock = pg.time.Clock()

    # Define window parameters
    size = (WIN_SIZE, WIN_SIZE) # (width, height)
    black = (0, 0, 0)
    blue = (0, 0, 255)

    # Define temporary parameters for rectangle, will eventually make a class
    start_coord = (WIN_SIZE / 2) - (BLOCK_SIZE / 2)
    # start_pos_and_size = (0, 0, BLOCK_SIZE, BLOCK_SIZE)

    # Create window
    screen = pg.display.set_mode(size)

    block = Block(blue, (0, 0, BLOCK_SIZE, BLOCK_SIZE), [start_coord, start_coord])
    square = block.make_block()



    game_over = False
    # Game loop
    while game_over == False:
        clock.tick(10)
        for event in pg.event.get():
            game_over = check_keypress(event, block)

        game_over = block.check_collision()
        block.update_pos()

        # Clear the screen before the next frame
        screen.fill(black)
        # Draw rectangle to screen
        screen.blit(square, [block.x, block.y])
        # Swap buffers
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()


# TODO:
# Extend snake body