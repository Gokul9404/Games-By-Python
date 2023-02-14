from time import sleep
import pygame
from pygame import BLEND_RGB_ADD
from math import sin, cos, radians, atan2, degrees
#==================================================================================================
path = "E:/Python Programs/Projects/Self-Projects/Tank_maniac/Assets"   # If path changed goto Load_map and set path their too
#==================================================================================================
WID, HIE = 32, 32
def load_burst_animation():
    burst_image = pygame.image.load(f"{path}/Burst/burst.png")
    burst_image_width = burst_image.get_width()
    total_image = burst_image_width // WID
    img_list = []
    for img_no in range(total_image):
        image = pygame.Surface((WID,HIE))
        image.blit(burst_image, (0,0), ( (img_no * WID), 0, WID, HIE) )
        image.set_colorkey((0,0,0))
        img_list.append(image)
    return img_list
#==================================================================================================
class Player:
    def __init__(self,display,initial_x,intial_y,X_limit_left,X_limit_right,X_movement_speed=2,Vessle_rotate_speed=0.5,type_char="player1") -> None:
        self.screen = display
        self.x, self.y = initial_x, intial_y
        self.Movement_speed = X_movement_speed
        self.Player_width, self.Player_height = 60, 40
        self.rect = pygame.Rect(self.x, self.y,self.Player_width,self.Player_height)
        self.left_limit, self.right_limit = X_limit_left, (X_limit_right - self.Player_width)
        
        self.damage_rect = pygame.Rect(self.x, self.y,self.Player_width+2,self.Player_height+2) 
        self.live = True

        self.rotate_speed = Vessle_rotate_speed
        self.angle = 10
        self.shoot_thrust = 5
        
        self.health = 100
        self.play_damage_animation = True
        self.animation_frame = 0
        self.Current_thrust_percnt, self.change_thrust_frame = 0, 0

        self.player_type = type_char
        if self.player_type == 'player1':
            self.lower_angle, self.higher_angle = 10, 60
            self.image = pygame.image.load(f"{path}/Players/player.png")
            self.gun_vessle = pygame.image.load(f"{path}/Players/player_gun.png")
        else:
            self.lower_angle, self.higher_angle = -60, -10
            self.image = pygame.image.load(f"{path}/Players/enemy.png")
            self.gun_vessle = pygame.image.load(f"{path}/Players/enemy_gun.png")   
        self.image = pygame.transform.scale(self.image,(self.Player_width,self.Player_height))
        self.gun_vessle = pygame.transform.scale(self.gun_vessle,(80,15))
        self.burst_animation = load_burst_animation()

    def rotate_gun_vessle(self,direction=""):
        # limiting the angle of the Gun Vessle
        if self.player_type == 'player1':
            if direction == "up": self.angle += self.rotate_speed
            elif direction == "down": self.angle -= self.rotate_speed
        else:
            if direction == "up": self.angle -= self.rotate_speed
            elif direction == "down": self.angle += self.rotate_speed
    
    def _limit_vessle_angle(self):
        # limiting the angle of the Gun Vessle
        if self.angle >= self.higher_angle:
            self.angle = self.higher_angle
        elif self.angle <= self.lower_angle:
            self.angle = self.lower_angle

    def _get_vessle_point(self):
        if self.player_type == 'player1':
            self.image_centre_x = self.x + (self.Player_width - 22)
            self.image_centre_y = self.y + 7
        else:
            self.image_centre_x = self.x + 22
            self.image_centre_y = self.y + 7       
        self.gun_vessle_copy = pygame.transform.rotate(self.gun_vessle, int(self.angle))
        vessle_rect = self.gun_vessle_copy.get_rect()
        vessle_rect.center = (self.image_centre_x, self.image_centre_y)
        return vessle_rect.x, vessle_rect.y
    
    def adjust_shoot_thrust(self,input=0):
        Lower_limit, Higher_limit = 1, 8
        thrust_change_speed = 0.1
        if (input != 0) and (self.change_thrust_frame % 6 == 0):  
            if input == 1: self.shoot_thrust += thrust_change_speed
            elif input == -1: self.shoot_thrust -= thrust_change_speed

        if self.shoot_thrust <= Lower_limit: self.shoot_thrust = Lower_limit
        elif self.shoot_thrust >= Higher_limit: self.shoot_thrust = Higher_limit

        self.shoot_thrust = float( int(self.shoot_thrust * 100) / 100)
        self.Current_thrust_percnt = (self.shoot_thrust ) / Higher_limit
        self.Current_thrust_percnt = int(self.Current_thrust_percnt * 100)
        return str(self.Current_thrust_percnt) 

    def Shoot(self):
        if self.angle > 0: rad = radians(self.angle)
        else: rad = radians( self.angle * -1)
        
        X_power, Y_power = self.shoot_thrust * cos(rad), self.shoot_thrust * sin(rad)
        X_power, Y_power=  float(int(X_power*100)/100),float(int(Y_power*100)/100)
        if self.angle < 0: X_power = X_power * -1
        
        length = self.gun_vessle.get_width() // 2
        x_add = length * cos(rad)
        y_sub = length * sin(rad)
        
        if self.player_type == 'player1': blt_x = self.image_centre_x + x_add
        else: blt_x = self.image_centre_x - x_add
        blt_y = self.image_centre_y - y_sub
        
        return X_power, Y_power, blt_x, blt_y, (self.shoot_thrust*2)
    
    def get_damage(self, damage):
        self.health = self.health - int(damage)

    def player_life_state(self):
        if self.health < 2: self.live = False

    def play_destruction_animation(self):
        destroyed_image = pygame.transform.scale(self.burst_animation[self.animation_frame],(self.Player_width,self.Player_height))
        self.screen.blit( destroyed_image ,(self.x,self.y))
        if (self.change_thrust_frame % 6 == 0):
            self.animation_frame += 1
            if self.animation_frame == len(self.burst_animation):
                self.play_damage_animation = False

    def finished_animation(self):
        if self.play_damage_animation:
            return False
        return True

    def get_rect(self):
        return self.damage_rect

    def get_health(self):
        return self.health

    def get_states(self,angles=False):
        center_coord =  self.rect.center
        player_state = [int(center_coord[0]),int(self.angle*10),int(self.shoot_thrust*10)]
        if angles:
            return [self.lower_angle, self.higher_angle]
        return player_state 

    def Move(self,dir=0):
        if dir!=0:
            if dir == -1: self.x -= self.Movement_speed
            elif dir == 1: self.x += self.Movement_speed

            if self.x >= self.right_limit: self.x = self.right_limit
            elif self.x <= self.left_limit : self.x = self.left_limit 
        self.rect.x = self.x
        self.rect.y = self.y
        self.damage_rect.center = self.rect.center 

    def Draw(self):
        self.change_thrust_frame += 1  
        self.player_life_state()
        if self.live:
            self._limit_vessle_angle()
            X, Y = self._get_vessle_point()
            self.screen.blit(self.gun_vessle_copy, (X, Y))
            self.screen.blit( self.image ,(self.x,self.y))
        else:
            self.play_destruction_animation()
        if (self.change_thrust_frame % 6 == 0):
            self.change_thrust_frame = 0 
        
    def Delete(self):
        del self
