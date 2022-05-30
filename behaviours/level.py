import pygame as pg
import random
import math

def load_map(path):
    return [list(row) for row in open(path + ".txt", "r").read().split("\n")]

def load_img_scaled(path, size):
    return pg.transform.scale(pg.image.load(path).convert(), size)

def dist2d(x0, y0, x1, y1):
    return math.sqrt(((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)))

fonts = {}
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pg.font.Font(font, size)
    surf = fonts[size].render(text, False, color)  
    x = x - surf.get_rect().width / 2
    y = y - surf.get_rect().height / 2

    surface.blit(surf, (x, y))

class level_manager:
    def __init__(self, lvl_num, lvl_path, tile_size, tile_num, tiles):
        self.lvls = []
        ## load
        for i in range(0, lvl_num):
            self.lvls.append(load_map(lvl_path + str(i))) 
        self.lvl_num = lvl_num
        self.rects = []
        ### save file
        try:
            lvl_str = open(lvl_path + "save.txt", "r").read().split("\n")
            self.current_lvl = int(lvl_str[0]) - 1
            self.old_unlocked_lvl = self.current_lvl
        except Exception as e:
            print(e)
            self.current_lvl = 0
            self.old_unlocked_lvl = 0
        
        ### other
        self.tile_size = tile_size
        self.level_completed = 0

        ### images
        self.tiles = {}
        for i in tiles:
            self.tiles[i] = load_img_scaled(tiles[i], tile_size)
        self.enemies = []

        self.boss = [] 
        self.boss_fight = 0
        self.music = pg.mixer.Sound(lvl_path + "hit.wav")
        self.p_music = pg.mixer.Sound(lvl_path + "p_hit.wav")
        self.lvls_all_complete = 0
        
    def get_rects(self):
        if self.current_lvl < self.lvl_num:
            self.rects = []
            y = 0
            for row in self.lvls[self.current_lvl]:
                x = 0
                for tile in row:
                    if tile == "1":
                        self.rects.append(pg.Rect(
                            x * self.tile_size[0],
                            y * self.tile_size[1],
                            self.tile_size[0],
                            self.tile_size[0],
                        ))
                    if tile == "2" or tile == "6" or tile == "7":
                        self.enemies.append([pg.Rect(
                            x * self.tile_size[0],
                            y * self.tile_size[1],
                            16, 16
                        ), random.randint(0, 2)]) 
                        self.lvls[self.current_lvl][y][x] = "0"

                    if tile == "3":
                        self.boss = []
                        self.boss.append(pg.Rect(
                            x * self.tile_size[0],
                            y * self.tile_size[1],
                            32, 34))
                        self.boss.append(random.randint(10, 20))
                        self.boss.append("Big Zombie")
                        self.boss.append("big_zombie")
                        self.lvls[self.current_lvl][y][x] = "0"

                    if tile == "4":
                        self.boss = []
                        self.boss.append(pg.Rect(
                            x * self.tile_size[0],
                            y * self.tile_size[1],
                            16, 20))
                        self.boss.append(random.randint(20, 40))
                        self.boss.append("Wogol")
                        self.boss.append("wogol")
                        self.lvls[self.current_lvl][y][x] = "0"

                    if tile == "5":
                        self.boss = []
                        self.boss.append(pg.Rect(
                            x * self.tile_size[0],
                            y * self.tile_size[1],
                            32, 36))
                        self.boss.append(random.randint(50, 70))
                        self.boss.append("Big Demon")
                        self.boss.append("big_demon")
                        self.lvls[self.current_lvl][y][x] = "0"

                    x += 1
                y += 1
    
    def get_player_pos(self):
        y = 0
        lvl_n = self.current_lvl
        if self.current_lvl >= self.lvl_num: lvl_n -= 1 
        for row in self.lvls[lvl_n]:
            x = 0
            for tile in row:
                if tile == "p":
                    return (x * self.tile_size[0], y * self.tile_size[1])
                x += 1
            y += 1

    ### doing collision through SAT
    ###     basically add x-vel and then check for collision
    ###     and then add y-vel and then check for collision
    def check_collisions(self, player):
        for n in self.enemies:
            i = n[0]
            xdist_from_player = dist2d(player.rect.x, player.rect.y, 
                                       i.x, i.y)
            
            if abs(xdist_from_player) < 80:
                direction = math.atan2(player.rect.y - i.y, player.rect.x - i.x)
                i.x += math.cos(direction) * 1.5
                i.y += math.sin(direction) * 1.5

                a_coll = 0
                if i.colliderect(player.weapon_rect) and player.weapon_deg_change:
                    self.enemies.remove(n)
                    player.health += 1
                    a_coll = 1
                    self.music.play()

                if not a_coll:
                    coll = 0
                    p_rect = None
                    p_rect = pg.Rect(player.rect.x,  player.rect.y, player.rect.w, player.rect.h)

                    if i.colliderect(p_rect): 
                        coll = 1
                        # player.health -= 1
                        if player.flipped:
                            player.vel[0] += 30
                        if not player.flipped:
                            player.vel[0] -= 30

                    if coll:
                        player.health -= 1
                        if player.flipped:
                            i.x -= 30 
                        else:
                            i.x += 30
                        self.p_music.play()
                    
        if self.boss[1] > 0:
            xdist_from_player = dist2d(player.rect.x, player.rect.y, 
                                        self.boss[0].x, self.boss[0].y)
            
            if abs(xdist_from_player) < 200:
                self.boss_fight = 1
                direction = math.atan2(player.rect.y - self.boss[0].y, player.rect.x - self.boss[0].x)
                self.boss[0].x += math.cos(direction) * 1.5
                self.boss[0].y += math.sin(direction) * 1.5

                a_coll = 0
                coll = 0
                if (self.boss[0]).colliderect(player.weapon_rect) and player.weapon_deg_change:
                    self.boss[1] -= 1
                    a_coll = 1

                if not a_coll:
                    coll = 0
                    p_rect = None
                    p_rect = pg.Rect(player.rect.x,  player.rect.y, player.rect.w, player.rect.h)

                    if (self.boss[0]).colliderect(p_rect): 
                        coll = 1
                        # player.health -= 1
                        if player.flipped:
                            player.vel[0] += 30
                        if not player.flipped:
                            player.vel[0] -= 30

                if coll or a_coll:
                    if player.flipped:
                        self.boss[0].x -= 30
                    else:
                        self.boss[0].x += 30
                    if coll:
                        player.health -= 1
                        self.p_music.play()
                    self.music.play()

        if self.boss[1] <= 0:
            self.boss_fight = 0
            player.state = "won"

        if player.state == "failed":
            player.rect.x = self.get_player_pos()[0]
            player.rect.y = self.get_player_pos()[1]

        if self.level_completed:
            self.progress(player)
            self.level_completed = 0

        self.get_rects()
        player.rect.x += player.vel[0]
        hit_list = [tile for tile in self.rects if player.rect.colliderect(tile)]
        for i in hit_list:
            if player.vel[0] < 0:
                player.rect.left = i.right 
                player.collision["left"] = 1

            elif player.vel[0] > 0:
                player.rect.right = i.left 
                player.collision["right"] = 1

        player.rect.y += player.vel[1]
        hit_list = [tile for tile in self.rects if player.rect.colliderect(tile)]
        for i in hit_list:
            if player.vel[1] < 0:
                player.rect.top = i.bottom
                player.collision["up"] = 1

            elif player.vel[1] > 0:
                player.rect.bottom = i.top
                player.collision["down"] = 1


    def progress(self, player):
        self.boss = [] 
        self.current_lvl += 1    
        
        if self.current_lvl > self.lvl_num - 1:
            self.lvls_all_complete = 1
            self.current_lvl = self.lvl_num - 1

        if not self.lvls_all_complete:
            player.rect.x = self.get_player_pos()[0]
            player.rect.y = self.get_player_pos()[1]
            self.get_rects()

    def reset(self, player):
        self.enemies = []
        self.boss = []
        player.rect.x = self.get_player_pos()[0]
        player.rect.y = self.get_player_pos()[1]
        for i in range(0, self.lvl_num):
            self.lvls[i] = load_map("res/lvls/" + str(i))
        self.get_rects()

    def render(self, surf, scroll):
        if not self.lvls_all_complete:
            y = 0
            for row in self.lvls[self.current_lvl]:
                x = 0
                for tile in row:
                    rect = pg.Rect(
                        x * self.tile_size[0] - scroll[0],
                        y * self.tile_size[1] - scroll[1],
                        self.tile_size[0],
                        self.tile_size[1]
                    )
                    if tile != "p":
                        surf.blit(self.tiles[tile], rect)
                    else:
                        surf.blit(self.tiles["0"], rect)
                    if tile != "p" and int(tile) > 1:
                        surf.blit(self.tiles["0"], rect)
                        self.tiles[tile].set_colorkey((0, 0, 0))
                        surf.blit(self.tiles[tile], rect)

                    x += 1

                y += 1
            for i in self.enemies:
                l = ["zombie", "goblin", "tiny_zombie"]
                n = pg.Rect(i[0].x - scroll[0], i[0].y - scroll[1], 
                            i[0].w, i[0].h)
                num = i[1] 
                self.tiles[l[num]].set_colorkey((0, 0, 0))
                surf.blit(self.tiles[l[num]], n)

            if self.boss[1] > 0:
                n = pg.Rect(self.boss[0].x - scroll[0], self.boss[0].y - scroll[1], 
                            self.boss[0].w, self.boss[0].h)
                self.tiles[self.boss[3]].set_colorkey((0, 0, 0))
                surf.blit(self.tiles[self.boss[3]], n)

            if self.boss_fight:
                pg.draw.rect(surf, (0, 0, 0), pg.Rect(0, 0, surf.get_size()[0], 50))
                pg.draw.rect(surf, (0, 0, 0), pg.Rect(0, surf.get_size()[1] - 50, surf.get_size()[0], 50))
                for i in range(0, self.boss[1]):
                    pg.draw.rect(surf, (255, 100, 100), pg.Rect(10 * i + 10, surf.get_size()[1] - 100, 10, 10))
                text(f"{self.boss[2]}", (255, 255, 255), 40, 80, surf.get_size()[1] - 120, "res/m5x7.ttf", surf)

    def save(self, path_file):
        save_f = open(path_file, "w")
        final_str = []
        lvl_n = 0
        print(self.current_lvl, self.old_unlocked_lvl)
        if self.current_lvl > self.old_unlocked_lvl:
            final_str.append(str(self.current_lvl + 1) + "\n")
            lvl_n = self.current_lvl
        else:
            final_str.append(str(self.old_unlocked_lvl + 1) + "\n")
            lvl_n = self.old_unlocked_lvl
        save_f.write("".join(final_str))                    
        save_f.close()

"""
                if i.colliderect(player.rect) and player.state == "attack" and player.current_frame > 2:
                    self.enemies.remove(i)
                    a_coll = 1

                if not a_coll and player.rect.y == i.y:
                    coll = 0
                    p_rect = None
                    if xdist_from_player < 0:
                        p_rect = pg.Rect(player.rect.x + 6, player.rect.y, 10, 16) 
                    if xdist_from_player > 0:
                        p_rect = pg.Rect(player.rect.x, player.rect.y, 10, 16) 

                    if i.colliderect(p_rect): 
                        coll = 1
                        player.health -= 1
                        if player.flipped:
                            player.vel[0] -= i.w * 1.25
                        if not player.flipped:
                            player.vel[0] += i.w * 1.25

                    if coll:
                        if player.flipped:
                            i.x += i.w * 1.25
                        else:
                            i.x -= i.w * 1.25
"""