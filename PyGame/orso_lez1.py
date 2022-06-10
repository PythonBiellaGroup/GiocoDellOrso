'''
Versione del gioco dopo la prima lezione su PyGame
https://youtu.be/rdT_Z23YRAY
ovvero senza utilizzo di Sprites e gruppi di collisioni
'''

import pygame
import time
import sys

# Initialize pygame
pygame.init()

# Palette - RGB colors
BLACK = (0, 0, 0)

# Create the window
FINESTRA_X=1536
FINESTRA_Y=864
screen = pygame.display.set_mode((FINESTRA_X, FINESTRA_Y))
pygame.display.set_caption("Gioco dell'orso")

# set game clock
clock = pygame.time.Clock()

# Caricamento assets
# Orso e cacciatori
orso = pygame.image.load('images/little-bear.png')
orso_idle = pygame.image.load('images/little-bear-idle.png')
orso_sel = pygame.image.load('images/little-bear-sel.png')

tre_cacciatori = pygame.image.load('images/TreCacciatoriTurno.png')
cacciatoreuno = pygame.image.load('images/little-hunter1.png')
cacciatoreuno_idle = pygame.image.load('images/little-hunter1-idle.png')
cacciatoreuno_sel = pygame.image.load('images/little-hunter1-sel.png')

cacciatoredue = pygame.image.load('images/little-hunter2.png')
cacciatoredue_idle = pygame.image.load('images/little-hunter2-idle.png')
cacciatoredue_sel = pygame.image.load('images/little-hunter2-sel.png')

cacciatoretre = pygame.image.load('images/little-hunter3.png')
cacciatoretre_idle = pygame.image.load('images/little-hunter3-idle.png')
cacciatoretre_sel = pygame.image.load('images/little-hunter3-sel.png')

orma_orso = pygame.image.load('images/impronta_orso.png')
orma_cacciatore = pygame.image.load('images/impronta_cacciatore.png')

# Pannelli, controlli e immagini "messaggio"
panel = pygame.image.load('images/buttonLong.png')
panel_due = pygame.image.load('images/panel.png')

uscita = pygame.image.load('images/back.png')
uscita_rect = uscita.get_rect()
uscita_rect.center = (1355,675)

orso_vince = pygame.image.load("images/Lorso-vince.png").convert_alpha()
cacciatori_vincono = pygame.image.load("images/Vincono-i-cacciatori.png").convert_alpha()

# Scacchiera
board_img = pygame.image.load('images/board.png')
# Posizioni nella board dove posizionare le pedine
# Per controllo click sulla scacchiera
posizioni = [(730,0), (565,5), (900,5), #0,1,2
             (730,135), (350,225), (730,225), #3,4,5
             (1115,225), (315,385), (465,385), #6,7,8
             (565,385), (730,385), (900,385), #9,10,11
             (995,385), (1155,385), (350,565), #12,13,14
             (730,565), (1115,565), (730,655), #15,16,17
             (565,775), (900,775), (730,800)] #18.19.20
PIXEL_IN_ASCOLTO = 80

# Assets per menu
# grafica titolo creata con https://textcraft.net/
title = pygame.image.load("images/Gioco-dellorso.png").convert_alpha()
tred_board = pygame.image.load("images/3d_board.png")
inizia = pygame.image.load('images/buttonLong.png')
inizia_rect = inizia.get_rect()
inizia_rect.center = (1290, 720)
inizia_str = pygame.image.load("images/Inizia-a-giocare.png").convert_alpha()

esci_gioco = pygame.image.load('images/buttonLong.png')
esci_gioco_rect = esci_gioco.get_rect()
esci_gioco_rect.center = (290, 720)
esci_gioco_str = pygame.image.load("images/Esci-dal-gioco.png").convert_alpha()

# Fonts
font_due_text = pygame.font.Font('fonts/LobsterTwo-Regular.otf',30)
font_due_small = pygame.font.Font('fonts/LobsterTwo-Regular.otf',45)
font_due_big = pygame.font.Font('fonts/LobsterTwo-Regular.otf',90)

