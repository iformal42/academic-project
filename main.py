import pygame as pg
from player import Player

# initializing constants
FPS = 60
SKY = (135, 206, 235)
WIDTH, HEIGHT = 1200, 1000
VELOCITY = 6
DEFAULT_STATE = "idle"


def action_handler(p):
    """keys event handler"""
    keys = pg.key.get_pressed()
    if keys[pg.K_d]:
        p.direction = "right"
        p.move(VELOCITY)
    if keys[pg.K_a]:
        p.direction = "left"
        p.move(-VELOCITY)

    if all(key == 0 for key in keys):
        p.current_state = DEFAULT_STATE


def main_game():
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((WIDTH, HEIGHT))

    # adding player object
    player = Player(32, 32, window)
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

        # update the screens
        pg.display.update()


if __name__ == "__main__":
    main_game()
