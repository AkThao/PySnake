#!/usr/bin/env python3

import pygame as pg


def main():
    # Initialise PyGame
    pg.init()

    # Define window parameters
    win_size = 500
    size = (win_size, win_size) # (width, height)
    black = (0, 0, 0)
    blue = (0, 0, 255)

    # Define temporary parameters for rectangle, will eventually make a class
    length = 20
    start_coord = (win_size / 2) - (length / 2)
    start_pos_and_size = (0, 0, length, length)

    # Create window
    screen = pg.display.set_mode(size)

    # Create a surface to contain a square
    square = pg.Surface((length, length), pg.SRCALPHA)
    # Draw a square onto the "square" surface
    pg.draw.rect(square, blue, start_pos_and_size)

    coords = (start_coord, start_coord)

    game_over = False
    # Game loop
    while game_over == False:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
                continue
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    game_over = True
                    continue

        # Clear the screen before the next frame
        screen.fill(black)
        # Draw rectangle to screen
        screen.blit(square, coords)
        # Swap buffers
        pg.display.flip()

    # pg.quit()


if __name__ == "__main__":
    main()