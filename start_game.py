'''
Author: Timothy Yang
Date: October 2019
Project: Row reduction game
'''
from Game import Game
import sys

new_game = Game(board_size = int(sys.argv[1]))
# new_game = Game(board_size = 6)
new_game.start()