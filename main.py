import pygame as pg
from pygame import mixer
from player import Player
from object import Collect
from board import Board
import layouts as lay
from layouts import map1

# initializing constants
FPS = 60
WIDTH, HEIGHT = lay.SCREEN_WIDTH, lay.SCREEN_HEIGHT
MAX_WIDTH = lay.MAX_SCREEN_WIDTH
VELOCITY = 6
falling = True
score = 0

collected = []

mixer.init()
eat_sound = mixer.Sound("gameasset/music/eat.mp3")
hit_sound = mixer.Sound("gameasset/music/hit.mp3")
jump_sound = mixer.Sound("gameasset/music/jump.mp3")
mixer.music.load("gameasset/music/level1.mp3")

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
            hit_sound.play()
            player.hit()
            return trap


def check_enemy_collision(player, items):
    """checking enemy collision with player"""
    e = items
    for enemy in items:
        if pg.sprite.collide_mask(player, enemy):
            if player.current_state == "fall" and player.rect.bottom > enemy.rect.top:
                items.remove(enemy)
                return enemy
            else:
                hit_sound.play()
                player.hit()
                return enemy


def fruit_collision(player, items):
    """checking trap collision with player"""
    global score

    for fruit in items:
        if pg.sprite.collide_mask(player, fruit):
            c = Collect()
            eat_sound.play()
            c.rect.x, c.rect.y = fruit.rect.x, fruit.rect.y
            collected.append(c)
            items.remove(fruit)
            score += 100
            break


def action_handler(p, floor, obstacle, fruit_list, enemies):
    """keys event handler"""
    collide_right = collide(p, floor, VELOCITY * 1.5)
    collide_left = collide(p, floor, -VELOCITY * 1.5)
    check_trap_collision(player=p, items=obstacle)
    check_enemy_collision(player=p, items=enemies)
    fruit_collision(player=p, items=fruit_list)
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


def draw_items(window, items, offset_x, player, traps_items, enemy_list, fruits):
    """drawing the items of the game"""
    # making a floor

    for tile in items:
        tile.draw(window, offset_x)
    # animate the player
    for trap in traps_items:
        trap.draw(window, offset_x)

    for fruit in fruits:
        fruit.draw(window, offset_x)

    for enemy in enemy_list:
        enemy.draw(window, offset_x)
    for cc in collected:
        d = cc.draw(window, offset_x)
        if d:
            collected.remove(cc)
    player.draw(window, offset_x)


def game_end(banner, window, message, pos=(550, 450), color=(255, 0, 0)):
    time = int(pg.time.get_ticks() / 1000)
    banner.game_over(70, color, pos, msg=message)
    pg.display.update()
    pg.time.wait(3000)
    window.fill((0, 0, 0))
    banner.show_score(70, f"Your score: {score}", (255, 255, 255), (400, 400))
    banner.show_score(70, f"Total Survival Time: {time} secs", (255, 255, 255), (400, 550))
    pg.display.update()
    pg.time.wait(6000)


def game_layout(level):
    return map1(level)


def main_game():
    # initialize the pygame
    pg.init()
    mixer.init()
    clock = pg.time.Clock()

    offset_x = 0
    scroll_boundary = WIDTH * 0.25
    level = 1

    mixer.music.play(-1)
    # window
    window = pg.display.set_mode((WIDTH, HEIGHT))  # , pg.FULLSCREEN | pg.SCALED)

    # adding player object
    player = Player(32, 32)

    # making map design
    # making floor,blocks,walls,enemy,traps,fruits

    map_objects, trap, enemies, fruit_list = game_layout(level)

    banner = Board(window)
    running = True
    while running:
        # 60 FPS
        clock.tick(FPS)
        lay.layout(window, WIDTH, HEIGHT, offset_x, level)
        banner.show_score(40, f"SCORE: {score}", (255, 255, 255), (20, 10))
        banner.show_score(40, f"LIFE: {player.life}", (255, 255, 255), (1300, 10))
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
                    jump_sound.play()
                    player.y_vel = -5
                    player.jump_count += 1
                    if player.jump_count == 2:
                        player.fall_count = 0
                        player.air_timer += 30

        # making a floor
        draw_items(window, map_objects, offset_x, player, trap, enemies, fruit_list)

        player.loop()
        check_up_down_collision(player=player, items=map_objects)
        action_handler(p=player, floor=map_objects, obstacle=trap,
                       fruit_list=fruit_list, enemies=enemies)  # enemies here

        if 300 < player.rect.x < 1500 * 6 + 1090:
            if ((player.rect.right - offset_x >= WIDTH - scroll_boundary) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_boundary) and player.x_vel < 0):
                offset_x += player.x_vel

        if 115 * 90 - 10 < player.rect.x < 115 * 90 + 10:
            mixer.music.load("gameasset/music/level2.mp3")
            mixer.music.play(-1)
            player.rect.center = (400, 800)
            pg.display.update()
            if level == 2:
                mixer.music.load("gameasset/music/gamewon.mp3")
                mixer.music.play(-1)
                game_end(banner, window, "HOME SWEET HOME", color=(0, 255, 0), pos=(400, 450))
                pg.quit()
            pg.time.wait(2000)
            offset_x = 0
            level = 2
            map_objects, trap, enemies, fruit_list = game_layout(level)

        if player.rect.y >= 950 or player.life < 0:
            game_end(banner, window, "GAME OVER")
            pg.quit()

        pg.display.update()


if __name__ == "__main__":
    main_game()
