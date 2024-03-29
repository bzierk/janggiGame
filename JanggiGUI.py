# Author: Bryan Zierk
# Date: 2/26/21
# Description: This program allows the user to play Janggi, a Korean board game similar to Xiangqi or Chinese Chess.
# The game is played on a board which is 9 lines wide by 10 lines tall where pieces are placed at the intersection
# of lines similar to Go. Players take turns moving pieces in an attempt to trap the opposing player's General. A player
# is victorious once they have checkmated the opposing general by leaving them no remaining valid moves.

import pygame as p
import JanggiGame as jg
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
    pieces = ['blueCannon', 'blueChariot', 'blueElephant', 'blueGeneral', 'blueGuard', 'blueHorse', 'blueSoldier',
              'redCannon', 'redChariot', 'redElephant', 'redGeneral', 'redGuard', 'redHorse', 'redSoldier']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (sqWidth, sqHeight))


def main():
    """
    If JanggiGUI is run as a script, main will use pygame to allow 2 users to play a game of Janggi
    """
    p.init()
    disp_board = p.display.set_mode((width, height))
    disp_board.fill(p.Color("black"))
    clock = p.time.Clock()
    game_state = jg.JanggiGame()
    valid_moves = game_state.get_valid_moves(game_state.active_turn())
    update_board = False
    load_images()
    sel_square = ()
    orig_dest_list = []
    while game_state.get_game_state() == 'UNFINISHED':
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()
                # print("loc is: ", loc)
                mouse_col = loc[0] // sqWidth
                mouse_row = loc[1] // sqHeight
                sel_square = (mouse_row, mouse_col)
                #print("selected square is: ", sel_square)
                orig_dest_list.append(sel_square)
                #print("list is: ", orig_dest_list)
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    sel_square = ()
                    orig_dest_list = []
            if len(orig_dest_list) == 2:
                move = jg.Move(orig_dest_list[0], orig_dest_list[1], game_state.get_board())
                # print("move is: ", move)
                # print("Origin is: ", orig)
                # print("Destination is: ", dest)
                if move in valid_moves:
                    game_state.make_move_helper(move)
                    sel_square = ()
                    update_board = True
                # game_state.terminal_print_board()
                orig_dest_list = []
        if update_board:
            valid_moves = game_state.get_valid_moves(game_state.active_turn())
            if len(valid_moves) == 0:
                if game_state.active_turn() == 'blue':
                    print('RED WON')
                    game_state.set_game_state('RED_WON')
                else:
                    print('BLUE WON')
                    game_state.set_game_state('BLUE_WON')
            update_board = False
        draw_game_state(disp_board, game_state, valid_moves, sel_square)
        clock.tick(maxFps)
        p.display.flip()


def input_to_string(mouse_x, mouse_y):
    """
    Converts mouse coordinates into a string which JanggiGame's make_move method can read
    """
    row = str(mouse_y + 1)
    col = str(chr(mouse_x + 97))
    return col + row


def highlight_valid_moves(disp_board, game_state, valid_moves, sel_square):
    if sel_square != ():
        r, c = sel_square
        if game_state.get_board()[r][c] is not None:
            if game_state.get_board()[r][c].get_color() == game_state.active_turn():
                s = p.Surface((sqWidth, sqHeight))
                s.set_alpha(100)
                s.fill(p.Color('black'))
                disp_board.blit(s, (c * sqWidth, r * sqHeight))
                s.fill(p.Color('red'))
                for move in valid_moves:
                    #print("r, c: ", r, c)
                    #print("orig: ", move.get_orig()[0], move.get_orig()[1])
                    if move.get_orig()[0] == r and move.get_orig()[1] == c:
                        disp_board.blit(s, (move.get_target()[1] * sqHeight, move.get_target()[0] * sqWidth))
    pass


def draw_game_state(disp_board, game_state, valid_moves, sel_square):
    draw_board(disp_board)
    highlight_valid_moves(disp_board, game_state, valid_moves, sel_square)
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
            if piece is not None:
                disp_board.blit(images[piece.get_color() + piece.get_name()], p.Rect(c * sqWidth, r * sqHeight,
                                                                                     sqWidth, sqHeight))


if __name__ == '__main__':
    main()
