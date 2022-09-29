"""
This module is used as board abstraction for the game.
"""

from board_fwd import Board # forward declaration of the board to solve circular imports
from player import AbstractPlayer

HUNTER = 1
BEAR = 2


class Board:
    """
    Board abstraction
    """
    adjacent = [[1, 2, 3],  # 0
                [0, 3, 4],
                [0, 3, 6],  # 2
                [0, 1, 2, 5],
                [1, 7, 8],  # 4
                [3, 9, 10, 11],
                [2, 12, 13],  # 6
                [4, 8, 14],
                [7, 4, 14, 9],  # 8
                [8, 10, 5, 15],
                [5, 9, 11, 15],  # 10
                [5, 10, 15, 12],
                [11, 6, 16, 13],  # 12
                [6, 12, 16],
                [7, 8, 18],  # 14
                [9, 10, 11, 17],
                [12, 13, 19],  # 16
                [15, 18, 19, 20],
                [14, 17, 20],  # 18
                [16, 17, 20],
                [18, 17, 19]]

    def __init__(self, size: int, default_char='_'):
        self._default_char = default_char
        self._cells = [default_char] * size
        self._last_action = None

    def __str__(self):
        return ''.join(self._cells)

    def __getitem__(self, index):
        return self._cells[index]

    def __setitem__(self, index, value):
        self._cells[index] = value

    def get_hash(self) -> str:
        """ get hash of the board """
        return str(self)

    def get_cells(self) -> list[str]:
        """ get cells """
        return self._cells

    def set_cells(self, cells: list[str]) -> None:
        """ set cells """
        self._cells = cells

    def get_size(self) -> int:
        """ get size of the board """
        return len(self._cells)

    def get_default_char(self) -> str:
        """ get default character """
        return self._default_char

    def display(self):
        print("            "+self._cells[0]+"            ","             "+"0"+"            ")
        print("        "+self._cells[1]+"       "+self._cells[2]+"        ","         "+"1"+"       "+"2"+"        ")
        print("            "+self._cells[3]+"            ","             "+"3"+"            ")
        print("  "+self._cells[4]+"         "+self._cells[5]+"         "+self._cells[6]+"  ","   "+"4"+"         "+"5"+"         "+"6"+"  ")
        print(""+self._cells[7]+"   "+self._cells[8]+"   "+self._cells[9]+"   "+self._cells[10]+"   "+self._cells[11]+"   "+self._cells[12]+"   "+self._cells[13]+"",
              " "+"7"+"   "+"8"+"   "+"9"+"  "+"10"+"  "+"11"+"  "+"12"+"  "+"13"+"")
        print("  "+self._cells[14]+"         "+self._cells[15]+"         "+self._cells[16]+"  ","  "+"14"+"        "+"15"+"        "+"16"+"")
        print("            "+self._cells[17]+"            ","            "+"17"+"            ")
        print("        "+self._cells[18]+"       "+self._cells[19]+"        ","        "+"18"+"      "+"19"+"        ")
        print("            "+self._cells[20]+"            ","            "+"20"+"            ")


class Game:
    """
    Game abstraction
    """
    end_states = ['2111_________________',
                  '1_21__1______________',
                  '__1___2_____11_______',
                  '______1_____12__1____',
                  '____________11__2__1_',
                  '________________11_21',
                  '_________________1112',
                  '______________1__12_1',
                  '_______11_____2___1__',
                  '____1__21_____1______',
                  '_1__2__11____________',
                  '12_11________________']

    def __init__(self, 
            board: Board, 
            player1: AbstractPlayer, 
            player2: AbstractPlayer, 
            max_turns: int = 300):
        self._default_cells = board._cells.copy()
        self._board = board
        self._player_1: AbstractPlayer = player1
        self._player_2: AbstractPlayer = player2
        self._turn: int = 0
        self._max_turns: int = max_turns
        self._winner: 0 | 1 | 2 = None

    def has_ended(self) -> bool:
        """
        Check if the game has ended
        """
        if self._board.get_hash() in self.end_states:
            self._winner = HUNTER
            return True
        elif self._turn >= self._max_turns:
            self._winner = BEAR
            return True
        else:
            return False

    def get_winner(self) -> int:
        """
        Get the winner of the game
        """
        return self._winner

    def print_winner(self) -> None:
        """
        Print the winner of the game
        """
        if not self.has_ended():
            print("The game has not ended yet")
            return

        if self._winner == HUNTER:
            print("The hunter won!")
        elif self._winner == BEAR:
            print("The bear won!")

    def switch_players(self, curr_player: AbstractPlayer) -> AbstractPlayer:
        """
        Switch players
        """
        if curr_player is self._player_1:
            return self._player_2
        else:
            return self._player_1

    def play(self, show_board: bool = False) -> int:
        """
        Play the game
        """
        curr_player = self._player_1
        while True:
            if show_board:
                self._board.display()

            curr_player.move(self._board)
            curr_player.add_state(self._board.get_hash())
            if curr_player.get_symbol() == '2':
                self._turn += 1

            if self.has_ended():
                break
                
            curr_player = self.switch_players(curr_player)

        return self.get_winner()

    def train(self, n_times: int = 100) -> None:
        """
        Train the players
        """
        for _ in range(n_times):
            self.play()
            self.apply_reward()
            self.reset()

        self._player_1.save_policy(
            n_times,
            self._player_2.get_state_info(n_times)
        )
        self._player_2.save_policy(
            n_times,
            self._player_1.get_state_info(n_times)
        )
        print("Saved policy")

    def apply_reward(self) -> None:
        """
        Apply reward to the players
        """
        bear = (
            self._player_1 if self._player_1.get_symbol() == '2' else
            self._player_2
        )
        hunter = (
            self._player_2 if self._player_1.get_symbol() == '2' else
            self._player_1
        )
        if self._winner == HUNTER:
            bear.feed_reward(has_won=False)
            hunter.feed_reward(has_won=True)
        elif self._winner == BEAR:
            bear.feed_reward(has_won=True)
            hunter.feed_reward(has_won=False)

    def reset(self) -> None:
        """
        Reset the game
        """
        self._turn = 0
        self._board.set_cells(self._default_cells.copy())
        self._winner = None
        self._player_1.reset()
        self._player_2.reset()
