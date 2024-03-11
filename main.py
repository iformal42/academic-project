import pygame as pg
from player import Player
from object import Platform, Object
import math as m

# initializing constants
FPS = 60
SKY = (135, 206, 235)
WIDTH, HEIGHT = 1500, 900
VELOCITY = 6
default_state = "idle"
"""actions of player are :- idle,run,jump,double_jump,hit,fall,wall_jump"""
col = (0, 225, 0)


# def check_collision(player):
#     global default_state
#
#     else:
#         default_state = "idle"


def action_handler(p):
    """keys event handler"""
    global default_state

    not_falling = True
    if p.rect.y < 850:
        not_falling = False
        default_state = "fall"
        p.fall()

    if not_falling:
        p.rect.y = 769
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            p.direction = "right"
            default_state = "run"
            p.run(VELOCITY)
        elif keys[pg.K_a]:
            p.direction = "left"
            default_state = "run"
            p.run(-VELOCITY)
        elif keys[pg.K_w]:
            p.jump(VELOCITY, -2)
        # elif keys[pg.K_x]:
        #     p.jump(VELOCITY, 2)
        else:
            default_state = "idle"


def blocks(width, height):
    """make block ground"""
    obj = Object(width, height)
    w, h = obj.block_w, obj.block_h

    count_tiles = m.ceil(WIDTH / w)

    return [Platform(tile * w, HEIGHT - h, width, height)
            for tile in range(count_tiles)]


def draw_ground(window, items):
    for tile in items:
        tile.draw(window)



def main_game():
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((WIDTH, HEIGHT))

    # adding player object
    player = Player(32, 32, window)

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
            # detects key pressed
        action_handler(p=player)

        draw_ground(window, floor)
        # animate the player
        sprite = player.animate_player()
        for i in floor:
            if pg.sprite.collide_mask(sprite,i):
                print("yes")

        # check_collision(player)
        player.current_state = default_state
        pg.display.update()


if __name__ == "__main__":
    main_game()
