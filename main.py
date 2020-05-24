#!/usr/bin/env python3

import pygame as pg

BLOCK_SIZE = 20
WIN_SIZE = 500


class Head():
    blue = (0, 0, 255)
    start_params = (0, 0, BLOCK_SIZE, BLOCK_SIZE)
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.last_x = self.x
        self.last_y = self.y
        self.direction = [0, -BLOCK_SIZE]
        self.square = None

    def make_block(self):
        # Create a surface to contain a square
        self.square = pg.Surface((BLOCK_SIZE, BLOCK_SIZE), pg.SRCALPHA)
        # Draw a square onto the "square" surface
        pg.draw.rect(self.square, self.blue, self.start_params)

    def update_pos(self):
        self.last_x = self.x
        self.last_y = self.y
        self.x += self.direction[0]
        self.y += self.direction[1]

    def change_direction(self, new_dir):
        if new_dir == 'u' and self.direction != [0, BLOCK_SIZE]:
            self.direction = [0, -BLOCK_SIZE]
        elif new_dir == 'd' and self.direction != [0, -BLOCK_SIZE]:
            self.direction = [0, BLOCK_SIZE]
        elif new_dir == 'l' and self.direction != [BLOCK_SIZE, 0]:
            self.direction = [-BLOCK_SIZE, 0]
        elif new_dir == 'r' and self.direction != [-BLOCK_SIZE, 0]:
            self.direction = [BLOCK_SIZE, 0]

    def check_collision(self):
        if self.x in (0, WIN_SIZE) or self.y in (0, WIN_SIZE):
            return True

        return False

    def get_pos(self):
        return (self.last_x, self.last_y)


class Block(Head):
    def __init__(self, next_block):
        self.next = next_block
        pos = next_block.get_pos()
        self.x = pos[0]
        self.y = pos[1]
        self.last_x = self.x
        self.last_y = self.y
        self.ready = 0

    def update_pos(self):
        self.last_x = self.x
        self.last_y = self.y
        next_pos = self.next.get_pos()
        self.x = next_pos[0]
        self.y = next_pos[1]


def add_block(snake_arr):
    snake_arr.append(Block(snake_arr[-1]))
    snake_arr[-1].make_block()

    return snake_arr


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

    # Define temporary parameters for rectangle, will eventually make a class
    start_coord = (WIN_SIZE / 2) - (BLOCK_SIZE / 2)

    # Create window
    screen = pg.display.set_mode(size)

    head = Head([start_coord, start_coord])
    head.make_block()

    bl2 = Block(head)
    bl2.make_block()

    bl3 = Block(bl2)
    bl3.make_block()

    snake = []
    snake.append(head)
    snake.append(bl2)
    snake.append(bl3)

    game_over = False
    # Game loop
    while game_over == False:
        clock.tick(10)
        for event in pg.event.get():
            game_over = check_keypress(event, head)
        if game_over == True:
            continue

        game_over = head.check_collision()

        for s in snake:
            s.update_pos()

        # Clear the screen before the next frame
        screen.fill(black)
        # Draw block to screen
        for s in snake:
            screen.blit(s.square, [s.x, s.y])
        # Swap buffers
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()


# TODO:
# Extend snake body