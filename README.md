# Janggi Game

Janggi is a strategy board game popular in Korea. A derivative of Chinese chess and similar to the more common Western Chess, Janggi is played between two players on a 9x10 gameboard. Unlike Western Chess, in Janggi, pieces are placed at the intersection of two lines rather than in the spaces formed by intersecting lines. In addition to the 9x10 grid, Janggi is unique in that it has a 2x2 block of diagonal lines forming a "Palace" in the center of each player's defensive end. The palace introduces unique movement opportunities for many of the pieces as well as restricting the Emperor and his Guards to those spaces.

For complete rules, refer to this [article](https://ancientchess.com/page/play-janggi.htm)

This implementation of Janggi was created as my portfolio project for Introduction to Computer Science II through Oregon State University's Computer Science program.

The guidelines for the project required that we implement the engine for a Janggi game which would be played as shown in the engine below:

Here's a very simple example of how the class could be used:
```
game = JanggiGame()
move_result = game.make_move('c1', 'e3') #should be False because it's not Red's turn
move_result = game.make_move('a7,'b7') #should return True
blue_in_check = game.is_in_check('blue') #should return False
game.make_move('a4', 'a5') #should return True
state = game.get_game_state() #should return UNFINISHED
game.make_move('b7','b6') #should return True
game.make_move('b3','b6') #should return False because it's an invalid move
game.make_move('a1','a4') #should return True
game.make_move('c7','d7') #should return True
game.make_move('a4','a4') #this will pass the Red's turn and return True
```

In the interest of self improvement (...and to simplify debugging of an otherwise complex game,) I researched the best way to implement a GUI for my game and after experimenting with a couple of options, I settled on the PyGame library. 

