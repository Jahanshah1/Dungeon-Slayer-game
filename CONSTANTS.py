TITLE = "Game"
WINDOW_SIZE = (1280, 720)
DISPLAY_SIZE = (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
DISPLAY_CENTER = (DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2)


HELP_STR = [ 
]

PLAYER_SIZE = (16, 28)
PLAYER_IMG_FOLDER = "res/imgs/player/wizard/"
PLAYER_STATES = 3
PLAYER_STATE_LIST = [("idle", 4), 
                     ("run", 4),
                     ("hit", 1)]

LVLS = 3
LVLS_FOLDER = "res/lvls/"
TILE_SIZE = (32, 32)
TILE_NUM = 3
TILES = {
    "0" : "res/imgs/tiles/floor/floor_1.png",
    "1" : "res/imgs/tiles/wall/wall_mid.png",
    "zombie" : "res/imgs/enemies/ice_zombie/0.png",
    "goblin" : "res/imgs/enemies/goblin/0.png",
    "tiny_zombie" : "res/imgs/enemies/tiny_zombie/0.png",
    "big_zombie" : "res/imgs/enemies/big_zombie/0.png",
    "big_demon" : "res/imgs/enemies/big_demon/0.png",
    "wogol" : "res/imgs/enemies/wogol/0.png"
}
