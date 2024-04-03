import pygame as pg
from enemy import Enemy
from object import Platform, Object, Trap, Fruits
import math as m

SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 900
MAX_SCREEN_WIDTH = 7 * SCREEN_WIDTH
sky, sun = (135, 206, 235), pg.image.load("gameasset/decoration/sun.png")
coconut_tree = pg.image.load("gameasset/decoration/coconut-tree.png")
mass_tree = pg.image.load("gameasset/decoration/mass_tree.png")
tree = pg.image.load("gameasset/decoration/tree.png")
home = pg.image.load("gameasset/decoration/wooden-house.png")
htree1 = pg.image.load("gameasset/decoration/dead-tree1.png")
htree2 = pg.image.load("gameasset/decoration/horror tree.png")
htree3 = pg.image.load("gameasset/decoration/dead-tree.png")
current_level = 1
unit = 90


def fruit(count, x, y):
    fruits = []
    for i in range(count):
        floor = Fruits(x + i * 90 + 45, y)
        fruits.append(floor)

    return fruits


def blocks(width, height, pos_x, pos_y, begin_x=96, begin_y=0):
    """make block ground"""
    obj = Object(width, height)
    w, h = obj.block_w - pos_x, obj.block_h - pos_y
    count_tiles = m.ceil(MAX_SCREEN_WIDTH / w)
    platforms = []
    for tile in range(-2, count_tiles):
        if tile in (8, 9, 28, 29, 30, 31, 51, 52, 53, 102, 103,):
            continue
        platforms.append(Platform(tile * w, SCREEN_HEIGHT - h, width, height, begin_x, begin_y))
    return platforms


def platform(x, high, count):
    """making platform; x:horizontal position in screen,high:vertical position about bottom,
    count:no. of block"""
    breaks = []
    if current_level == 2:
        begin_y = 64
    else:
        begin_y = 0
    for i in range(count):
        floor = Platform(x + 90 * i, SCREEN_HEIGHT - high * 48, 48, 16, 192, begin_y=begin_y)
        breaks.append(floor)

    return breaks


def wall(x, breaks_count) -> list:
    """make walls"""
    walls = []
    for h in range(2, breaks_count + 2):
        walls.append(Platform(x, SCREEN_HEIGHT - h * (48 + 16), 48, 48, 352 - 80, 64))
    return walls


def layout(window, width, height, offset_x, level):
    global current_level
    if level == 1:
        window.fill(sky)
        window.blit(sun, (750, 100))
        window.blit(coconut_tree, (500 - offset_x, height - 316))
        window.blit(coconut_tree, (unit * 62 - offset_x, height - 316))
        window.blit(tree, (width - 200 - offset_x, height - 316))
        window.blit(tree, (unit * 69 - offset_x, height - 316))
        window.blit(mass_tree, (2 * width - offset_x, height - 316))
        window.blit(mass_tree, (unit * 42 - offset_x, height - 316))
        window.blit(coconut_tree, (unit * 112 - offset_x, height - 316))
        window.blit(home, (unit * 114 - offset_x, height - 310))
    if level == 2:
        current_level = 2
        window.fill((4, 26, 64))
        window.blit(htree2, (500 - offset_x, height - 316))
        window.blit(htree2, (unit * 62 - offset_x, height - 316))
        window.blit(htree1, (width - 200 - offset_x, height - 300))
        window.blit(htree2, (unit * 69 - offset_x, height - 316))
        window.blit(htree1, (2 * width - offset_x, height - 300))
        window.blit(htree3, (unit * 42 - offset_x, height - 300))
        window.blit(htree3, (unit * 112 - offset_x, height - 300))
        window.blit(home, (unit * 114 - offset_x, height - 310))


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


traps_pos = [unit * (32 + i * 2) + 35 for i in range(1, 10)]
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


