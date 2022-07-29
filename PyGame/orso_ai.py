from json.encoder import INFINITY
import pygame
import time
import sys
import functools
import pickle
# Palette - RGB colors
BLACK = (0, 0, 0)
IS_AI_HUNTER_PLAYING = False 
IS_AI_BEAR_PLAYING = True
BEAR_WINS = 1
HUNTER_WINS = 2
INFINITY = 1000000

class BearGame:
    '''
    PyGame independent game class
    Class for logical board and game model
    20 positions:
    _ means empty;
    1-8-9 means hunters; 
    2 means bear;
    '''

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
        self._winner = None 
        self._last_move = None
        self._bear_player = Player("orso") 
        self._bear_player.load_policy("bear_v2.policy")

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

    def get_winner_display(self) -> str:
        '''Returns the winner in a string type for display purposes'''
        if self._winner == HUNTER_WINS:
            return 'Hanno vinto i cacciatori!'
        if self._winner == BEAR_WINS:
            return "Ha vinto l'orso, congratulazioni"

    def game_over(self) -> bool:
        if not self.get_possible_moves(self._bear_position):
            self._winner = HUNTER_WINS
            return True
        elif (self._bear_moves > self._max_bear_moves):
            self._winner = BEAR_WINS
            return True
        else:
            return False

    def get_winner(self):
        return self._winner

    def get_hash(self) -> str:
        '''
        Return a hash of the board
        '''
        board = self._board.copy()
        # normalize the hunter ids 
        for i in range(len(board)):
            if board[i] == '8' or board[i] == '9':
                board[i] = '1'  
        return ''.join(board)

    
    def get_bear_actions(self) -> list[(int, int)]:
        actions = [] 
        for adj in BearGame.adjacent[self._bear_position]:
            if self._board[adj] == '_':
                actions.append((self._bear_position, adj))
        return actions

    def get_hunter_actions(self) -> list[(int, int)]:
        actions = [] 
        for pos in self.get_hunter_positions():
            for adj in BearGame.adjacent[pos]:
                if self._board[adj] == '_':
                    actions.append((pos, adj))
        return actions

    def is_hunter(self, selection:str) -> bool:
        return selection in ['1','8','9']

    def is_hunter_turn(self) -> bool:
        return self._is_hunter_turn


    def undo_move(self):
        self._is_hunter_turn = not self._is_hunter_turn
        target_position, starting_position = self._last_move # contrario!
        self._board[starting_position] = '_'
        if self._is_hunter_turn:
            self._board[target_position] = '1'
        else:
            self._bear_moves -= 1
            self._bear_position = target_position
            self._board[target_position] = '2'
        self._last_move = None 

    def move_hunter(self, start_position: int, final_position: int):
        '''
        Move hunter to final position
        '''
        self._last_move = (start_position, final_position)
        if (final_position in self.get_possible_moves(start_position)):
            selected_hunter = self._board[self._hunter_starting_pos]
            self._board[start_position] = '_'
            self._board[final_position] = selected_hunter

            self._hunter_starting_pos = -1
            self._is_hunter_turn = not self._is_hunter_turn
        else: # Go back to picking stage
            self._hunter_starting_pos = -1
            raise ValueError("Posizione non valida")

    def manage_hunter_selection(self, sel:int) -> str:
        '''Input selection from user; return user message to display'''
        # Pick up pawn (starting pos -1)
        if self._hunter_starting_pos == -1:
            if (not(self.is_hunter(self._board[sel]))):
                return "Seleziona un cacciatore!"
            else:
                self._hunter_starting_pos = sel
                return "Cacciatore, fa' la tua mossa!"
        else: # Finding final position for hunter
            try:
                self.move_hunter(self._hunter_starting_pos, sel)
            except ValueError as e:
                return str(e)
            return "Orso, scegli la tua mossa!"
    
    def move_bear(self, new_position: int) -> None:
        '''
        Move bear to a random position
        '''
        self._last_move = (self._bear_position, new_position)
        if new_position in self.get_possible_moves(self._bear_position):
            self._board[self._bear_position] = '_'
            self._board[new_position] = '2'
            self._bear_position = new_position
            self._bear_moves += 1
            self._is_hunter_turn = not self._is_hunter_turn
        else:
            print(self._last_move)
            raise ValueError("Orso non può muoversi qui!")

    def move_player(self, start_pos, end_pos) -> str:
        '''
        Move player to a random position
        '''
        if self._is_hunter_turn:
            return self.move_hunter(start_pos, end_pos)
        else:
            return self.move_bear(end_pos)

    def manage_bear_selection(self, sel: int) -> str:
        '''Input selection from user; return user message to display'''
        try: 
            self.move_bear(sel)
        except ValueError:
            return "Orso non può muoversi qui!"
        return "Seleziona uno dei cacciatori!"
    
    def manage_ai_bear_selection(self) -> str:
        bear_actions = self.get_bear_actions()
        action = self._bear_player.get_action(bear_actions, self)
        self.move_bear(action[1])
        return "AI ha mosso!!!"

    def display(self):
        # print board
        print("            "+self._board[0]+"            ","             "+"0"+"            ")
        print("        "+self._board[1]+"       "+self._board[2]+"        ","         "+"1"+"       "+"2"+"        ")
        print("            "+self._board[3]+"            ","             "+"3"+"            ")
        print("  "+self._board[4]+"         "+self._board[5]+"         "+self._board[6]+"  ","   "+"4"+"         "+"5"+"         "+"6"+"  ")
        print(""+self._board[7]+"   "+self._board[8]+"   "+self._board[9]+"   "+self._board[10]+"   "+self._board[11]+"   "+self._board[12]+"   "+self._board[13]+"",
              " "+"7"+"   "+"8"+"   "+"9"+"  "+"10"+"  "+"11"+"  "+"12"+"  "+"13"+"")
        print("  "+self._board[14]+"         "+self._board[15]+"         "+self._board[16]+"  ","  "+"14"+"        "+"15"+"        "+"16"+"")
        print("            "+self._board[17]+"            ","            "+"17"+"            ")
        print("        "+self._board[18]+"       "+self._board[19]+"        ","        "+"18"+"      "+"19"+"        ")
        print("            "+self._board[20]+"            ","            "+"20"+"            ")


    def set_is_hunter_turn(self, is_hunter_turn: bool) -> None:
        self._is_hunter_turn = is_hunter_turn

    def get_hunter_positions(self) -> list:
        return [i for i, x in enumerate(self._board) if x == '1' or x == '8' or x == '9']

    def sub_bear_moves(self, moves: int) -> None:
        self._bear_moves -= moves

    def set_winner(self, winner: int) -> None:
        self._winner = winner

    
    def get_position(self, pos: int) -> str:
        return self._board[pos]

    def is_footprint_and_type(self, sel:int) -> tuple:
        '''
        Return a tuple:
        - if is a footprint
        - footprint type (HUNTER|BEAR), None if is not a footprint
        '''
        if self._is_hunter_turn:
            if self._hunter_starting_pos == -1:
                return (False, None)
            else:
                if sel in self.get_possible_moves(self._hunter_starting_pos):
                    return (True, "HUNTER")
                else:
                    return (False, None)
        else:
            if sel in self.get_possible_moves(self._bear_position):
                return (True, "BEAR")
            else:
                return (False, None)

    def get_possible_moves(self, position: int) -> list:
        moves = []
        #Check free positions
        for x in BearGame.adjacent[position]:
            if self._board[x] == '_':
                moves.append(x)
        return moves

    def get_bear_position(self) -> int:
        return self._bear_position

