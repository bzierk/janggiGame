"""
Contains settings for the construction of a Janggi board and visualizing the board using pygame
"""

width = 649                      # width of play screen
height = 721                     # height of play screen
xDimension = 9                   # columns
yDimension = 10                  # rows
sqWidth = width // xDimension    # width of a single square
sqHeight = height // yDimension  # height of a single square
xOffset = sqWidth // 2           # horizontal midpoint of a square
yOffset = sqHeight // 2          # vertical midpoint of a square
maxFps = 15
board_color = (245, 150, 23)
line_color = (0, 0, 0)
