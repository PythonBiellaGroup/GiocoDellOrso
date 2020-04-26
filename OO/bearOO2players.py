class Board():
    #init
    def __init__(self):
        self.__cells = ['_'] * 21
        self.__cells[0] = self.__cells[1] = self.__cells[2] = '1'
        # init bear position
        self.__bear_position = 20
        self.__max_bear_moves = 40
        self.__cells[self.__bear_position] = '2'
        # Hunter starts
        self.__is_hunter_turn = True
        # Bear moves counter
        self.__bear_moves = 1
        # Combinations for bear to loose, one for each edge position
        # index ease                '0,','1', '2', '3', '4', '5', '6', '7', '8', '9', '10, '11, '12, '13  '14, '15, '16, '17, '18, '19, '20
        self.__bear_ko_positions = [['2', '1', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], # Bear in 0
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
                                    ['1', '2', '_', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']] # Bear in 1
        
    #displays board in a presentable order
    def display(self):
        # print board
        print("            "+self.__cells[0]+"            ","             "+"0"+"            ")
        print("        "+self.__cells[1]+"       "+self.__cells[2]+"        ","         "+"1"+"       "+"2"+"        ")
        print("            "+self.__cells[3]+"            ","             "+"3"+"            ")
        print("  "+self.__cells[4]+"         "+self.__cells[5]+"         "+self.__cells[6]+"  ","   "+"4"+"         "+"5"+"         "+"6"+"  ")
        print(""+self.__cells[7]+"   "+self.__cells[8]+"   "+self.__cells[9]+"   "+self.__cells[10]+"   "+self.__cells[11]+"   "+self.__cells[12]+"   "+self.__cells[13]+"",
              " "+"7"+"   "+"8"+"   "+"9"+"  "+"10"+"  "+"11"+"  "+"12"+"  "+"13"+"")
        print("  "+self.__cells[14]+"         "+self.__cells[15]+"         "+self.__cells[16]+"  ","  "+"14"+"        "+"15"+"        "+"16"+"")
        print("            "+self.__cells[17]+"            ","            "+"17"+"            ")
        print("        "+self.__cells[18]+"       "+self.__cells[19]+"        ","        "+"18"+"      "+"19"+"        ")
        print("            "+self.__cells[20]+"            ","            "+"20"+"            ")

    #updates board
    def update(self, starting_position, target_position):
        self.__cells[starting_position] = '_'
        if self.__is_hunter_turn:
            self.__cells[target_position] = '1'
        else:
            self.__bear_moves += 1
            self.__bear_position = target_position
            self.__cells[target_position] = '2'
        # Change turn
        self.__is_hunter_turn = not self.__is_hunter_turn
            
    #checks all conditions for winner
    def is_winner(self):
        if (self.__cells in self.__bear_ko_positions):
            print("Hunter WINS; Bear's moves ",self.__bear_moves)
            return True
        elif (self.__bear_moves > self.__max_bear_moves):
            print("Bear WINS")            
            return True
        else:
            return False

    def is_hunter_turn(self):
        return self.__is_hunter_turn

    def get_bear_moves(self):
        return self.__bear_moves

    def get_bear_position(self):
        return self.__bear_position
        
    def get_position(self, position):
        return self.__cells[position]

    def possible_moves(self, position):
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
            if self.__cells[x] == '_':
                moves.append(x)
        return moves
    
##########################################################################################################
# The game
##########################################################################################################
#MODEL
# init board
game = Board()

# Game cycle
while not game.is_winner():
    game.display()
    # Starting position
    if game.is_hunter_turn():
        print("Hunter is playing")
        try:
            # Must be integer
            starting_pos = int(input(" Enter position you want to pick from (0-20): \n").strip())
            # Between 0 and 20
            if starting_pos < 0 or starting_pos > 20:
                print("Number out of range")
                raise Exception
            # Belonging to hunter
            if (game.get_position(starting_pos) != '1'):
                print("Not your pawn")
                raise Exception 
        except:
            print("Please enter only valid fields from board (0-20)")
            continue
        
    else:
        print("Bear is playing move n. ",game.get_bear_moves())
        starting_pos = game.get_bear_position()

    # Target position
    try:
        target_pos = int(input(" Enter target position you want to go to: \n").strip())
        if target_pos not in game.possible_moves(starting_pos):
            raise Exception
    except:
        print("Please enter only valid fields from board (0-20)")
        continue
    # Make the move
    game.update(starting_pos, target_pos)

