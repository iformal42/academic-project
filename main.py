import pygame as pg
from player import Player
from object import Trap
from enemy import Enemy
import layouts as lay
from layouts import map1, make_traps

# initializing constants
FPS = 60
WIDTH, HEIGHT = lay.SCREEN_WIDTH, lay.SCREEN_HEIGHT
MAX_WIDTH = lay.MAX_SCREEN_WIDTH
VELOCITY = 6
falling = True
x_pos_traps = [500, WIDTH, 2 * WIDTH]
y_pos_traps = [122, 348]
ground_position_trap = [(x, y_pos_traps[0]) for x in x_pos_traps]
COORDINATES_OF_TRAPS = [*ground_position_trap, (WIDTH + 200, y_pos_traps[1])]
"""actions of player are :- idle,run,jump,double_jump,hit,fall,wall_jump"""


def check_up_down_collision(player, items):
    """check_up_down_collision"""
    global falling
    add = 1
    if player.current_state == "run":
        add = 10
    player.rect.bottom += add
    for i in items:
        if pg.sprite.collide_mask(player, i):
            if player.y_vel == 0:
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
    """checking right and left of player and breaks"""
    player.rect.move_ip(dx, 0)
    player.update()
    collided = None
    for ob in items:
        if pg.sprite.collide_mask(player, ob):
            collided = ob
            if player.in_air:
                player.x_vel *= -1 / VELOCITY
            break
    player.rect.move_ip(-dx, 0)
    player.update()
    return collided


def check_trap_collision(player, items):
    """checking trap collision with player"""
    for trap in items:
        if pg.sprite.collide_mask(player, trap):
            player.hit()
            return trap


def action_handler(p, floor, obstacle):
    """keys event handler"""
    collide_right = collide(p, floor, VELOCITY * 1.5)
    collide_left = collide(p, floor, -VELOCITY * 1.5)
    check_trap_collision(player=p, items=obstacle)

    p.fall(falling, 0)

    if not falling and not p.in_air:
        keys = pg.key.get_pressed()
        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and (not p.is_hit) and not collide_right:
            p.direction = "right"
            p.run(VELOCITY)
        elif (keys[pg.K_a] or keys[pg.K_LEFT]) and (not collide_left) and (not p.is_hit):
            p.direction = "left"
            p.run(VELOCITY)
        else:
            p.x_vel = 0


def draw_items(window, items, offset_x, player, traps_items, enemy_list):
    """drawing the items of the game"""
    # making a floor
    for tile in items:
        tile.draw(window, offset_x)
    # animate the player
    for trap in traps_items:
        trap.draw(window, offset_x)
    for enemy in enemy_list:
        enemy.draw(window, offset_x)
    player.draw(window, offset_x)


def main_game():
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()
    offset_x = 0
    scroll_boundary = WIDTH * 0.25
    # window
    window = pg.display.set_mode((WIDTH, HEIGHT))  # , pg.FULLSCREEN | pg.SCALED)

    # adding player object
    player = Player(32, 32)

    enemy1 = Enemy(400, 550, 270)
    enemy2 = Enemy(2190, 360, 6 * 90, "pig")
    enemy3 = Enemy(11 * 90, 789, 17 * 90, "snail", flip="first")
    enemy4 = Enemy(28 * 90, 789, 18 * 90, "snail")
    enemy5 = Enemy(60 * 90, 750, 90 * 5, name="bunny", flip="first")
    enemy6 = Enemy(64 * 90, 750, 90 * 5, name="bunny")
    enemy7 = Enemy(67 * 90, 772, 90 * 5, name="chicken", flip="first")
    enemy8 = Enemy(71 * 90, 771, 90 * 5, name="chicken")
    enemy9 = Enemy(85 * 90, 771, 90 * 3, name="pig", flip="first")
    enemy10 = Enemy(92 * 90, 771, 90 * 3, name="mushroom")
    enemies = [enemy1, enemy2, enemy3, enemy4, enemy6, enemy5, enemy7, enemy8, enemy9, enemy10]

    # making map design
    # making floor,blocks,walls
    # traps
    map_objects, trap = map1()

    running = True
    while running:
        # 60 FPS
        clock.tick(FPS)
        lay.layout(window, WIDTH, HEIGHT, offset_x)

        for event in pg.event.get():
            # stop condition
            if event.type is pg.QUIT:
                running = False

            if event.type == pg.KEYUP:
                player.current_state = "idle"

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False

                if event.key == pg.K_SPACE and player.jump_count < 2 and not falling:
                    player.y_vel = -5
                    player.jump_count += 1
                    if player.jump_count == 2:
                        player.fall_count = 0
                        player.air_timer += 30

        # making a floor
        draw_items(window, map_objects, offset_x, player, trap, enemies)

        player.loop()
        check_up_down_collision(player=player, items=map_objects)

        action_handler(p=player, floor=map_objects, obstacle=[*trap, *enemies])  # enemies here
        if ((player.rect.right - offset_x >= WIDTH - scroll_boundary) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_boundary) and player.x_vel < 0):
            offset_x += player.x_vel
        if player.rect.y >= 950:
            player.rect.topleft = (90, 200)
            offset_x = 0
            # pg.quit()
        pg.display.update()


if __name__ == "__main__":
    main_game()
