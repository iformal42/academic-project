import pygame as pg
from object import Platform, Object, Trap
import math as m

SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 900
MAX_SCREEN_WIDTH = 7 * SCREEN_WIDTH
sky, sun = (135, 206, 235), pg.image.load("gameasset/decoration/sun.png")
coconut_tree = pg.image.load("gameasset/decoration/coconut-tree.png")
mass_tree = pg.image.load("gameasset/decoration/mass_tree.png")
tree = pg.image.load("gameasset/decoration/tree.png")
unit = 90


def blocks(width, height, pos_x, pos_y):
    """make block ground"""
    obj = Object(width, height)
    w, h = obj.block_w - pos_x, obj.block_h - pos_y
    count_tiles = m.ceil(MAX_SCREEN_WIDTH / w)
    platforms = []
    for tile in range(-2, count_tiles):
        if tile in (8, 9, 28, 29, 30, 31, 51, 52, 53, 102, 103,):
            continue
        platforms.append(Platform(tile * w, SCREEN_HEIGHT - h, width, height, 96, 0))
    return platforms


def platform(x, high, count):
    """making platform; x:horizontal position in screen,high:vertical position about bottom,
    count:no. of block"""
    breaks = []
    for i in range(count):
        floor = Platform(x + 90 * i, SCREEN_HEIGHT - high * 48, 48, 16, 192, 0)
        breaks.append(floor)
        print(floor.rect.topright)

    return breaks


def wall(x, breaks_count) -> list:
    """make walls"""
    walls = []
    for h in range(2, breaks_count + 2):
        walls.append(Platform(x, SCREEN_HEIGHT - h * (48 + 16), 48, 48, 352 - 80, 64))
    return walls


def layout(window, width, height, offset_x):
    window.fill(sky)
    window.blit(sun, (750, 100))
    window.blit(coconut_tree, (500 - offset_x, height - 316))
    window.blit(tree, (width - 200 - offset_x, height - 316))
    window.blit(mass_tree, (2 * width - offset_x, height - 316))


#
def wall_stares(stare_len, position, reverse=False):
    change = 0
    if reverse:
        change = stare_len - 1
    stare_list = []

    for b in range(stare_len):
        stare = wall(position + b * 90, abs(change - b))
        stare_list.extend(stare)

    return stare_list


traps_pos = [unit * (32 + i*2) + 35 for i in range(1,10)]
x_pos_traps = [unit * 6, unit * 20, *traps_pos]
y_pos_traps = [122]
ground_position_trap = [(x, y_pos_traps[0]) for x in x_pos_traps]
coordinates_of_traps = [*ground_position_trap]


def make_traps():
    """list of tuples (x,y); x is position from right , y from bottom"""
    trap_list = []
    for i in coordinates_of_traps:
        trap_list.append(Trap(i[0], SCREEN_HEIGHT - i[1]))
    return trap_list

def map1():
    # making floors
    floor = blocks(48, 48, 0, 0)

    # making walls
    stare = wall_stares(7, 95 * 90)
    starerev = wall_stares(7, 104 * 90, reverse=True)

    walls = [*wall(-180, 10), *wall(MAX_SCREEN_WIDTH, 9),
             *wall(58 * unit, 4), *wall(65 * unit, 3), *wall(72 * unit, 4),
             *wall(78 * unit, 1), *wall(83 * unit, 2), *wall(88 * unit, 3), *wall(93 * unit, 4),
             *stare, *starerev]

    platform01 = []
    temp01 = [platform01.extend(platform(unit * (34 + i * 5), 6, 2)) for i in range(5)]
    temp02 = [platform01.extend(platform(unit * (37 + i * 5), 10, 2)) for i in range(4)]

    platforms = [*platform(150, 6, 3), *platform(SCREEN_WIDTH + 100, 6, 3),
                 *platform(SCREEN_WIDTH + 600, 6, 4), *platform(SCREEN_WIDTH + 3 * 60, 10, 6),
                 *platform01]

    return [*floor, *walls, *platforms],make_traps()


