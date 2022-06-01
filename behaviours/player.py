import pygame as pg

def centered_rotation(surf, image, topleft, angle):
    rotated_image = pg.transform.rotate(image, -angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)


fonts = {}
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pg.font.Font(font, size)
    surf = fonts[size].render(text, False, color)  
    x = x - surf.get_rect().width / 2
    y = y - surf.get_rect().height / 2

    surface.blit(surf, (x, y))

class player:
    def __init__(self, spawn_pos, size, img_folder, colorkey, state_num, states_list):
        self.moving = {
            "right" : 0,
            "left"  : 0,
            "up"    : 0,
            "down"  : 0
        }
        self.collision = {
            "right" : 0,
            "left"  : 0,
            "up"    : 0,
            "down"  : 0
        }
        self.vel = [0, 0]
        self.rect = pg.Rect(spawn_pos[0], spawn_pos[1], 
                            size[0], size[1])
        self.orig_rect = pg.Rect(spawn_pos[0], spawn_pos[1], size[0], size[1]) 
        self.scroll = [0, 0]
        self.true_scroll = [0.0, 0.0]
        self.animated_imgs = {}
        self.use_timer = 0
        self.delta_timer = 0
        self.time_delta = 1
        player.timer = 0
        for i in range(0, state_num):
            self.animated_imgs[states_list[i][0]] = [] 
            for n in range(0, states_list[i][1]):
                img = pg.image.load(img_folder + states_list[i][0] + "/" + str(n) + ".png").convert_alpha()
                img.set_colorkey(colorkey)
                img = pg.transform.scale(img, size)
                self.animated_imgs[states_list[i][0]].append(img)

        ## animation
        self.current_img = None
        self.state = "idle"
        self.frames_passed = 0
        self.current_frame = 0
        self.flipped = 0

        self.weapon_img = pg.image.load("res/imgs/player/weapons/weapon_anime_sword.png").convert() 
        self.weapon_img.set_colorkey((0, 0, 0))
        self.weapon_rect = pg.Rect(self.rect.x, self.rect.y, self.weapon_img.get_size()[0], self.weapon_img.get_size()[1])
        self.weapon_deg_change = 0
        self.weapon_deg = 0
        self.weapon_flip = 0
        self.health = 5
        self.change_level = 0

    ### calculating offset for camera, this is done by subtracting
    ### the scroll from the current x pos and then subtracting half the
    ### display size and then adding half the size of the player rect, 
    ### dividing by 10 gives the camera a follow effect
    def calc_scroll(self, display_size):
        self.true_scroll[0] += (self.rect.x - self.true_scroll[0] - display_size[0] / 2 + self.rect.w / 2) / 10
        self.true_scroll[1] += (self.rect.y - self.true_scroll[1] - display_size[1] / 2 + self.rect.h / 2) / 10
        self.scroll = [round(self.true_scroll[0]), round(self.true_scroll[1])]

    def reset_val(self):
        self.vel = [0, 0]
        self.collision = {
            "right" : 0,
            "left"  : 0,
            "up"    : 0,
            "down"  : 0
        }

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if self.state == "won":
                    if e.key == pg.K_e:
                        self.state = "idle"
                        self.change_level = 1

                if self.state == "failed":
                    if e.key == pg.K_e:
                        self.state = "idle"
                        self.health = 5
                if self.state != "failed":
                    if e.key == pg.K_d:
                        self.moving["right"] = 1

                    if e.key == pg.K_a:
                        self.moving["left"] = 1

                    if e.key == pg.K_s:
                        self.moving["down"] = 1
                    
                    if e.key == pg.K_w:
                        self.moving["up"] = 1
                    
                    if e.key == pg.K_SPACE:
                        self.weapon_deg_change = 1

            if e.type == pg.KEYUP:
                if e.key == pg.K_d:
                    self.moving["right"] = 0

                if e.key == pg.K_a:
                    self.moving["left"] = 0

                if e.key == pg.K_s:
                    self.moving["down"] = 0
                
                if e.key == pg.K_w:
                    self.moving["up"] = 0

    def update(self):
        if self.health <= 0:
            self.state = "failed"

        if self.state != "failed":
            if self.moving["right"]:
                self.vel[0] += 3
            
            if self.moving["left"]:
                self.vel[0] -= 3

            if self.moving["up"]:
                self.vel[1] -= 3

            if self.moving["down"]:
                self.vel[1] += 3

        if self.weapon_deg_change:
            if self.weapon_flip:
                self.weapon_deg -= 18
            else:
                self.weapon_deg += 18
            if self.weapon_deg > 360 or self.weapon_deg < -360:
                self.weapon_deg = 0
                self.weapon_deg_change = 0

        # if velocity is not 0, it means running
        if (self.vel[0] != 0 or self.vel[1] != 0) and self.state != "failed" and self.state != "run":
            self.state = "run"
            self.current_frame = 0
       
        if self.vel[0] < 0 and self.vel[0] != 0:
            self.flipped = 1

        if self.vel[0] > 0 and self.vel[0] != 0:
            self.flipped = 0

        # if all velocity val are 0, then idle
        if not self.moving["left"] and not self.moving["right"] and self.state != "idle" and self.state != "failed":
            self.state = "idle"
            self.current_frame = 0

        self.frames_passed += 1

        # the animation runs at 1 frame every 15 frames
        if self.state != "failed":
            if self.frames_passed > 0 and self.frames_passed % 15 == 0:
                self.frames_passed = 0
                if self.current_frame < len(self.animated_imgs[self.state]) - 1:
                    self.current_frame += 1
                else:
                    self.current_frame = 0

        if not self.weapon_deg_change:
            self.weapon_flip = self.flipped
            if not self.weapon_flip:
                self.weapon_rect.x = self.rect.x + self.rect.w - 2
            else:
                self.weapon_rect.x = self.rect.x - self.rect.w + 2
        else:
            self.weapon_flip = self.weapon_flip
            if not self.weapon_flip:
                self.weapon_rect.x = self.rect.x + self.rect.w - 2
            else:
                self.weapon_rect.x = self.rect.x - self.rect.w + 2

        self.weapon_rect.y = self.rect.y
        #self.weapon_rect.y = self.rect.y + self.rect.h / 2


    def render(self, surf):
        if self.state != "failed" and self.state != "won":
            self.current_img = (self.animated_imgs[self.state][self.current_frame])
            self.current_img = pg.transform.flip(self.current_img, self.flipped, 0)
            
            new_rect =  pg.Rect(self.weapon_rect.x - self.scroll[0],
                                self.weapon_rect.y - self.scroll[1],
                                self.weapon_rect.w, self.weapon_rect.h)

            surf.blit(self.current_img, (self.rect.x - self.scroll[0] - 2, self.rect.y - self.scroll[1] - 9))
            centered_rotation(surf, pg.transform.flip(self.weapon_img, self.weapon_flip, 0), new_rect.topleft, self.weapon_deg)
            for i in range(0, self.health):
                pg.draw.rect(surf, (255, 150, 200), pg.Rect(10 * i + 10, 10, 5, 5))
        if self.state == "failed":
            text("You died, press E to play again", (255, 255, 255), 
                  40, surf.get_size()[0] / 2, surf.get_size()[1] / 2, "res/m5x7.ttf",
                  surf)  

        if self.state == "won":
            self.state = "idle"
            self.current_frame = 0
            self.current_img = (self.animated_imgs[self.state][self.current_frame])
            self.current_img = pg.transform.flip(self.current_img, self.flipped, 0)
            
            new_rect =  pg.Rect(self.weapon_rect.x - self.scroll[0],
                                self.weapon_rect.y - self.scroll[1],
                                self.weapon_rect.w, self.weapon_rect.h)

            surf.blit(self.current_img, (self.rect.x - self.scroll[0] - 2, self.rect.y - self.scroll[1] - 9))
            centered_rotation(surf, pg.transform.flip(self.weapon_img, self.weapon_flip, 0), new_rect.topleft, self.weapon_deg)
            for i in range(0, self.health):
                pg.draw.rect(surf, (255, 150, 200), pg.Rect(10 * i + 10, 10, 5, 5))
            text("You completed the level!", (255, 255, 255), 
                  40, surf.get_size()[0] / 2, surf.get_size()[1] / 2, "res/m5x7.ttf",
                  surf)  
            text("Press E to continue", (255, 255, 255), 
                  40, surf.get_size()[0] / 2, surf.get_size()[1] / 2 + 20, "res/m5x7.ttf",
                  surf)             
            self.state = "won"