class BearBoard:
    '''
    Class for logical board and game model
    20 positions:
    _ means empty;
    1-8-9 means hunters; 
    2 means bear;
    '''
    def __init__(self, max_bear_moves: int, hunter_starts: bool):
        # Start settings
        self.reset(max_bear_moves, hunter_starts)
        
    def reset(self, max_bear_moves: int, hunter_starts: bool) -> None:
        # Start and reset settings
        self._board = ['1', '8', '9', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '2']
        self._bear_position = 20
        self._bear_moves = 0
        self._hunter_starting_pos = -1
        # From external configuration
        self._is_hunter_turn = hunter_starts        
        self._max_bear_moves = max_bear_moves 

    def get_bear_moves(self) -> int:
        '''
        Counter of bear moves
        '''
        return self._bear_moves


    def get_max_bear_moves(self) -> int:
        '''
        Max bear moves
        '''
        return self._max_bear_moves

    def get_board_position(self, position:int) -> str:
        return self._board[position]

    def get_board_length(self) -> int:
        '''
        Return the length of the board
        '''
        return len(self._board)

    def get_hunter_starting_pos(self) -> int:
        return self._hunter_starting_pos
    
    def is_bear_winner(self) -> bool:
        '''Returns the winner in a string type for display purposes'''
        if not(self.get_possible_moves(self._bear_position)):
            return False
        if (self._bear_moves >= self._max_bear_moves):
            return True

    def get_winner(self) -> str:
        '''Returns the winner in a string type for display purposes'''
        if not(self.get_possible_moves(self._bear_position)):
            return 'Hanno vinto i cacciatori!'
        if (self._bear_moves >= self._max_bear_moves):
            return "Ha vinto l'orso, congratulazioni"

    def game_over(self) -> bool:
        if ( ( not(self.get_possible_moves(self._bear_position)) ) or (self._bear_moves >= self._max_bear_moves) ):
            return True
        else:
            return False

    def is_hunter(self, selection:str) -> bool:
        return selection in ['1','8','9']

    def is_hunter_turn(self) -> bool:
        return self._is_hunter_turn

    def manage_hunter_selection(self, sel:int) -> tuple:
        '''Input selection from user; return 2 outputs: 1) message, 2) bool if board must be redrawn (not useful in PyGame)'''
        selected_hunter = ''
        # Pick up pawn (starting pos -1)
        if self._hunter_starting_pos == -1:
            if (not(self.is_hunter(self._board[sel]))):
                return ("Seleziona un cacciatore!", True)
            else:
                self._hunter_starting_pos = sel
                return ("Cacciatore, fa' la tua mossa!", True)
        else: # Finding final position for hunter
            if sel in self.get_possible_moves(self._hunter_starting_pos):
                selected_hunter = self._board[self._hunter_starting_pos]
                self._board[self._hunter_starting_pos] = '_'
                self._board[sel] = selected_hunter
                self._hunter_starting_pos = -1
                self._is_hunter_turn = not(self._is_hunter_turn)
                return ("Orso, scegli la tua mossa!", True)
            else: # Go back to picking stage
                self._hunter_starting_pos = -1
                return ("Posizione non valida!", True)
    
    def manage_bear_selection(self,sel: int) -> tuple:
        '''Input selection from user; return 2 outputs: 1) message, 2) bool if board must be redrawn (not useful in PyGame)'''
        if sel in self.get_possible_moves(self._bear_position):
            # Bear makes the move
            self._board[self._bear_position] = '_'
            self._board[sel] = '2'
            self._bear_moves += 1
            self._bear_position = sel
            self._is_hunter_turn = not(self._is_hunter_turn)
            return ("Seleziona uno dei cacciatori!", True)
        else:
            return ("Posizione non valida...", False)

    def get_possible_moves(self, position: int) -> list:
        '''Adjacent locations, index is position'''
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


def menu():
    '''
    Display main menu with PyGame
    TODO: richiedere opzioni: numero mosse, chi parte
    '''
    pygame.mixer.music.load('sounds/intro.wav')
    pygame.mixer.music.play(-1)

    screen.blit(tred_board, (0, 0))#
    screen.blit(title, (500,20))
    screen.blit(orso_idle, (250, 420))
    screen.blit(tre_cacciatori, (1200, 420))
    
    screen.blit(inizia, (1100, 680))
    screen.blit(inizia_str, (1140, 700))

    screen.blit(esci_gioco, (100, 680))
    screen.blit(esci_gioco_str, (170, 690))

    pos_call = (0, 0)
    running = True
    while running:
        pos_call = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:                
                pos_call = pygame.mouse.get_pos()
                # print(pos_call)
                # Per uscire
                if esci_gioco_rect.collidepoint(pos_call):
                    running = False
                    pygame.quit()
                    sys.exit()

                # Per iniziare il gioco
                if inizia_rect.collidepoint(pos_call):
                    running = False
                    pygame.time.delay(800)
                    # fade out menu music
                    pygame.mixer.music.fadeout(800)
                    game(30, True)

        pygame.display.update()



