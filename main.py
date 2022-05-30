from CONSTANTS import *  
import pygame as pg
from states.menu import menu 
from states.game import gameplay
from behaviours.player import player
from behaviours.level import level_manager 
from engine import *

class game_state:
    def __init__(self):
        self.win = pe_win(WINDOW_SIZE, TITLE)
        # a smaller screen surface which is then scaled up
        self.screen = pg.Surface(DISPLAY_SIZE)

        self.running = 1
        self.lmbtn_down = 0
        self.mouse = pe_mouse()
        self.mouse_pos = [0, 0]
        self.helping = 0
        # storing the pygame events
        self.events = 0

        self.lvls = level_manager(LVLS, LVLS_FOLDER, TILE_SIZE, TILE_NUM, TILES)
        self.player = player(self.lvls.get_player_pos(), PLAYER_SIZE, PLAYER_IMG_FOLDER, None, PLAYER_STATES, PLAYER_STATE_LIST)
        self.player.rect.w = 14
        self.player.rect.h = 19
        self.lvls.get_rects()

    ## chdeck libs, email and y
    # this function handles different game states like menu..etc..
    def handle_states(self):
        while self.running:
            self.mouse_pos = self.mouse.get_scaled_pos(self.win.get_size(), DISPLAY_SIZE)
            # menu
            while self.running == 1:
                menu(self)
            
            while self.running == 2 or self.running == 3: 
                gameplay(self)


    # closing
    def destroy(self):
        self.win.close()

if __name__ == '__main__':
    game_s = game_state()
    game_s.handle_states()
    game_s.lvls.save("res/lvls/save.txt")
    game_s.destroy()


