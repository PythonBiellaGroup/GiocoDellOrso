"""
This module handles all the logic to start the game
"""
import argparse
import random
from board import Board, Game
from player import AIPlayer, HumanPlayer, AbstractPlayer


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
    parser.add_argument('--hunter_ai_file', 
        type=str, 
        help='Path to the hunter AI policy file',
        default=DEFAULT_NO_PLAYER)

    parser.add_argument('--bear_ai_file', 
        type=str, 
        help='Path to the bear AI policy file',
        default=DEFAULT_NO_PLAYER)

    parser.add_argument('--bear_human', 
        action='store_true',
        help='Use this flag if you want bear to be human player',
        default=False)

    parser.add_argument('--hunter_human', 
        action='store_true',
        help='Use this flag if you want hunter to be human player',
        default=False)

    parser.add_argument('--n_games', 
        type=int, 
        help='Number of games to play (useful for training phase)',
        default=1)

    parser.add_argument('--disable_training', 
        action='store_true',
        help='Use this flag if you just want to play',
        default=False)

    parser.add_argument('--seed', 
        type=int, 
        help='Seed for the random generator (None for random seed)',
        default=None)
    return parser.parse_args()

def initialize_players(args) -> tuple[AbstractPlayer, AbstractPlayer]:
    """
    Initialize the players
    """
    if args.hunter_human:
        hunter_ai = HumanPlayer(
            positions=DEFAULT_HUNTER_POSITION,
            name='hunter',
            symbol='1',
        )
    else:
        hunter_ai = AIPlayer(
            positions=DEFAULT_HUNTER_POSITION,
            name='hunter',
            symbol='1',
            loss_reward=-5, 
            win_reward=100
        )
        if args.hunter_ai_file != DEFAULT_NO_PLAYER:
            hunter_ai.load_policy(args.hunter_ai_file)

    if args.bear_human:
        bear_ai = HumanPlayer(
            positions=DEFAULT_BEAR_POSITION,
            name='bear',
            symbol='2',
        )
    else:
        bear_ai = AIPlayer(
            positions=DEFAULT_BEAR_POSITION,
            name='bear',
            symbol='2',
            loss_reward=-5, 
            win_reward=1
        )
        if (args.bear_ai_file != DEFAULT_NO_PLAYER):
            bear_ai.load_policy(args.bear_ai_file)

    return hunter_ai, bear_ai

if __name__ == '__main__':
    args = _parse_arguments()

    if args.seed is not None:
        random.seed(args.seed)

    hunter_player, bear_player = initialize_players(args)

    board = inizialize_board()
    game = Game(board, hunter_player, bear_player)

    if not args.disable_training:
        game.train(args.n_games)
    else:
        for _ in range(args.n_games):
            game.play(show_board=True)
            game.print_winner()
            game.reset()