# Metodo per ottimizzare il caricamento degli assets
# "lru_cache" decorator saves recent images into memory for fast retrieval.
@functools.lru_cache()
def get_img(path):
    return pygame.image.load(path)

@functools.lru_cache()
def get_img_alpha(path):
    return pygame.image.load(path).convert_alpha()

class OrsoPyGame():
    # Create the window
    FINESTRA_X=1536
    FINESTRA_Y=864
    DIM_CASELLA = 80

    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((OrsoPyGame.FINESTRA_X, OrsoPyGame.FINESTRA_Y))
        pygame.display.set_caption("Gioco dell'orso")
        # set game clock
        self.clock = pygame.time.Clock()
        self._load_assets_menu()
        self._load_assets_game()
        # Gestione caselle: posizione e gruppo sprite
        self._caselle = [(730,0), (565,5), (900,5), #0,1,2
                    (730,135), (350,225), (730,225), #3,4,5
                    (1115,225), (315,385), (465,385), #6,7,8
                    (565,385), (730,385), (900,385), #9,10,11
                    (995,385), (1155,385), (350,565), #12,13,14
                    (730,565), (1115,565), (730,655), #15,16,17
                    (565,775), (900,775), (730,800)] #18.19.20
        # Creazione gruppo caselle
        self._lista_caselle = pygame.sprite.Group()
        for i,p in enumerate(self._caselle):
            #print(i,p)
            pos = CasellaGiocoOrso(i, self)
            # Definisco rect ma non image
            pos.rect = pygame.Rect(p[0],p[1], OrsoPyGame.DIM_CASELLA, OrsoPyGame.DIM_CASELLA)
            self._lista_caselle.add(pos)

    def _load_assets_game(self):
        '''Caricamento assets del gioco'''
        self.USCITA_IMG = get_img('images/back.png')
        self.USCITA_RECT = self.USCITA_IMG.get_rect()
        self.USCITA_RECT.center = (1355,675)
        self.ORSO_VINCE = get_img_alpha("images/Lorso-vince.png")
        self.CACCIATORI_VINCONO = get_img_alpha("images/Vincono-i-cacciatori.png")
        # Scacchiera
        self.BOARD_IMG = get_img('images/board.png')

    def _load_assets_menu(self):
        '''Caricamento assets menu'''
        # grafica titolo creata con https://textcraft.net/
        self.ORSO_IDLE_IMG = get_img('images/little-bear-idle.png')
        self.TRE_CACCIATORI_IMG = get_img('images/TreCacciatoriTurno.png')

        self.TITOLO = get_img_alpha("images/Gioco-dellorso.png")
        self.MENU_BACKGROUND = get_img("images/3d_board.png")

    def menu(self):
        '''
        Display main menu with PyGame
        TODO: richiedere opzioni: numero mosse, chi parte
        '''
        pygame.mixer.music.load('sounds/intro.wav')
        pygame.mixer.music.play(-1)

        # Elementi di sfondo
        self.screen.blit(self.MENU_BACKGROUND, (0, 0))#
        self.screen.blit(self.TITOLO, (500,20))
        self.screen.blit(self.ORSO_IDLE_IMG, (250, 420))
        self.screen.blit(self.TRE_CACCIATORI_IMG, (1200, 420))
        
        # Creo gruppo sprite per menu
        self._menu_items = pygame.sprite.Group()
        self._m_inizio = OpzioneMenuInizioGioco(self)
        self._menu_items.add(self._m_inizio)
        self._m_uscita = OpzioneMenuUscita(self)
        self._menu_items.add(self._m_uscita)
        self.OPZIONI_MOSSE = {
            20:'Partita veloce (20 mosse)',
            30:'Partita standard (30 mosse)',
            40:'Partita classica (40 mosse)'
        }
        self._m_mosse = OpzioneMenuNumeroMosse(self.OPZIONI_MOSSE, 30, self, (580,395))
        self._menu_items.add(self._m_mosse)
        self.OPZIONI_TURNO = {
            True:'Iniziano i cacciatori',
            False:"Inizia l'orso"
            }
        self._m_inizia_cacciatore = OpzioneMenuInizoTurno(self.OPZIONI_TURNO, True, self, (580,485))            
        self._menu_items.add(self._m_inizia_cacciatore)

        self._pos_call = (0, 0)
        self._running = True
        while self._running:
            self._pos_call = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    self._quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:                
                    self._pos_call = pygame.mouse.get_pos()
                    for m_item in self._menu_items:
                        if m_item.rect.collidepoint(self._pos_call):
                            m_item.action()
            # Aggiorna gli items di menu
            self._menu_items.update()
            self._menu_items.draw(self.screen)
            # Aggiorna lo screen
            pygame.display.update()

    def _quit(self):
        '''Uscita dal gioco'''
        pygame.time.delay(500)
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

    def _menu_call(self):
        '''Richiamo menu'''
        pygame.time.delay(500)
        pygame.mixer.music.fadeout(500)
        self.menu()

    def game(self, numero_mosse: int, inizia_cacciatore: bool):
        '''Gioco implementato con PyGame'''
        pygame.mixer.music.load('sounds/orso_music.ogg')
        pygame.mixer.music.play(-1)
        # Inizializza la scacchiera e il gioco
        self.gioco_orso = BearGame(numero_mosse, inizia_cacciatore)
        self._msg = "L'orso vince facendo "+str(self.gioco_orso.get_max_bear_moves())+" mosse"
         # Creazione gruppo elementi di HUD
        self._hud = pygame.sprite.Group()
        self._h_turno = HudTurno(self)
        self._h_mosse = HudMosseOrso(self)
        self._h_msg = HudMessaggi(self)        
        self._hud.add(self._h_turno)
        self._hud.add(self._h_mosse)
        self._hud.add(self._h_msg)       
        # Inizializzazioni
        self._running = True
        self._pos_call = (0, 0)
        self._selezione = None   
        while self._running:
            #self._pos_call = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    self._menu_call()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._pos_call = pygame.mouse.get_pos()
                    # Verifica se click su freccia per uscita
                    if self.USCITA_RECT.collidepoint(self._pos_call):
                        self._running = False
                        self._menu_call()
                    # Controlla click nelle caselle
                    for casella_cliccata in self._lista_caselle:
                        if casella_cliccata.rect.collidepoint(self._pos_call):
                            self._selezione = casella_cliccata.position
                            # Controlla e aggiorna gli spostamenti nella scacchiera
                            # Se click in posizione non corretta, ritorna solo un messaggio
                            if (self.gioco_orso.is_hunter_turn()):
                                self._msg = self.gioco_orso.manage_hunter_selection(self._selezione)
                            else:
                                if IS_AI_BEAR_PLAYING:
                                    self._msg = self.gioco_orso.manage_ai_bear_selection()                       
                                else:
                                    self._msg = self.gioco_orso.manage_bear_selection(self._selezione)
            self.clock.tick(60)
            # Disegna la scacchiera
            self.screen.blit(self.BOARD_IMG, (0, 0))
            # Pannello uscita
            self.screen.blit(self.USCITA_IMG, (1250, 580))
            # Aggiorna le caselle
            self._lista_caselle.update()
            self._lista_caselle.draw(self.screen)
            # Aggiorna HUD
            self._hud.update()
            self._hud.draw(self.screen)
            # Check fine del gioco
            if self.gioco_orso.game_over():
                self._msg = self.gioco_orso.get_winner_display()
                if self.gioco_orso.is_bear_winner():
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/orso_ride.wav'))
                    self.screen.blit(self.ORSO_VINCE, (580,380))            
                else:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/cacciatori_ridono.wav'))
                    self.screen.blit(self.CACCIATORI_VINCONO, (480,380))            
            # Aggiornamento screen
            pygame.display.update()
            # Reset del gioco
            if self.gioco_orso.game_over():
                time.sleep(5)
                # Si inverte chi inizia
                inizia_cacciatore = not(inizia_cacciatore)
                if inizia_cacciatore:
                    self._msg = "Ricominciano i cacciatori"
                else:
                    self._msg = "Ricomincia l'orso"
                self.gioco_orso.reset(numero_mosse, inizia_cacciatore)


