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
maxFps = 15
images = {}


def loadImages():
    """
    Used to load in png files for pieces of each color
    """
    pieces = ['bCannon', 'bChariot', 'bElephant', 'bGeneral', 'bGuard', 'bHorse', 'bSoldier',
              'rCannon', 'rChariot', 'rElephant', 'rGeneral', 'rGuard', 'rHorse', 'rSoldier']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (sqWidth, sqHeight))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    screen.fill(p.Color("black"))
    clock = p.time.Clock()
    gs = JanggiEngine.GameState()
    loadImages()
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(maxFps)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.get_board())

def drawBoard(screen):
    #p.draw.rect(screen, "dark orange")
    colors = [p.Color("white"), p.Color("dark orange")]
    for r in range(yDimension):
        for c in range(xDimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sqWidth, r*sqHeight, sqWidth, sqHeight))

def drawPieces(screen, board):
    pass

if __name__ == '__main__':
    main()
