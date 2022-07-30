"""
This module handles all the logic to start the game
"""
import argparse
from board import Board, Game
from player import AIPlayer

DEFAULT_NO_PLAYER = 'random'
DEFAULT_HUNTER_POSITION = [0, 1, 2]
DEFAULT_BEAR_POSITION = [20]
def inizialize_board() -> Board:
    """
    Initialize the board
    """
    board = Board(21)
    board[0] = '1'
    board[1] = '1'
    board[2] = '1'

    board[20] = '2'
    return board


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hunter_player', type=str, default=DEFAULT_NO_PLAYER)
    parser.add_argument('--bear_player', type=str, default=DEFAULT_NO_PLAYER)
    parser.add_argument('--n_games', type=int, default=100)
    return parser.parse_args()

if __name__ == '__main__':
    args = _parse_arguments()
    hunter_player_file = args.hunter_player
    bear_player_file = args.bear_player
    n_games = args.n_games

    hunter_player = AIPlayer(DEFAULT_HUNTER_POSITION, 'hunter', '1')
    bear_player = AIPlayer(DEFAULT_BEAR_POSITION, 'bear', '2')


    if hunter_player_file != DEFAULT_NO_PLAYER:
        hunter_player.load_policy(hunter_player_file)

    if bear_player_file != DEFAULT_NO_PLAYER:
        bear_player.load_policy(bear_player_file)

    board = inizialize_board()
    game = Game(board, hunter_player, bear_player)
    game.train(n_games)
