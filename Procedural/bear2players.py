# Moves for bear to win
MAX_BEAR_MOVES = 40
# Combinations for bear to loose, one for each edge position
# index ease'0,','1', '2', '3', '4', '5', '6', '7', '8', '9', '10, '11, '12, '13  '14, '15, '16, '17, '18, '19, '20
BEAR_KO = [['2', '1', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], # Bear in 0
           ['1', '_', '2', '1', '_', '_', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], # Bear in 2
           ['_', '_', '1', '_', '_', '_', '2', '_', '_', '_', '_', '_', '1', '1', '_', '_', '_', '_', '_', '_', '_'], # Bear in 6
           ['_', '_', '_', '_', '_', '_', '1', '_', '_', '_', '_', '_', '1', '2', '_', '_', '1', '_', '_', '_', '_'], # Bear in 13
           ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '1', '1', '_', '_', '2', '_', '_', '1', '_'], # Bear in 16
           ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '1', '1', '_', '2', '1'], # Bear in 19
           ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '1', '1', '1', '2'], # Bear in 20
           ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '1', '_', '_', '1', '2', '_', '1'], # Bear in 18
           ['_', '_', '_', '_', '_', '_', '_', '1', '1', '_', '_', '_', '_', '_', '2', '_', '_', '_', '1', '_', '_'], # Bear in 14
           ['_', '_', '_', '_', '1', '_', '_', '2', '1', '_', '_', '_', '_', '_', '1', '_', '_', '_', '_', '_', '_'], # Bear in 7
           ['_', '1', '_', '_', '2', '_', '_', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], # Bear in 4
           ['1', '2', '_', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], # Bear in 1
          ]
# Conditions for end of game
def is_over(game_board, bear_moves):
    if (game_board in BEAR_KO):
        print("Hunter WINS")
    if (bear_moves > MAX_BEAR_MOVES):
        print("Bear WINS")
    return ((game_board in BEAR_KO) or (bear_moves > MAX_BEAR_MOVES ))
# Return possible moves (adjacent free positiion)
def possible_moves(board, position):
    #Adjacent locations
    adjacent = [[1,2,3], #0
                [0,3,4],
                [0,3,6], #2
                [0,1,2,5],
                [1,7,8], #4
                [3,9,10,11],
                [2,12,13], #6
                [4,8,14],
                [7,4,14,9], #8
                [8, 10,5,15],
                [5,9,11,15],#10
                [5,10,15,12],
                [11,6,16,13],#12
                [6,12,16],
                [7,8,18],#14
                [9,10,11,17],
                [12,13,19], #16
                [15,18,19,20],
                [14,17,20], #18
                [16, 17, 20],
                [18, 17, 19]]
    moves = []
    #Check free positions
    for x in adjacent[position]:
        if board[x] == '_':
            moves.append(x)
    return moves
    
# Print board with pawns    
def print_board(game_board):
    # print board
    print("            "+game_board[0]+"            ","            "+"0"+"            ")
    print("        "+game_board[1]+"       "+game_board[2]+"        ","        "+"1"+"       "+"2"+"        ")
    print("            "+game_board[3]+"            ","            "+"3"+"            ")
    print("  "+game_board[4]+"         "+game_board[5]+"         "+game_board[6]+"  ","  "+"4"+"         "+"5"+"         "+"6"+"  ")
    print(""+game_board[7]+"   "+game_board[8]+"   "+game_board[9]+"   "+game_board[10]+"   "+game_board[11]+"   "+game_board[12]+"   "+game_board[13]+"",
          ""+"7"+"   "+"8"+"   "+"9"+"   "+"10"+"  "+"11"+"  "+"12"+"  "+"13"+"")
    print("  "+game_board[14]+"         "+game_board[15]+"         "+game_board[16]+"  "," "+"14"+"        "+"15"+"        "+"16"+"")
    print("            "+game_board[17]+"            ","           "+"17"+"            ")
    print("        "+game_board[18]+"       "+game_board[19]+"        ","       "+"18"+"      "+"19"+"        ")
    print("            "+game_board[20]+"            ","           "+"20"+"            ")
    
##########################################################################################################
# The game
##########################################################################################################
#MODEL
# init board
game = ['_'] * 21
# init hunter
game[0] = game[1] = game[2] = '1'
# init bear position
bear_position = 20
game[bear_position] = '2'
# Hunter starts
is_hunter_turn = True
# Bear moves counter
bear_moves = 1

# Game cycle
while not is_over(game,bear_moves):
    print_board(game)
    # Starting position
    if is_hunter_turn:
        print("Hunter is playing")
        try:
            # Must be integer
            starting_pos = int(input(" Enter position you want to pick from (0-20): \n").strip())
            # Between 0 and 20
            if starting_pos < 0 or starting_pos > 20:
                print("Number out of range")
                raise Exception
            # Belonging to hunter
            if (game[starting_pos] != '1'):
                print("Not your pawn")
                raise Exception 
        except:
            print("Please enter only valid fields from board (0-20)")
            continue
        
    else:
        print("Bear is playing move n. ",bear_moves)
        starting_pos = bear_position

    # Target position
    try:
        target_pos = int(input(" Enter target position you want to go to: \n").strip())
        if target_pos not in possible_moves(game,starting_pos):
            raise Exception
    except:
        print("Please enter only valid fields from board (0-20)")
        continue
    # Make the move
    game[starting_pos] = '_'
    if is_hunter_turn:
        game[target_pos] = '1'
    else:
        bear_moves += 1
        bear_position = target_pos
        game[target_pos] = '2'
    # Change turn
    is_hunter_turn = not is_hunter_turn

