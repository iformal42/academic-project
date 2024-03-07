import pygame as pg
from player import Player
from ground import Platform

# initializing constants
FPS = 60
SKY = (135, 206, 235)
WIDTH, HEIGHT = 1500, 900
VELOCITY = 6
DEFAULT_STATE = "idle"
"""actions of player are :- idle,run,jump,double_jump,hit,fall,wall_jump"""


def action_handler(p):
    """keys event handler"""

    keys = pg.key.get_pressed()

    if all(key == 0 for key in keys):
        p.current_state = DEFAULT_STATE
    elif keys[pg.K_d]:
        p.direction = "right"
        p.run(VELOCITY)
    elif keys[pg.K_a]:
        p.direction = "left"
        p.run(-VELOCITY)
    elif keys[pg.K_w]:
        p.jump(VELOCITY, -2)


def main_game():
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((WIDTH, HEIGHT))

    # adding player object
    player = Player(32, 32, window)
    block = Platform(3 * 16, 3 * 16, window)
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

        # animate the player
        player.animate_player()
        for i in range(16):
            window.blit(block.block, (i*96, HEIGHT - 2 * 48))

        # update the screens
        pg.display.update()


if __name__ == "__main__":
    main_game()
