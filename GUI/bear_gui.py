import tkinter
from time import sleep

# Functions found on Internet (stackoverflow) to draw circles and arcs
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tkinter.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tkinter.Canvas.create_circle_arc = _create_circle_arc
# End of functions found on Internet (stackoverflow) to draw circles and arcs

###########
# Classes #
###########
class BearBoard:
    '''Class for logical board (20 positions where _ means empty;1 means hunter; 2 means bear; with game model'''
    def __init__(self, max_bear_moves: int, hunter_starts: bool):
        # Start settings
        self.reset(max_bear_moves, hunter_starts)
        
    def reset(self, max_bear_moves: int, hunter_starts: bool) -> None:
        # Start and reset settings
        self._board = ['1', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '2']
        self._bear_position = 20
        self._bear_moves = 1
        self._hunter_starting_pos = -1
        # From external configuration
        self._is_hunter_turn = hunter_starts        
        self._max_bear_moves = max_bear_moves 

    def get_bear_moves(self) -> int:
        return self._bear_moves

    def get_hunter_starting_pos(self) -> int:
        return self._hunter_starting_pos
    
    def get_winner(self) -> str:
        '''Returns the winner in a string type for display purposes'''
        if not(self.get_possible_moves(self._bear_position)):
            return 'HUNTER'
        if (self._bear_moves > self._max_bear_moves):
            return 'BEAR'

    def game_over(self) -> bool:
        if ( ( not(self.get_possible_moves(self._bear_position)) ) or (self._bear_moves > self._max_bear_moves) ):
            return True
        else:
            return False  

    def manage_hunter_selection(self, sel:int) -> tuple:
        '''Input selection from user; return 2 outputs: 1) message, 2) bool if board must be redrawn'''
        # Pick up pawn (starting pos -1)
        if self._hunter_starting_pos == -1:                    
            if (self._board[sel] != '1'):
                return (str(sel) + " is not an HUNTER", True)
            else:
                self._hunter_starting_pos = sel
                return ('Hunter picked up pawn at position '+str(sel)+"\nNow has to choose target position!", True)
        else: # Finding final position for hunter
            if sel in self.get_possible_moves(self._hunter_starting_pos):
                self._board[self._hunter_starting_pos] = '_'
                self._board[sel] = '1'
                self._hunter_starting_pos = -1
                self._is_hunter_turn = not(self._is_hunter_turn)
                return ('Hunter choose '+str(sel)+"\nIs BEAR turn n. "+str(self._bear_moves)+", choose target!", True)
            else: # Go back to picking stage
                self._hunter_starting_pos = -1
                return ("Hunter clicked in a not valid position.\nIs HUNTER turn again, pick a pawn!", True)
    
    def manage_bear_selection(self,sel: int) -> tuple:
        '''Input selection from user; return 2 outputs: 1) message, 2) bool if board must be redrawn, 3) bool if turn is changed'''    
        if sel in self.get_possible_moves(self._bear_position):
            # Bear makes the move
            self._board[self._bear_position] = '_'
            self._board[sel] = '2'
            self._bear_moves += 1
            self._bear_position = sel
            self._is_hunter_turn = not(self._is_hunter_turn)
            return ('Bear choose '+str(sel)+"\nIs HUNTER turn, pick a pawn!", True)
        else:
            return ("BEAR clicked in a not valid position.\nIs BEAR turn n. "+str(self._bear_moves)+", choose target!", False)

    def get_possible_moves(self, position: int) -> list:
        # Adjacent locations, index is position
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
            if self._board[x] == '_':
                moves.append(x)
        return moves
       
