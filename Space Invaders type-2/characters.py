import pygame
from pygame import mixer

class Enemy_sprites():
    def __init__(self, image_path = {}):
        self.image_path = image_path
        self.Enemy_image_width, self.frame= 24, 0
        self.Enemy_initial_x, self.Enemy_initial_y =  65, 80
        self.shift_y = 35
        self.surface = None
        self.acc, self.velocity_vector, self.position = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.load_pos()
        self.Load_enemy()
    def Load_enemy(self):
        i = 0
        self.Enemy_images = {}
        self.Enemy_change_frame, self.Enemy_frame = {}, {}
        for enemy in self.image_path:
            images = self.image_path[enemy]
            image_list = []
            for image_path in images:
                img = pygame.image.load(image_path)
                image = pygame.transform.scale(img,(self.Enemy_image_width,self.Enemy_image_width))
                image_list.append(image.copy())
            self.Enemy_images[enemy] = image_list.copy()
            self.Enemy_change_frame[enemy] = i
            self.Enemy_frame[enemy] = 0
            i += 1
    def load_pos(self):
        self.Enemy_Rect = {}
        next_x_diff, next_y_diff = 45,40
        y = self.Enemy_initial_y
        for enemy in self.image_path:
            x = self.Enemy_initial_x
            rect = []
            for _ in range(15):
                rect.append(pygame.Rect(x,y,self.Enemy_image_width,self.Enemy_image_width))
                x += next_x_diff
            self.Enemy_Rect[enemy] = rect
            y += next_y_diff
    def parameters(self,delta,Surface):
        self.surface = Surface
        self.delta = delta
        self.frame += 1
        n = len(self.Enemy_change_frame)                    #  
        if self.frame % 20 == 0:                            #
            for i in self.Enemy_change_frame:               #
                self.Enemy_change_frame[i] += 1             #
                if self.Enemy_change_frame[i] % n == 0:     #
                    if self.Enemy_change_frame[i] % n == 0:     #
                        if self.Enemy_frame[i] == len(self.image_path[i])-1:
                            self.Enemy_frame[i] = 0
                        else:  self.Enemy_frame[i] += 1
            self.frame = 0
    def check_for_collision(self,player_bullet_rect):
        for enemy in self.Enemy_Rect:
            rect_list = self.Enemy_Rect[enemy]
            for rect in rect_list:
                if rect.colliderect(player_bullet_rect): 
                    rect_list.remove(rect)
                    self.Enemy_Rect[enemy] = rect_list
                    return True
        return False   
    def movement(self):
        self.acc.x = 0.3
        self.velocity_vector.x += self.acc.x * self.delta
        if self.velocity_vector.x > 1.2: self.velocity_vector.x = 1.2
        self.position.x += self.velocity_vector.x * self.delta + (self.acc.x * 0.5) * self.delta * self.delta
        new_pos_x = int(self.position.x)
        self.position.x = 0
        for enemy in self.Enemy_Rect:
            Enemy_rect = self.Enemy_Rect[enemy]
            for rect in Enemy_rect:
                rect.x += new_pos_x
                if rect.x >= (755 - self.Enemy_image_width):
                    rect.x -= 705 
                    rect.y += self.shift_y
    def check_for_win_and_lose(self):
        W, F = True, False
        for enemy in self.Enemy_Rect:
            rec_list = self.Enemy_Rect[enemy]
            if len(rec_list)>0: 
                W = False
                for rec in rec_list:
                    if rec.bottom >= 375: F = True
        if F: return 'lose'
        elif W: return 'win'
        else: return None
    def draw(self):
        self.movement()
        for enemy in self.Enemy_Rect:
            for rec in self.Enemy_Rect[enemy]:
                x = self.Enemy_frame[enemy]
                self.surface.blit(self.Enemy_images[enemy][x], (rec.x, rec.y) )
    
class Player():
    def __init__(self,image_path,Bullet_image,y):
        self.bult_img = pygame.image.load(Bullet_image)
        self.player_width, self.player_height = 32, 32
        self.stop_force, self.velocity ,self.bullet_x  = -0.25, 1, 0
        self.current_image, self.bullet_count = 0, 0
        self.player_image = []
        for path in image_path:
            img = pygame.image.load(path)
            self.player_image.append(pygame.transform.scale(img,(self.player_width,self.player_height)))
        self.surface , self.delta = None, None
        self.move_left, self.move_right, self.shoot = False, False, True
        self.player_rect = pygame.Rect(0,y,self.player_width,self.player_height)
        self.acc, self.velocity_vector, self.position = pygame.math.Vector2(0,0),pygame.math.Vector2(0,0), pygame.math.Vector2(388,(self.player_rect.y+10))
        self.shoot_sound = None
    def parameters(self,delta,surface):
        self.surface = surface
        self.delta = delta
    def shoot_bullet(self):
        if self.shoot: 
            self.bullet_count += 1
            self.shoot = False
            self.current_image = 1
            self.bullet_x = self.player_rect.x + (self.player_width//2) - (self.bult_img.get_width()//2)
            if self.shoot_sound: self.shoot_sound.play()
    def move_bullet(self):
        if not self.shoot:
            self.acc.y = -0.6
            self.velocity_vector.y -= self.acc.y * self.delta
            if self.velocity_vector.y > 3 and self.velocity_vector.y > 0: self.velocity_vector.y = 3
            self.position.y -= (self.velocity_vector.y * self.delta + (self.acc.y * 0.5) * self.delta * self.delta)
            if self.position.y <= 15: self.reload()
        if self.shoot: self.bullet_x = self.player_rect.x + (self.player_width//2) - (self.bult_img.get_width()//2)
    def reload(self):
        self.shoot = True
        self.position.y = self.player_rect.y + 10
        self.current_image = 0
    def set_movement(self, dir):
        if dir == "left": self.move_left, self.move_right = True, False
        elif dir == "right": self.move_left, self.move_right = False, True
        else: self.move_left, self.move_right = False, False
    def movement(self):
        self.acc.x = 0.0
        if self.move_left: self.acc.x -= 1.2
        elif self.move_right: self.acc.x += 1.2
        self.acc.x += self.velocity_vector.x * self.stop_force
        self.velocity_vector.x += self.acc.x * self.delta
        self.limit_vel(4)
        self.position.x += self.velocity_vector.x * self.delta + (self.acc.x * 0.5) * self.delta * self.delta
        self.stop_motion()
        self.player_rect.x = self.position.x
    def limit_vel(self,vel):
        if self.velocity_vector.x > vel and self.velocity_vector.x > 0: self.velocity_vector.x = vel
        if self.velocity_vector.x < -vel and self.velocity_vector.x < 0: self.velocity_vector.x = -1 * vel
        if abs(self.velocity_vector.x) < 0.01: self.velocity_vector.x = 0
    def stop_motion(self):
        if self.position.x <= 40: self.position.x = 41
        elif self.position.x >= 730: self.position.x = 729
    def get_bullet_rect(self):
        y = int(self.position.y)
        r = pygame.Rect(self.bullet_x,y,self.bult_img.get_width(), self.bult_img.get_height())
        return r
    def draw(self):
        self.movement()
        self.move_bullet()
        self.surface.blit(self.bult_img, (self.bullet_x, self.position.y))
        self.surface.blit(self.player_image[self.current_image], (self.player_rect.x, self.player_rect.y))