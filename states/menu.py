import pygame as pg

fonts = {}
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pg.font.Font(font, size)
    surf = fonts[size].render(text, False, color)  
    x = x - surf.get_rect().width / 2
    y = y - surf.get_rect().height / 2

    surface.blit(surf, (x, y))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = "res/m5x7.ttf"

def menu_events(game):
    game.events = pg.event.get()
    for e in game.events:
        if e.type == pg.QUIT:
            game.running = 0
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_e:
                game.running = 2
                game.lvls.reset(game.player)
                game.lvls.lvls_all_complete = 0 
                game.lvls.level_completed = 0
                game.player.state = "idle"
                game.player.change_level = 0
                game.player.health = 5
                game.player.reset_val()



    game.player.handle_events(game.events)

def menu_update(game):
    pass

def menu_render(game):
    game.screen.fill(BLACK)
    text("Press E to play. Space is to attack and WASD is for moving", 
         WHITE, 30, game.screen.get_size()[0] / 2, 
         game.screen.get_size()[1] / 2, FONT,
         game.screen)

def menu(game):
    menu_events(game)
    menu_update(game)
    menu_render(game)
    game.win.draw(game.screen, scale=2)