# Classi opzioni di menu
class OpzioneMenu(pygame.sprite.Sprite):
    '''
    Classe generica di opzione menu, richiede
    - opzioni come dizionario valore:voce da visualizzare
    - valore iniziale di default
    - gioco orso
    - posizione del pannello di sfondo
    '''
    PANNELLO_UNO_IMG = get_img('images/buttonLong.png') #panel
    def __init__(self, opzioni: dict, default_value: object, game: OrsoPyGame, position: tuple):
        super().__init__()
        self.game = game
        self.LOBSTER_30 = pygame.font.Font('fonts/LobsterTwo-Regular.otf',30)
        # Iniziano i cacciatori è il default
        self.value = default_value
        self.opzioni = opzioni
        self.position = position

    def update(self):
        self.game.screen.blit(OpzioneMenuNumeroMosse.PANNELLO_UNO_IMG, self.position)
        self._text = self.LOBSTER_30.render(
            self.opzioni[self.value], 
            1, 
            BLACK)
        self.rect = self._text.get_rect()
        self.rect.x = self.position[0]+20
        self.rect.y = self.position[1]+25
        self.image = self._text

    def action(self):
        raise NotImplementedError("Action must be implemented by child class")


class OpzioneMenuInizoTurno(OpzioneMenu):
    def action(self):
        self.value = not(self.value)