# Option GUI window class
class BearInputs:
    def __init__(self):
        ''' Creates the entire game options window'''
        self._menu_window = tkinter.Tk()
        title = tkinter.Label(master = self._menu_window, text = 'BEAR''S GAME OPTIONS', font = ('Helvetica', 15, 'bold'))
        title.grid(row = 0, column = 0, columnspan = 2)
        
        self._default_font = ('Helvetica', 12)

        #Add elements
        self.first_turn()
        self.max_bear_moves()
        self.board_color()
        self.board_size()
        button_frame = tkinter.Frame(master = self._menu_window)
        button_frame.grid(
            row = 5, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.S)
        ok_button = tkinter.Button(
            master = button_frame, text = 'OK', font = self._default_font, 
            command = self._on_ok_button)
        ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)
        self._menu_window.rowconfigure(5, weight = 1)
        self._menu_window.columnconfigure(1, weight = 1)
        self._menu_window.wm_title("Bear's game options (by Burlesco)")
        self._menu_window.mainloop()

    def get_board_size(self) -> str:
        return self._board_size

    def get_board_color(self) -> str:
        return self._board_color

    def get_first_turn(self) -> str:
        return self._first_turn

    def get_max_bear_moves(self) -> str:
        return self._max_bear_moves

    def _on_ok_button(self) -> None:
        '''Assigns new variables to all the variables that are in each option and destroys the menu window'''
        self._first_turn = self._first_turn_variable.get()
        self._max_bear_moves = self._max_bear_moves_variable.get()
        self._board_size = self._board_size_variable.get()
        self._board_color = self._board_color_variable.get()
        self._menu_window.destroy()

    def board_size(self) -> None:
        board_size_label = tkinter.Label(
            master = self._menu_window, text = 'Board Size (x1, x1.5, x2):',
            font = self._default_font)
            
        board_size_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._board_size_variable = tkinter.StringVar()
        self._board_size_variable.set('x1')
        self._board_size_menu = tkinter.OptionMenu(self._menu_window, self._board_size_variable, 'x1','x1.5','x2')
        self._board_size_menu.grid(
            row = 1, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E) 
            
    def board_color(self) -> None:
        board_color_label = tkinter.Label(
            master = self._menu_window, text = 'Board Color (green, gray, blue):',
            font = self._default_font)
            
        board_color_label.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._board_color_variable = tkinter.StringVar()
        self._board_color_variable.set('LIME GREEN')
        self._board_color_menu = tkinter.OptionMenu(self._menu_window, self._board_color_variable, 'LIME GREEN','SEASHELL4','SKY BLUE')
        self._board_color_menu.grid(
            row = 2, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)          
        
    def first_turn(self) -> None:
        first_turn_label = tkinter.Label(
            master = self._menu_window, text = 'First turn (Hunter or Bear):',
            font = self._default_font)
            
        first_turn_label.grid(
            row = 3, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._first_turn_variable = tkinter.StringVar()
        self._first_turn_variable.set('H')
        self._first_turn_menu = tkinter.OptionMenu(self._menu_window, self._first_turn_variable, 'H','B')
        self._first_turn_menu.grid(
            row = 3, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E) 

    def max_bear_moves(self)-> None:
        '''Creates the winning rules option'''
        max_bear_moves_label = tkinter.Label(
            master = self._menu_window, text = 'Max moves for Bear:',
            font = self._default_font)
        max_bear_moves_label.grid(
            row = 4, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._max_bear_moves_variable = tkinter.StringVar()
        self._max_bear_moves_variable.set('40')
        self._max_bear_moves_menu = tkinter.OptionMenu(self._menu_window, self._max_bear_moves_variable, '40', '30', '20')
        
        self._max_bear_moves_menu.grid(
            row = 4, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E) 

# Main GUI game class
class BearGUI:
    def __init__(self):
    
        # First page
        self._BearInputs = BearInputs()
        
        # Options from first page
        # Background board color
        self._board_color = self._BearInputs.get_board_color()
        # Get choosen size and set graphic attributes
        self._board_size = self._BearInputs.get_board_size()
        # Who starts
        self._is_hunter_starting = ( self._BearInputs.get_first_turn() == 'H' )
        # Max bear moves to win
        self._max_bear_moves = int(self._BearInputs.get_max_bear_moves())
        
        #Size and resize management        
        self._board_center=250
        self._main_circle_radius=200
        if (self._board_size == 'x1.5'): # Original
            self._board_center = 1.5 * self._board_center
            self._main_circle_radius = 1.5 * self._main_circle_radius
        elif (self._board_size == 'x2'): #x1.5
            self._board_center = 2 * self._board_center
            self._main_circle_radius = 2 * self._main_circle_radius
        # Derived variables to create the board
        # Square side around positions for click listener
        self._pixel_area_listened = self._main_circle_radius / 10
        self._board_side = 2 * self._board_center
        # Define the 20 positions in the board
        self._pos0 = ( self._board_center, int(self._board_center/5) ) # 0
        self._pos1 = ( int(self._board_side/10 + self._board_center/2), int((self._main_circle_radius/10) + (self._board_center/5)) ) # 1
        self._pos2 = ( int(self._main_circle_radius + self._board_center/2), int((self._main_circle_radius/10) + (self._board_center/5)) ) # 2
        self._pos3 = ( self._board_center, int(self._board_center/2) ) # 3
        self._pos4 = ( int((self._main_circle_radius/10) + (self._board_center/5)), int(self._board_side/10 + self._board_center/2) ) # 4
        self._pos5 = ( self._board_center, int(self._board_side/10 + self._board_center/2)) # 5
        self._pos6 = ( int(self._board_side - self._main_circle_radius + self._board_center/2), int(self._board_side/10 + self._board_center/2)) # 6
        self._pos7 = ( int(self._board_center/5), self._board_center) # 7
        self._pos8 = ( int(self._board_center/2), self._board_center) # 8
        self._pos9 = ( int(self._board_side/10 + self._board_center/2), self._board_center) # 9
        self._pos10 = ( self._board_center, self._board_center) # 10
        self._pos11 = ( int(self._main_circle_radius + self._board_center/2), self._board_center) # 11
        self._pos12 = ( int(self._board_center + self._board_center/2), self._board_center) # 12
        self._pos13 = ( int(self._board_side - self._board_center/5), self._board_center) # 13
        self._pos14 = ( int((self._main_circle_radius/10) + (self._board_center/5)), int(self._main_circle_radius + self._board_center/2)) # 14
        self._pos15 = ( self._board_center, int(self._main_circle_radius + self._board_center/2)) # 15
        self._pos16 = ( int(self._board_side - self._main_circle_radius + self._board_center/2), int(self._main_circle_radius + self._board_center/2)) # 16)
        self._pos17 = ( self._board_center, int(self._board_center + self._board_center/2)) # 17
        self._pos18 = ( int(self._board_side/10 + self._board_center/2), int(self._board_side - self._main_circle_radius + self._board_center/2)) # 18
        self._pos19 = ( int(self._main_circle_radius + self._board_center/2), int(self._board_side - self._main_circle_radius + self._board_center/2)) # 19
        self._pos20 = ( self._board_center, int(self._board_side - (self._board_center/5))) # 20              
        
        self._positions = [ self._pos0, self._pos1, self._pos2, self._pos3, self._pos4, 
                            self._pos5, self._pos6, self._pos7, self._pos8, self._pos9,
                            self._pos10, self._pos11, self._pos12, self._pos13, self._pos14, 
                            self._pos15, self._pos16, self._pos17, self._pos18, self._pos19, self._pos20 ]        
        # Options end

        # Board object creation and settings
        self.bear_board = BearBoard(self._max_bear_moves, self._is_hunter_starting)
        
        # Graphic settings
        self._default_font = ('Helvetica', 12)
        self._line_width=2
        self._line_color="white"

        # Main GUI
        self._root_window = tkinter.Tk()
        self._root_window.resizable(0, 0)
        self._root_window.wm_title("Bear's game - by Burlesco (PythonGroupBiella)")
        
        # Message board section
        self._game_status = tkinter.StringVar()
        self._status = tkinter.Label(
            master = self._root_window,
            width = 30, height = 3, textvariable = self._game_status, font = self._default_font)
        self._status.grid(row = 0, column = 0)
        
        # Board section
        self._canvas = tkinter.Canvas(master=self._root_window, width=self._board_side, height=self._board_side, borderwidth=0, highlightthickness=0, bg=self._board_color)
        self._canvas.grid(row = 1, column = 0)
        # Load images for pawns
        self._bear_img = tkinter.PhotoImage(file='little-bear.png')
        self._hunter_img = tkinter.PhotoImage(file='little-hunter.png')
        self._selbear_img = tkinter.PhotoImage(file='little-bear-sel.png')
        self._selhunter_img = tkinter.PhotoImage(file='little-hunter-sel.png')
        
        # Method on-click to manage the game
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        
        # Message to start
        if (self.bear_board._is_hunter_turn):
            self._game_status.set("Hunter choose first\nIs HUNTER turn, pick a pawn!")
        else:
            self._game_status.set("Bear choose first\nIs BEAR turn n. "+str(self.bear_board._bear_moves)+", choose target!")
        self._redraw_game_board()

    def start(self) -> None:
        '''Starts the Bear game'''
        self._root_window.mainloop()
        
    def _redraw_game_board(self) -> None:
        '''(Re)draws the entire gameboard: circles and lines.
        Basing on board state, turn and selections, put images'''
        _background = self._board_color
        self._canvas.delete(tkinter.ALL)
        # Board graphics: circles and lunettes
        self._canvas.create_circle(self._board_center, self._board_center, (self._board_side - self._main_circle_radius)/4, 
                                   fill=_background, outline=self._line_color, width=self._line_width)
        # Lunettes with half circles (wiht deletions when outline=_background)
        # 9 o'clock
        _x = int(self._main_circle_radius/4)
        _y = self._board_center
        _z = int((self._board_side - self._main_circle_radius)/4)
        self._canvas.create_circle( _x, _y, _z, fill=_background, outline=self._line_color, width=self._line_width)
        self._canvas.create_circle_arc((self._main_circle_radius / 4), self._board_center, (self._board_side - self._main_circle_radius)/4, 
                                      fill=_background, outline=_background, start=+280, end=-280, width=self._line_width)

        # 12 o'clock
        self._canvas.create_circle(self._board_center, (self._main_circle_radius / 4), (self._board_side - self._main_circle_radius)/4,
                                   fill=_background, outline=self._line_color, width=self._line_width)
        self._canvas.create_circle_arc(self._board_center, (self._main_circle_radius / 4), (self._board_side - self._main_circle_radius)/4,
                                       fill=_background, outline=_background, start=-170, end=-370, width=self._line_width)
        # 6 o'clock
        self._canvas.create_circle(self._board_center, self._board_side - (self._main_circle_radius / 4), (self._board_side - self._main_circle_radius)/4,
                                   fill=_background, outline=self._line_color, width=self._line_width)
        self._canvas.create_circle_arc(self._board_center, self._board_side - (self._main_circle_radius / 4), (self._board_side - self._main_circle_radius)/4,
                                       fill=_background, outline=_background, start=-190, end=10, width=self._line_width)
        # 3 o'clock
        self._canvas.create_circle(self._board_side - (self._main_circle_radius / 4), self._board_center, (self._board_side - self._main_circle_radius)/4,
                                   fill=_background, outline=self._line_color, width=self._line_width)
        self._canvas.create_circle_arc(self._board_side - (self._main_circle_radius / 4), self._board_center, (self._board_side - self._main_circle_radius)/4,
                                       fill=_background, outline=_background, start=-100, end=+100, width=self._line_width)
        # Lins
        self._canvas.create_line((self._main_circle_radius / 4), self._board_center, self._board_side - (self._main_circle_radius / 4), self._board_center,
                                 fill=self._line_color, width=self._line_width)
        self._canvas.create_line(self._board_center, (self._main_circle_radius / 4), self._board_center, self._board_side - (self._main_circle_radius / 4),
                                 fill=self._line_color, width=self._line_width)
        # Big circle not filled
        self._canvas.create_circle(self._board_center, self._board_center, self._main_circle_radius,
                                   outline=self._line_color, width=self._line_width)
        # Draw bear and hunters basing on board state
        for i in range (0,len(self.bear_board._board)):
            self._canvas.create_text(self._positions[i][0]-10, self._positions[i][1]-10, text=str(i))#, fill=self._line_color)
            if self.bear_board._board[i] == '2':
                if not self.bear_board._is_hunter_turn:
                    self._canvas.create_image(self._positions[i][0], self._positions[i][1], image=self._selbear_img)
                else:
                    self._canvas.create_image(self._positions[i][0], self._positions[i][1], image=self._bear_img)
            if self.bear_board._board[i] == '1':
                if (self.bear_board.get_hunter_starting_pos() == i):
                    self._canvas.create_image(self._positions[i][0], self._positions[i][1], image=self._selhunter_img)
                else:
                    self._canvas.create_image(self._positions[i][0], self._positions[i][1], image=self._hunter_img)
        
    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        '''Handles where the user clicks inside the game window. 
        Takes where they clicked and converts its pixels into position.
        This is the core of the game'''
        _pixel_area_listened = self._pixel_area_listened
        for pos in range(0,len(self._positions)):
            # Check if click is near (square of _pixel_area_listened) to one of board positions
            if ( (event.x <= self._positions[pos][0]+_pixel_area_listened) and 
                 (event.x >= self._positions[pos][0]-_pixel_area_listened) and 
                (event.y <= self._positions[pos][1]+_pixel_area_listened) and 
                (event.y >= self._positions[pos][1]-_pixel_area_listened) ):
                # A valid position in canvas has been found
                # Hunter turn
                if (self.bear_board._is_hunter_turn):
                    msg, show = self.bear_board.manage_hunter_selection(pos)
                else:
                    msg, show = self.bear_board.manage_bear_selection(pos)
                self._game_status.set(msg)
                if show:
                    self._redraw_game_board()
        # Check for winner
        if self.bear_board.game_over():
            # Managing restart reset and reset
            self._is_hunter_starting = not(self._is_hunter_starting)
            restart = ""
            if (self._is_hunter_starting):
                restart = "hunter restarts"
            else:
                restart = "bear restarts"
            self._game_status.set('-----GAME OVER-----\nWINNER is:  {} '.format(self.bear_board.get_winner())+"\n Now exchanged roles: "+restart)
            self.bear_board.reset(self._max_bear_moves, self._is_hunter_starting )
            self._redraw_game_board()
        return None
            
###########
# Run GUI #
###########

if __name__ == '__main__':
    try:
        BearGUI().start()
    except:
        pass