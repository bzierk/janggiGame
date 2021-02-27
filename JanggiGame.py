# Author: Bryan Zierk
# Date: 2/26/21
# Description:

import pygame as p
import JanggiEngine

width = 649
height = 721
xDimension = 9
yDimension = 10
sqWidth = width // xDimension
sqHeight = height // yDimension
xOffset = sqWidth // 2
yOffset = sqHeight // 2
maxFps = 15
images = {}


def load_images():
    """
    Used to load in png files for pieces of each color
    """
    pieces = ['bCannon', 'bChariot', 'bElephant', 'bGeneral', 'bGuard', 'bHorse', 'bSoldier',
              'rCannon', 'rChariot', 'rElephant', 'rGeneral', 'rGuard', 'rHorse', 'rSoldier']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (sqWidth, sqHeight))


def main():
    p.init()
    disp_board = p.display.set_mode((width, height))
    disp_board.fill(p.Color("black"))
    clock = p.time.Clock()
    game_state = JanggiEngine.GameState()
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
    drawBoard(disp_board)
    drawPieces(disp_board, game_state.get_board())


def drawBoard(disp_board):
    # p.draw.rect(screen, "dark orange")
    board_color = (245, 150, 23)
    line_color = (0, 0, 0)
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
    p.draw.line(disp_board, line_color, (3 * sqWidth + xOffset, 2 * sqHeight + yOffset), (5 * sqWidth + xOffset, yOffset))
    p.draw.line(disp_board, line_color, (3 * sqWidth + xOffset, yOffset), (5 * sqWidth + xOffset, 2 * sqHeight + yOffset))


def drawPieces(disp_board, game_state):
    for r in range(yDimension):
        for c in range(xDimension):
            piece = game_state[r][c]
            if piece != '--':
                disp_board.blit(images[piece], p.Rect(c * sqWidth, r * sqHeight, sqWidth, sqHeight))


if __name__ == '__main__':
    main()