class OpzioneMenuNumeroMosse(OpzioneMenu):
    def action(self):
        self.value += 10
        if self.value == 50:
            self.value = 20


class OpzioneMenuUscita(pygame.sprite.Sprite):
    '''Menu: uscita'''
    def __init__(self, game: OrsoPyGame):
        super().__init__()
        self.game = game
        self.ESCI_GIOCO = get_img('images/buttonLong.png')
        self.ESCI_GIOCO_STR = get_img_alpha("images/Esci-dal-gioco.png")


    def update(self):
        self.game.screen.blit(self.ESCI_GIOCO, (100, 680))
        self.rect = self.ESCI_GIOCO_STR.get_rect()
        self.rect.x = 170
        self.rect.y = 690
        self.image = self.ESCI_GIOCO_STR

    def action(self):
        self.game._running = False
        self.game._quit()
    

class OpzioneMenuInizioGioco(pygame.sprite.Sprite):
    '''Menu: inizio'''
    def __init__(self, game: OrsoPyGame):
        super().__init__()
        self.game = game
        self.INIZIA = get_img('images/buttonLong.png')
        self.INIZIA_STR = get_img_alpha("images/Inizia-a-giocare.png")


    def update(self):
        self.game.screen.blit(self.INIZIA, (1100, 680))
        self.rect = self.INIZIA_STR.get_rect()
        self.rect.x = 1140
        self.rect.y = 700
        self.image = self.INIZIA_STR

    def action(self):
        self.game._running = False
        pygame.time.delay(800)
        # fade out menu music
        pygame.mixer.music.fadeout(800)
        self.game.game(
            self.game._m_mosse.value, 
            self.game._m_inizia_cacciatore.value
        )
  