def map1(level):
    global current_level
    if level == 1:
        enemy1 = Enemy(400, 550, 270)
        enemy2 = Enemy(2190, 360, 6 * 90, "pig")
        enemy3 = Enemy(11 * 90, 789, 17 * 90, "snail", flip="first")
        enemy4 = Enemy(27 * 90, 789, 17 * 90, "snail")
        enemy5 = Enemy(60 * 90, 750, 90 * 5, name="bunny", flip="first")
        enemy6 = Enemy(64 * 90, 750, 90 * 5, name="bunny")
        enemy7 = Enemy(67 * 90, 772, 90 * 5, name="chicken", flip="first")
        enemy8 = Enemy(71 * 90, 771, 90 * 5, name="chicken")
        enemy9 = Enemy(85 * 90, 771, 90 * 3, name="pig", flip="first")
        enemy10 = Enemy(92 * 90, 771, 90 * 3, name="mushroom")
        enemies = [enemy1, enemy2, enemy3, enemy4, enemy6, enemy5, enemy7, enemy8, enemy9, enemy10]

        # making floors
        floor = blocks(48, 48, 0, 0)

        # making walls
        stare = wall_stares(7, 95 * 90)
        starerev = wall_stares(7, 104 * 90, reverse=True)

        walls = [*wall(-180, 10), *wall(117 * unit, 9),
                 *wall(58 * unit, 4), *wall(65 * unit, 3), *wall(72 * unit, 4),
                 *wall(78 * unit, 1), *wall(83 * unit, 2), *wall(88 * unit, 3), *wall(93 * unit, 4),
                 *stare, *starerev]

        platform01 = []
        fruit01 = []
        temp01 = [(fruit01.extend(fruit(count=2, x=unit * (34 + i * 5), y=590)),
                   platform01.extend(platform(unit * (34 + i * 5), 6, 2))) for i in range(5)]
        temp02 = [(fruit01.extend(fruit(count=2, x=unit * (37 + i * 5), y=400)),
                   platform01.extend(platform(unit * (37 + i * 5), 10, 2))) for i in range(4)]

        platforms = [*platform(150, 6, 3), *platform(SCREEN_WIDTH + 100, 6, 3),
                     *platform(SCREEN_WIDTH + 600, 6, 4), *platform(SCREEN_WIDTH + 3 * 60, 10, 6),
                     *platform01]
        fruits = [*fruit(count=3, x=150, y=590), *fruit(3, x=SCREEN_WIDTH + 100, y=590),
                  *fruit(4, x=SCREEN_WIDTH + 600, y=590), *fruit(6, x=SCREEN_WIDTH + 3 * 60, y=400),
                  *fruit01, *fruit(3, 61 * unit, 800), *fruit(3, 68 * unit, 800),
                  *fruit(4, 84 * unit, 800), *fruit(4, 89 * unit, 800),
                  *fruit(1, 101 * unit + 50, 300), *fruit(1, 101 * unit + 100, 200), *fruit(1, 101 * unit + 150, 100),
                  *fruit(1, 101 * unit + 200, 200), *fruit(1, 101 * unit + 250, 300)]
        return [*floor, *walls, *platforms], make_traps(), enemies, fruits

    if level == 2:
        current_level = 2

        enemy1 = Enemy(400, 550, 270)
        enemy2 = Enemy(2190, 360, 6 * 90, "bat")
        enemy3 = Enemy(11 * 90, 770, 17 * 90, "ghost", flip="first")
        enemy4 = Enemy(27 * 90, 770, 17 * 90, "ghost")
        enemy5 = Enemy(60 * 90, 780, 90 * 5, name="slime", flip="first")
        enemy6 = Enemy(64 * 90, 780, 90 * 5, name="slime")
        enemy7 = Enemy(67 * 90, 762, 90 * 5, name="chameleon", flip="first")
        enemy8 = Enemy(71 * 90, 762, 90 * 5, name="chameleon")
        enemy9 = Enemy(85 * 90, 774, 90 * 3, name="pig", flip="first")
        enemy10 = Enemy(92 * 90, 771, 90 * 3, name="mushroom")
        enemies = [enemy1, enemy2, enemy3, enemy4, enemy6, enemy5, enemy7, enemy8, enemy9, enemy10]

        # making floors
        floor = blocks(48, 48, 0, 0, begin_x=0, begin_y=128)

        # making walls
        stare = wall_stares(7, 95 * 90)
        starerev = wall_stares(7, 104 * 90, reverse=True)

        walls = [*wall(-180, 10), *wall(117 * unit, 9),
                 *wall(58 * unit, 4), *wall(65 * unit, 3), *wall(72 * unit, 4),
                 *wall(78 * unit, 1), *wall(83 * unit, 2), *wall(88 * unit, 3), *wall(93 * unit, 4),
                 *stare, *starerev]

        platform01 = []
        fruit01 = []
        temp01 = [(fruit01.extend(fruit(count=2, x=unit * (34 + i * 5), y=590)),
                   platform01.extend(platform(unit * (34 + i * 5), 6, 2))) for i in range(5)]
        temp02 = [(fruit01.extend(fruit(count=2, x=unit * (37 + i * 5), y=400)),
                   platform01.extend(platform(unit * (37 + i * 5), 10, 2))) for i in range(4)]

        platforms = [*platform(150, 6, 3), *platform(SCREEN_WIDTH + 100, 6, 3),
                     *platform(SCREEN_WIDTH + 600, 6, 4), *platform(SCREEN_WIDTH + 3 * 60, 10, 6),
                     *platform01]
        fruits = [*fruit(count=3, x=150, y=590), *fruit(3, x=SCREEN_WIDTH + 100, y=590),
                  *fruit(4, x=SCREEN_WIDTH + 600, y=590), *fruit(6, x=SCREEN_WIDTH + 3 * 60, y=400),
                  *fruit01, *fruit(3, 61 * unit, 800), *fruit(3, 68 * unit, 800),
                  *fruit(4, 84 * unit, 800), *fruit(4, 89 * unit, 800),
                  *fruit(1, 101 * unit + 50, 300), *fruit(1, 101 * unit + 100, 200),
                  *fruit(1, 101 * unit + 150, 100),
                  *fruit(1, 101 * unit + 200, 200), *fruit(1, 101 * unit + 250, 300)]
        return [*floor, *walls, *platforms], make_traps(), enemies, fruits
