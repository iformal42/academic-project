import pygame as pg
from player import Player
from object import Platform, Object
import math as m

# initializing constants
FPS = 60
SKY = (135, 206, 235)
WIDTH, HEIGHT = 1500, 900
VELOCITY = 6
falling = True
"""actions of player are :- idle,run,jump,double_jump,hit,fall,wall_jump"""
col = (0, 225, 0)


def check_collision(player, items):
    global falling
    for i in items:
        if pg.sprite.collide_mask(player, i):
            falling = False
            player.landed()
            player.rect.bottom = i.rect.top


def action_handler(p):
    """keys event handler"""
    p.fall(falling, 0)
    if not falling and not p.in_air:
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            p.direction = "right"
            p.run(VELOCITY)
        elif keys[pg.K_a]:
            p.direction = "left"
            p.run(-VELOCITY)


def blocks(width, height):
    """make block ground"""
    obj = Object(width, height)
    w, h = obj.block_w, obj.block_h

    count_tiles = m.ceil(WIDTH / w)

    return [Platform(tile * w, HEIGHT - h, width, height)
            for tile in range(count_tiles)]


def draw_ground(window, items):
    """draw the floor of the game"""
    for tile in items:
        tile.draw(window)


def main_game():
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((WIDTH, HEIGHT))

    # adding player object
    player = Player(32, 32)

    # storing blocks for floor
    floor = blocks(16, 16)

    running = True
    while running:
        # 60 FPS
        clock.tick(FPS)
        window.fill(SKY)

        for event in pg.event.get():
            # stop condition
            if event.type is pg.QUIT:
                running = False

            if event.type == pg.KEYUP:
                player.current_state = "idle"
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and player.jump_count < 2 and not falling:
                    player.jump_count += 1
                    if player.jump_count == 2:
                        player.air_timer += 25

        # making a floor
        draw_ground(window, floor)

        # animate the player

        player.animate_player(window)

        player.loop()

        check_collision(player=player, items=floor)

        action_handler(p=player)

        pg.display.update()


if __name__ == "__main__":
    main_game()