# Classi HUD di gioco
class HudTurno(pygame.sprite.Sprite):
    '''HUD: pannello per il turno'''
    ORSO_IDLE_IMG = get_img('images/little-bear-idle.png')
    TRE_CACCIATORI_IMG = get_img('images/TreCacciatoriTurno.png')
    
    PANNELLO_DUE_IMG = get_img('images/panel.png') #panel_due
 
    def __init__(self, game: OrsoPyGame):
        super().__init__()
        self.game = game
        self.LOBSTER_45 = pygame.font.Font('fonts/LobsterTwo-Regular.otf',45)

        self._turno_str = self.LOBSTER_45.render("Turno", 1, BLACK)

    def update(self): 
        # Inizializzazione Pannello turno, parte fissa
        self.game.screen.blit(HudTurno.PANNELLO_DUE_IMG, (1250, 80))        
        self.game.screen.blit(self._turno_str, (1300, 90))          
        if self.game.gioco_orso._is_hunter_turn:
            self.rect = HudTurno.TRE_CACCIATORI_IMG.get_rect()
            self.rect.x = 1265
            self.rect.y = 160
            self.image = HudTurno.TRE_CACCIATORI_IMG
        else:
            self.rect = HudTurno.ORSO_IDLE_IMG.get_rect()
            self.rect.x = 1320
            self.rect.y = 160
            self.image = HudTurno.ORSO_IDLE_IMG


class HudMosseOrso(pygame.sprite.Sprite):
    '''HUD: pannello per il contatore mosse orso'''
    PANNELLO_DUE_IMG = get_img('images/panel.png') #panel_due

    def __init__(self, game: OrsoPyGame):
        super().__init__()
        self.game = game
        self.LOBSTER_45 = pygame.font.Font('fonts/LobsterTwo-Regular.otf',45)
        self.LOBSTER_90 = pygame.font.Font('fonts/LobsterTwo-Regular.otf',90)
        # Pannello mosse orso
        self._mosse_str = self.LOBSTER_45.render("Mosse orso", 1, BLACK)     
            
    def update(self):
        self._mosse = self.LOBSTER_90.render(str(self.game.gioco_orso.get_bear_moves()), 1, BLACK)       
        self.game.screen.blit(HudMosseOrso.PANNELLO_DUE_IMG, (80, 80))  
        self.game.screen.blit(self._mosse_str, (90, 90))  
        self.rect = self._mosse.get_rect()
        self.rect.x = 145
        self.rect.y = 140
        self.image = self._mosse


class HudMessaggi(pygame.sprite.Sprite):
    '''HUD: pannello per i messaggi'''    
    PANNELLO_UNO_IMG = get_img('images/buttonLong.png') #panel

    def __init__(self, game: OrsoPyGame):
        super().__init__()
        self.game = game
        self.LOBSTER_30 = pygame.font.Font('fonts/LobsterTwo-Regular.otf',30)

    def update(self):
        self._text = self.LOBSTER_30.render(self.game._msg, 1, BLACK)
        self.game.screen.blit(self.PANNELLO_UNO_IMG, (40, 680))
        self.rect = self._text.get_rect()
        self.rect.x = 50
        self.rect.y = 705
        self.image = self._text


