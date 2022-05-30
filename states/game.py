import pygame as pg

fonts = {}
### centered text drawing
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pg.font.Font(font, size)
    surf = fonts[size].render(text, False, color)  
    x = x - surf.get_rect().width / 2
    y = y - surf.get_rect().height / 2

    surface.blit(surf, (x, y))

WHITE = (255, 255, 255)
SKY_COLOR = (52, 171, 249)
FONT = "res/m6x11.ttf"

def game_events(game):
    game.events = pg.event.get()
    if game.running == 2:
        for e in game.events:
            if e.type == pg.QUIT:
                game.running = 0
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    game.running = 1
                    game.player.state = "idle"
                    game.lvls.boss_fight = 0

        game.player.handle_events(game.events)

    if game.running == 3:
        for e in game.events:
            if e.type == pg.QUIT:
                game.running = 0
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_e:
                    game.lvls.lvls_all_complete = 0 
                    game.running = 1
                    game.lvls.current_lvl = 0
                    game.lvls.level_completed = 0
                    game.player.state = "idle"
                    game.player.change_level = 0
                    game.player.health = 5
                    game.player.reset_val()

def game_update(game):
    if game.lvls.lvls_all_complete:
        game.running = 3

    if game.running == 2:
        game.player.reset_val()
        ### camera
        game.player.calc_scroll(game.screen.get_size())

        if game.player.change_level:
            game.lvls.level_completed = 1
            game.player.change_level = 0

        ### updating player animation..etc..
        game.player.update()

        game.lvls.check_collisions(game.player)

def game_render(game):
    if game.running == 2:
        game.screen.fill((70, 59, 58))

        game.lvls.render(game.screen, game.player.scroll)
        game.player.render(game.screen)

    else:
        game.screen.fill((70, 59, 58))
        text("You finished the game!", (255, 255, 255), 30, 
             game.screen.get_size()[0] / 2, game.screen.get_size()[1] / 2,
             "res/m5x7.ttf", game.screen)
        text("Go back to menu by pressing E", (255, 255, 255), 30, 
             game.screen.get_size()[0] / 2, game.screen.get_size()[1] / 2 + 20,
             "res/m5x7.ttf", game.screen)





def gameplay(game):
    game_events(game)
    game_update(game)
    game_render(game)
    game.win.draw(main_surf = game.screen, scale = 2);
"""
     if game.lvls.level_completed:
        game.running = 3
        game.state_changed = 1
        game.lvls.level_completed = 0
        
    if game.lvls.current_lvl >= game.lvls.lvl_num:
        game.running = 5
        game.state_changed = 1




"""

