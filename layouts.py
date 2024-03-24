import pygame as pg
from object import Platform, Object
import math as m

SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 900
MAX_SCREEN_WIDTH = 7 * SCREEN_WIDTH
sky, sun = (135, 206, 235), pg.image.load("gameasset/decoration/sun.png")
coconut_tree = pg.image.load("gameasset/decoration/coconut-tree.png")
mass_tree = pg.image.load("gameasset/decoration/mass_tree.png")
tree = pg.image.load("gameasset/decoration/tree.png")


def blocks(width, height, pos_x, pos_y):
    """make block ground"""
    obj = Object(width, height)
    w, h = obj.block_w - pos_x, obj.block_h - pos_y
    count_tiles = m.ceil(MAX_SCREEN_WIDTH / w)
    platforms = []
    for tile in range(-2, count_tiles):
        if tile in (8, 9, 28, 29, 30, 31, 51, 52, 53):
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


def wall(x, breaks_count):
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


def map1():
    floor = blocks(48, 48, 0, 0)

    walls = [*wall(-180, 10), *wall(MAX_SCREEN_WIDTH, 9)]

    platforms = [*platform(150, 6, 3), *platform(SCREEN_WIDTH + 100, 6, 3),
                 *platform(SCREEN_WIDTH + 700, 6, 3), *platform(SCREEN_WIDTH + 3 * 60, 10, 6)]

    return [*floor, *walls, *platforms]