#==================================================================================================
class Cannon_ball():
    def __init__(self, screen):
        self.screen = screen
        self.PositionX, self.PositionY = 500, 300
        self.cur_pos_x, self.cur_pos_y = float(self.PositionX), float(self.PositionY)
        self.velocityx, self.velocityy = 0.0, 0.0
        self.gravity = 0.08
        self.colour = (200,200,200)
        
        self.size = 5
        self.burst = False
        self.framee = 0
        
        self.theta, self.anglee = 0.0, 0
        self.cannon_image = pygame.image.load(f"{path}/Players/Cannon.png")
        self.image_width , self.image_height = self.cannon_image.get_width(), self.cannon_image.get_height()
        self.image_rect = pygame.Rect(0,0, self.image_width, self.image_width) 

        self.path_trace_particles = []
        self.should_move = True
        
        self.burst_animation = load_burst_animation()
        self.play_burst_animation, self.finished = False, False
        self.animation_frame = 0

    def set_velocity(self,x,y):
        self.velocityx = x
        self.velocityy = (-1 * y)
        self.burst, self.finished = False, False
        self.path_trace_particles = []

    def Move(self):
        self.PositionX = int(self.cur_pos_x)
        self.PositionY =  int(self.cur_pos_y)
        self.cur_pos_x += self.velocityx
        self.cur_pos_y += self.velocityy
        self.velocityy += self.gravity

        self.theta = atan2(self.velocityy,self.velocityx)
        self.anglee = int(degrees(self.theta))

    def stop(self):
        self.cur_pos_x, self.cur_pos_y = 1000,1000
        self.should_move = False
    
    def set_position(self,x,y):
        self.should_move = True
        self.cur_pos_x, self.cur_pos_y = x, y

    def Position(self):
        return self.PositionX, self.PositionY

    def check_collision(self,turn,player_rects=[],rects=[]):
        if not self.burst:
            collided_ply = -1
            turn_no = turn - 1
            if self.image_rect.colliderect(player_rects[turn_no]):
                turn_no *= -1
                collided_ply = turn_no
                self.burst = True
            if rects:
                for r in rects:
                    if self.image_rect.colliderect(r):
                        self.burst = True
            return collided_ply, self.burst, self.finished
        return -1, self.burst, self.finished
        
    def path_traceses(self):
        part_x, part_y = self.image_rect.center
        particle = [part_x,part_y,self.size]
        self.path_trace_particles.append(particle)
        
        for partcl in self.path_trace_particles:
            partcl[2] -= 0.1
            if partcl[2] <= 3.5: self.path_trace_particles.remove(partcl)
    
    def draw_path_traceses(self):
        for particle in self.path_trace_particles:
            s = int(particle[2]) + 5
            surf = pygame.Surface((s,s))
            pygame.draw.circle(surf, (20,20,15), ( int(particle[2]) , int(particle[2]) ), s)
            surf.set_colorkey((0,0,0))
            self.screen.blit(surf, (particle[0]-s+2, particle[1]-s+2 ), special_flags=BLEND_RGB_ADD)

    def collide_animation(self):
        if self.burst:        
            self.play_burst_animation = True
            self.should_move = False
            if self.play_burst_animation and (not self.finished):
                self.screen.blit(self.burst_animation[self.animation_frame], self.image_rect.center) 
            self.framee += 1

            if (self.framee % 8 == 0):
                self.framee = 0
                if self.play_burst_animation:
                    self.animation_frame += 1
                    if self.animation_frame == (len(self.burst_animation) - 1):
                        self.finished = True
                    if self.animation_frame == len(self.burst_animation):
                        self.animation_frame = 0
                        self.play_burst_animation, self.burst = False, False
                        self.stop()
            
    def rotate_cannon_ball(self):
        self.cannon = pygame.transform.rotate(self.cannon_image, int(-1* self.anglee))
        self.image_rect = self.cannon.get_rect()
        self.image_rect.center = (self.PositionX, self.PositionY)

    def Draw(self):
        if self.burst:
            self.collide_animation()
        if self.should_move:
            self.Move()
            self.rotate_cannon_ball()
            self.path_traceses()
            self.draw_path_traceses()
            self.screen.blit(self.cannon,(self.image_rect.x, self.image_rect.y))
    
    def Delete(self):
        del self
#==================================================================================================