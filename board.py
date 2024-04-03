import pygame as pg


class Board:
    def __init__(self, screen, font="freesansbold.ttf"):
        # with open("highscore.txt") as s:
        #     self.high_score = int(s.read())
        self.font_style = font
        self.window = screen

    def show_score(self, size: int, msg: str, color: tuple, pos: tuple):
        """color should be rgb"""
        font = pg.font.Font(self.font_style, size)
        text = f"{msg}"
        score_board = font.render(text, True, color)
        self.window.blit(score_board, pos)

    def reset_board(self, score: int):
        """update board if highest score achieved"""
        if score > self.high_score:
            self.high_score = score
            print("HIGHEST SCORE HAS BEEN ACHIEVED", self.high_score)
            with open("highscore.txt", "w") as s:
                highest = s.write(str(self.high_score))

    def game_over(self, size: int, color: tuple, pos: tuple, msg: str = "GAME OVER"):
        """game over text"""
        g_font = pg.font.Font(self.font_style, size)
        score_board = g_font.render(msg, True, color)
        self.window.blit(score_board, pos)
