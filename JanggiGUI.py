# Author: Bryan Zierk
# Date: 2/26/21
# Description: This program allows the user to play Janggi, a Korean board game similar to Xiangqi or Chinese Chess.
# The game is played on a board which is 9 lines wide by 10 lines tall where pieces are placed at the intersection
# of lines similar to Go. Players take turns moving pieces in an attempt to trap the opposing player's General. A player
# is victorious once they have checkmated the opposing general by leaving them no remaining valid moves.

import pygame as p
import JanggiGame
import Settings

width = Settings.width
height = Settings.height
xDimension = Settings.xDimension
yDimension = Settings.yDimension
sqWidth = width // xDimension
sqHeight = height // yDimension
xOffset = sqWidth // 2
yOffset = sqHeight // 2
maxFps = Settings.maxFps
board_color = Settings.board_color
line_color = Settings.line_color
images = {}


def load_images():
    """
    Creates a dictionary of png image files for each unique piece
    """
    pieces = ['bCannon', 'bChariot', 'bElephant', 'bGeneral', 'bGuard', 'bHorse', 'bSoldier',
              'rCannon', 'rChariot', 'rElephant', 'rGeneral', 'rGuard', 'rHorse', 'rSoldier']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (sqWidth, sqHeight))


def main():
    """
    If JanggiGame is run as a script, main will use pygame to allow 2 users to play a game of Janggi
    """
    p.init()
    disp_board = p.display.set_mode((width, height))
    disp_board.fill(p.Color("black"))
    clock = p.time.Clock()
    game_state = JanggiGame.GameState()
    load_images()
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        draw_game_state(disp_board, game_state)
        clock.tick(maxFps)
        p.display.flip()


def draw_game_state(disp_board, game_state):
    draw_board(disp_board)
    draw_pieces(disp_board, game_state.get_board())


def draw_board(disp_board):
    # p.draw.rect(screen, "dark orange")

    for r in range(yDimension):
        for c in range(xDimension):
            p.draw.rect(disp_board, board_color, p.Rect(c * sqWidth, r * sqHeight, sqWidth, sqHeight))

    # draws horizontal lines on board
    for r in range(yDimension):
        p.draw.line(disp_board, line_color, (xOffset, (r * sqHeight) + yOffset), ((xDimension * sqWidth) - xOffset,
                                                                                  (r * sqHeight) + yOffset))

    # draws vertical lines on board
    for c in range(xDimension):
        p.draw.line(disp_board, line_color, ((c * sqWidth) + xOffset, yOffset), ((c * sqWidth) + xOffset,
                                                                                 (yDimension * sqHeight) - yOffset))

    # draws diagonal lines to represent the Palace
    p.draw.line(disp_board, line_color, (3 * sqWidth + xOffset, 7 * sqHeight + yOffset),
                (5 * sqWidth + xOffset, 9 * sqHeight + yOffset))
    p.draw.line(disp_board, line_color, (3 * sqWidth + xOffset, 9 * sqHeight + yOffset),
                (5 * sqWidth + xOffset, 7 * sqHeight + yOffset))
    p.draw.line(disp_board, line_color, (3 * sqWidth + xOffset, 2 * sqHeight + yOffset),
                (5 * sqWidth + xOffset, yOffset))
    p.draw.line(disp_board, line_color, (3 * sqWidth + xOffset, yOffset),
                (5 * sqWidth + xOffset, 2 * sqHeight + yOffset))


def draw_pieces(disp_board, game_state):
    for r in range(yDimension):
        for c in range(xDimension):
            piece = game_state[r][c]
            if piece != '--':
                disp_board.blit(images[piece], p.Rect(c * sqWidth, r * sqHeight, sqWidth, sqHeight))


if __name__ == '__main__':
    main()