def game(numero_mosse: int, inizia_cacciatore: bool):
    '''
    Gioco implementato con PyGame
    '''
    pygame.mixer.music.load('sounds/orso_music.ogg')
    pygame.mixer.music.play(-1)

    # Inizializza la scacchiera e il gioco
    bear_board = BearBoard(numero_mosse, inizia_cacciatore)
    msg = "L'orso vince facendo "+str(bear_board.get_max_bear_moves())+" mosse"
    
    # Inizializzazioni
    running = True
    pos_call = (0, 0)
    selezione = None   
    # show non usata, var per decidere se serve o no ridisegnare lo schermo
    show = True

    while running:
        #pos_call = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_call = pygame.mouse.get_pos()
                # print(pos_call)
                # Verifica se click su freccia per uscita
                if uscita_rect.collidepoint(pos_call):
                    running = False
                    pygame.mixer.music.stop()
                    menu()
                    #bear_board.reset(numero_mosse, inizia_cacciatore)
                    
                # Verifica se c'è stato click in una posizione della scacchiera
                for pos in range(0,len(posizioni)):
                    if ( (pos_call[0] <= posizioni[pos][0]+PIXEL_IN_ASCOLTO) and 
                        (pos_call[0] >= posizioni[pos][0]) and 
                        (pos_call[1] <= posizioni[pos][1]+PIXEL_IN_ASCOLTO) and 
                        (pos_call[1] >= posizioni[pos][1]) ):
                        selezione = pos
                        # Controlla e aggiorna gli spostamenti nella scacchiera
                        # Se click in posizione non corretta, ritorna solo un messaggio
                        if (bear_board.is_hunter_turn()):
                            msg, show = bear_board.manage_hunter_selection(pos)
                        else:
                            msg, show = bear_board.manage_bear_selection(pos)
    
        # Debug 
        #string = font.render("pos_call = " + str(pos_call), 1, BLACK)
        clock.tick(60)
        # Disegna la scacchiera
        screen.blit(board_img, (0, 0))

        # Pannello mosse orso
        mosse_str = font_due_small.render("Mosse orso", 1, BLACK)
        mosse = font_due_big.render(str(bear_board.get_bear_moves()), 1, BLACK)    
        screen.blit(panel_due, (80, 80))  
        screen.blit(mosse_str, (90, 90))  
        screen.blit(mosse, (145, 140))    

        # Pannello turno
        screen.blit(panel_due, (1250, 80))
        turno_str = font_due_small.render("Turno", 1, BLACK)
        screen.blit(turno_str, (1300, 90))
        if not bear_board.is_hunter_turn():
            screen.blit(orso_sel, (1320, 160))
        else:
            screen.blit(tre_cacciatori, (1265, 160))

        # Pannello uscita
        screen.blit(uscita, (1250, 580))
    
        # Disegna la pedine
        bl = bear_board.get_board_length()
        for i in range (0,bl):
            if bear_board.get_board_position(i) == '2':
                if not bear_board.is_hunter_turn():
                    screen.blit(orso_sel, posizioni[i])
                    # Visualizza orme
                    for j in range (0,bl):
                        if j in bear_board.get_possible_moves(i):
                            screen.blit(orma_orso, posizioni[j])
                else:
                    screen.blit(orso, posizioni[i])
            # Disegna i 3 cacciatori
            if bear_board.get_board_position(i) == '1':
                if (bear_board.get_hunter_starting_pos() == i):
                    screen.blit(cacciatoreuno_sel, posizioni[i])
                    # Visualizza orme
                    for j in range (0,bl):
                        if j in bear_board.get_possible_moves(i):
                            screen.blit(orma_cacciatore, posizioni[j])
                else:
                    if bear_board.is_hunter_turn():
                        screen.blit(cacciatoreuno, posizioni[i])
                    else:
                        screen.blit(cacciatoreuno_idle, posizioni[i])
            if bear_board.get_board_position(i) == '8':
                if (bear_board.get_hunter_starting_pos() == i):
                    screen.blit(cacciatoredue_sel, posizioni[i])
                    # Visualizza orme
                    for j in range (0,bl):
                        if j in bear_board.get_possible_moves(i):
                            screen.blit(orma_cacciatore, posizioni[j])
                else:
                    if bear_board.is_hunter_turn():
                        screen.blit(cacciatoredue, posizioni[i])
                    else:
                        screen.blit(cacciatoredue_idle, posizioni[i])
            if bear_board.get_board_position(i) == '9':
                if (bear_board.get_hunter_starting_pos() == i):
                    screen.blit(cacciatoretre_sel, posizioni[i])
                    # Visualizza orme
                    for j in range (0, bl):
                        if j in bear_board.get_possible_moves(i):
                            screen.blit(orma_cacciatore, posizioni[j])
                else:
                    if bear_board.is_hunter_turn():
                        screen.blit(cacciatoretre, posizioni[i])
                    else:
                        screen.blit(cacciatoretre_idle, posizioni[i])
        # Check fine del gioco
        if bear_board.game_over():
            msg = bear_board.get_winner()
            if bear_board.is_bear_winner():
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/orso_ride.wav'))
                screen.blit(orso_vince, (580,380))            
                
            else:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/cacciatori_ridono.wav'))
                screen.blit(cacciatori_vincono, (480,380))            

        # Pannello messaggi
        text = font_due_text.render(msg, 1, BLACK)            
        screen.blit(panel, (40, 680))
        screen.blit(text, (50,705))

        # Aggiornamento screen
        pygame.display.update()

        # Reset del gioco
        if bear_board.game_over():
            time.sleep(5)
            # Si inverte chi inizia
            inizia_cacciatore = not(inizia_cacciatore)
            if inizia_cacciatore:
                msg = "Ricominciano i cacciatori"
            else:
                msg = "Ricomincia l'orso"
            bear_board.reset(numero_mosse, inizia_cacciatore)

# Main
if __name__ == "__main__":
    # Il gioco è richiamato da menu
    menu()