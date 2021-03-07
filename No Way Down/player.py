import pygame
from pygame import image

class Player():
    def __init__(self, action_and_image_path = {},action_and_frames={} ):
        self.action_types = action_and_image_path
        self.action_frames = action_and_frames
        self.Player_image_width = 24
        self.Player_initial_x, self.Player_initial_y =  210,576
        self.x, self.y = 220,576
        self.player_rect = pygame.Rect(self.Player_initial_x+10, self.Player_initial_y,self.Player_image_width,self.Player_image_width)
        self.Player_Animation = {}
        self.Animation = {}
        self.draw_parameters = []
        self.cur_action = "idle"
        self.filp = False
        self.Left, self.Right, self.Up = False, False, False

    def Load_Player_image(self):
        for Action in self.action_types:
            image_path = self.action_types[Action]
            Animation_name = image_path.split("/")[-1]
            images = len(self.action_frames[Action])
            for n in range(images):
                Animation_id = Animation_name + "_" + str(n)
                img_loc = image_path + "/" + Animation_id + ".png"
                image = pygame.image.load(img_loc)
                Animation_image = pygame.transform.scale(image,(self.Player_image_width,self.Player_image_width))
                self.Player_Animation[Animation_id] = Animation_image.copy()
     
    def Load_Animation(self):
        self.Load_Player_image()
        for action in self.action_frames:
            frames = []
            n = 0
            for frame in self.action_frames[action]: 
                for _ in range(int(frame)):
                    frame_id = action + f"_{n}"
                    frames.append(frame_id)
                n+=1
            self.Animation[action] = frames

    def Set_draw_para(self,action,frame,Wall_Tile,win_Tile,scroll=[0,0]):
        if self.cur_action != action:
            frame = 0
            self.frame = frame
        else:
            self.frame = frame
            frame += 1
        anime = self.Animation[self.cur_action]
        if frame >= len(anime): frame = 0
        self.scroll = scroll
        self.Wall_tiles = Wall_Tile
        self.Win_Tile = win_Tile
        return frame

    def Check_for_win(self):
        for tile in self.Win_Tile:
            if self.player_rect.colliderect(tile):
                if tile.y <= (self.player_rect.y + self.scroll[1] - 8): return True
            return False

    def collision_test(self,tiles):
        hit_list = []
        for tile in tiles:
            if self.player_rect.colliderect(tile): hit_list.append(tile)
        return hit_list

    def movement(self):
        movement = [0,0]
        if self.Left or self.Right or self.Up:
            if self.Left:
                movement[0] -= 1
                self.cur_action = 'run'
                self.filp = False
            if self.Right:
                movement[0] += 1
                self.cur_action = 'run'
                self.filp = True
            if self.Up:
                movement[1] -= 1
                self.cur_action = "forward"
                self.filp = False
        else: self.cur_action = "idle"
        self.player_rect.x += movement[0]
        hit_list = self.collision_test(self.Wall_tiles)
        for tile in hit_list:
            if movement[0] > 0: self.player_rect.right = tile.left
            elif movement[0] < 0: self.player_rect.left = tile.right
        self.player_rect.y += movement[1]
        hit_list = self.collision_test(self.Wall_tiles)
        for tile in hit_list:
            if movement[1] < 0: self.player_rect.top = tile.bottom
     
    def draw(self,Surface):
        self.movement()
        Anime = self.Animation[self.cur_action]
        img = self.Player_Animation[Anime[self.frame]]
        image = pygame.transform.flip(img,self.filp,False)
        self.x, self.y  = self.player_rect.x + self.scroll[0], self.player_rect.y + self.scroll[1]
        Surface.blit(image,(self.player_rect.x + self.scroll[0], self.player_rect.y + self.scroll[1]))

    def get_player_pos(self):
        Pos = [ int(self.player_rect.x + self.scroll[0]), int(self.player_rect.y + self.scroll[1])]
        return Pos

    def reposite(self, player_y):
        self.player_rect.x , self.player_rect.y = self.Player_initial_x, player_y