class CasellaGiocoOrso(pygame.sprite.Sprite):
    '''
    Oggetto casella del gioco
    Gestisce la visualizzazione di personaggi e orme
    '''
    # Static resources
    TRASPARENTE = pygame.Surface((80,80), pygame.SRCALPHA)

    ORSO_IMG = get_img('images/little-bear.png')
    ORSO_IDLE_IMG = get_img('images/little-bear-idle.png')
    ORSO_SEL_IMG = get_img('images/little-bear-sel.png')

    CACCIATORE_UNO_IMG = get_img('images/little-hunter1.png')
    CACCIATORE_UNO_IDLE_IMG = get_img('images/little-hunter1-idle.png')
    CACCIATORE_UNO_SEL_IMG = get_img('images/little-hunter1-sel.png')

    CACCIATORE_DUE_IMG = get_img('images/little-hunter2.png')
    CACCIATORE_DUE_IDLE_IMG = get_img('images/little-hunter2-idle.png')
    CACCIATORE_DUE_SEL_IMG = get_img('images/little-hunter2-sel.png')

    CACCIATORE_TRE_IMG = get_img('images/little-hunter3.png')
    CACCIATORE_TRE_IDLE_IMG = get_img('images/little-hunter3-idle.png')
    CACCIATORE_TRE_SEL_IMG = get_img('images/little-hunter3-sel.png')
        
    # Orme
    ORMA_ORSO_IMG = get_img('images/impronta_orso.png')
    ORMA_CACCIATORE_IMG = get_img('images/impronta_cacciatore.png')

    def __init__(self, position: int, game: OrsoPyGame):
        super().__init__()
        self.position = position
        self.game = game

    def update(self):
        '''Valorizza l'attributo image dello sprite'''
        # Disegna la pedine ottenendo la board dall'oggetto gioco
        bb = self.game.gioco_orso
        if bb.get_board_position(self.position) == '_':
            # Controllo se è orma
            is_orma, tipo_orma  = bb.is_footprint_and_type(self.position)            
            if is_orma:
                if tipo_orma == 'HUNTER':
                    self.image = CasellaGiocoOrso.ORMA_CACCIATORE_IMG
                else:
                    self.image = CasellaGiocoOrso.ORMA_ORSO_IMG                    
            else:
                self.image = CasellaGiocoOrso.TRASPARENTE
        # Verifica se è orso
        elif bb.get_board_position(self.position) == '2':            
            if not bb.is_hunter_turn():
                self.image = CasellaGiocoOrso.ORSO_SEL_IMG
            else:
                self.image = CasellaGiocoOrso.ORSO_IMG
        # Verifica se è uno dei cacciatori
        elif bb.get_board_position(self.position) == '1':
            if (bb.get_hunter_starting_pos() == self.position):
                self.image = CasellaGiocoOrso.CACCIATORE_UNO_SEL_IMG
            else:
                if bb.is_hunter_turn():
                    self.image = CasellaGiocoOrso.CACCIATORE_UNO_IMG
                else:
                    self.image = CasellaGiocoOrso.CACCIATORE_UNO_IDLE_IMG
        elif bb.get_board_position(self.position) == '8':
            if (bb.get_hunter_starting_pos() == self.position):
                self.image = CasellaGiocoOrso.CACCIATORE_DUE_SEL_IMG
            else:
                if bb.is_hunter_turn():
                    self.image = CasellaGiocoOrso.CACCIATORE_DUE_IMG
                else:
                    self.image = CasellaGiocoOrso.CACCIATORE_DUE_IDLE_IMG
        elif bb.get_board_position(self.position) == '9':
            if (bb.get_hunter_starting_pos() == self.position):
                self.image = CasellaGiocoOrso.CACCIATORE_TRE_SEL_IMG
            else:
                if bb.is_hunter_turn():
                    self.image = CasellaGiocoOrso.CACCIATORE_TRE_IMG
                else:
                    self.image = CasellaGiocoOrso.CACCIATORE_TRE_IDLE_IMG


class Player:
    def __init__(self, name):
        self.name = name
        self.states_value = {}  # state -> value

    def get_action(self, actions, current_board: OrsoPyGame):
        value_max = -INFINITY
        for act in actions:
            current_board.move_player(act[0], act[1])
            state_value = self.states_value.get(current_board.get_hash())
            if (state_value is None):
                value = 0
            else:
                value = state_value

            if value >= value_max:
                value_max = value
                action = act

            current_board.undo_move()
        return action

    def print_value(self, board):
        print(f"{self.name}: {board.get_hash()} -> {self.states_value.get(board.get_hash())}")

    def load_policy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

# Main
if __name__ == "__main__":
    # Il gioco è richiamato da menu
    opg = OrsoPyGame()
    opg.menu()


