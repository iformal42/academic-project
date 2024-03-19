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


def check_up_down_collision(player, items):
    global falling
    add = 1
    if player.current_state == "run":
        add = 10
    player.rect.bottom += add
    for i in items:
        if pg.sprite.collide_mask(player, i):

            if player.y_vel == 0:
                print("colide")
                falling = False
                player.rect.bottom = i.rect.top
                player.landed()
            if player.y_vel < 0:
                player.rect.top = i.rect.bottom
                player.air_count = player.air_timer + 1

            return "collided"

    player.rect.bottom -= add
    if not player.in_air:
        player.air_count = player.air_timer + 1


def collide(player, items, dx):
    global falling

    player.rect.move_ip(dx, 0)
    player.update()
    collided = None
    for ob in items:
        if pg.sprite.collide_mask(player, ob):
            collided = ob
            if player.in_air:
                player.x_vel *= -3 / VELOCITY

            break
    player.rect.move_ip(-dx, 0)
    player.update()
    return collided


def action_handler(p, floor):
    """keys event handler"""
    cr = collide(p, floor, VELOCITY * 1.5)
    cl = collide(p, floor, -VELOCITY * 1.5)
    p.fall(falling, 0)
    if not falling and not p.in_air:
        keys = pg.key.get_pressed()
        if keys[pg.K_d] and not cr:
            p.direction = "right"
            p.run(VELOCITY)
        elif keys[pg.K_a] and not cl:
            p.direction = "left"
            p.run(VELOCITY)
        else:
            p.x_vel = 0


def wall(x, breaks_count):
    walls = []
    for h in range(2, breaks_count + 2):
        walls.append(Platform(x, HEIGHT - h * (48 + 16), 48, 48, 352 - 80, 64))
    return walls


def platform(x, high, count):
    breaks = []
    for i in range(count):
        breaks.append(Platform(x + 90 * i, HEIGHT - high * 48, 48, 16, 192, 0))
    return breaks


def blocks(width, height, pos_x, pos_y):
    """make block ground"""
    obj = Object(width, height)
    w, h = obj.block_w - pos_x, obj.block_h - pos_y
    count_tiles = m.ceil(WIDTH / w) + 55
    platforms = []
    for tile in range(-2, count_tiles):
        if tile in (8, 9, 28, 29, 30, 31, 51, 52, 53):
            continue
        platforms.append(Platform(tile * w, HEIGHT - h, width, height, 96, 0))

    return platforms


def draw_items(window, items, offset_x, player):
    """drawing the items of the game"""
    # making a floor
    for tile in items:
        tile.draw(window, offset_x)
    # animate the player
    player.draw(window, offset_x)


def main_game():
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()
    offset_x = 0
    scroll_boundary = WIDTH * 0.25
    # window
    window = pg.display.set_mode((WIDTH, HEIGHT))

    # adding player object
    player = Player(32, 32)

    # storing blocks for floor
    floor = blocks(48, 48, 0, 0)
    walls = [*wall(-180, 10), *wall((WIDTH + 90) * 4, 9)]
    platforms = [*platform(150, 6, 3), *platform(WIDTH + 100, 6, 3),
                 *platform(WIDTH + 700, 6, 3), *platform(WIDTH, 10, 9)]
    map_objects = [*floor, *walls, *platforms]

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
                    player.y_vel = -5
                    player.jump_count += 1
                    if player.jump_count == 2:
                        player.air_timer += 30

        # making a floor
        draw_items(window, map_objects, offset_x, player)

        player.loop()
        is_collided = check_up_down_collision(player=player, items=map_objects)

        action_handler(p=player, floor=map_objects)
        if ((player.rect.right - offset_x >= WIDTH - scroll_boundary) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_boundary) and player.x_vel < 0):
            offset_x += player.x_vel

        pg.display.update()


if __name__ == "__main__":
    main_game()
