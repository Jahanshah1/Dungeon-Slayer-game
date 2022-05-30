import pygame as pg
import sys

pg.init()
pg.font.init()
pg.mixer.init()
pg.display.init()

# A small window class
class pe_win:
    def __init__(self, size, caption = "pg game", flags = 0, icon = None):
        self.size = size 
        self.caption = caption
        self.flags = flags
        self.icon = icon
        self.screen = pg.display.set_mode(self.size, self.flags)

        pg.display.set_caption(caption)

        self.fps = pg.time.Clock()

        if icon is not None:
            pg.display.set_icon(pg.image.load(self.icon).convert())
    
        self.display_size = pg.display.get_surface().get_size()

    def cls(self, color = (0, 0, 0)):
        self.screen.fill(color)

    def get_size(self):
        self.display_size = pg.display.get_surface().get_size()
        return self.display_size

    # Draws a smaller surface which contains the main game, 
    # helps in making the game faster
    def draw(self, main_surf=None, pos=[0, 0], scale=0, fps=60):
        self.screen.fill((0, 0, 255))

        self.display_size = pg.display.get_surface().get_size()
        if main_surf is not None and scale:
            pg.transform.scale(main_surf, self.display_size, dest_surface=self.screen)

        if main_surf is not None and not scale:
            self.screen.blit(main_surf, pos)

        pg.display.update()
        self.fps.tick(fps)

    # Closes pygame and the program
    def close(self):
        pg.quit()
        sys.exit()

class pe_mouse:
    def __init__(self, img = None, visible = True):
        self.visible = visible
        pg.mouse.set_visible(self.visible)
        self.pos = pg.mouse.get_pos()
        self.scaled_pos = None

    # If you use a smaller surface than the original display, this function is very important
    def get_scaled_pos(self, win_size, surf_size):
        self.pos = pg.mouse.get_pos()
        self.scaled_pos = (self.pos[0] / (win_size[0] / surf_size[0]), self.pos[1] / (win_size[1] / surf_size[1]))
        return self.scaled_pos

