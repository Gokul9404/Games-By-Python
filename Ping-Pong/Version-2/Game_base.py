import pygame
from pygame import BLEND_RGB_ADD

class Wall():
    def __init__(self,scren,colour=(254,254,254)):
        Coord = {"Top":[25,25,940,10],"Bottum":[25,575,940,10],'Left':[25,25,10,550],'Right':[960,25,10,560]}
        self.color = colour
        self.screen = scren
        self.game_wall = True
        self.Waal, self.Win = [], {}
        for Side in Coord:
            Cord = Coord[Side]
            Rect = pygame.Rect(Cord[0] , Cord[1], Cord[2], Cord[3])
            if Side in ['Left','Right']: self.Win[Side] = Rect
            self.Waal.append(Rect)
        self.centre_wall = pygame.Rect(500,25, 10, 550)
    def Win_wall(self):
        return self.Win.copy()
    def coll_walls(self):
        return self.Waal.copy()
    def Draw(self):
        if self.game_wall:
            pygame.draw.rect(self.screen,self.color,self.centre_wall)
            pygame.draw.circle(self.screen, self.color,(503,300),100,8)
        for wals in self.Waal:
            pygame.draw.rect(self.screen,self.color,wals)

class Paddle():
    def __init__(self,scren,velocity=2,colour=(173,181,189)):
        Coord = {'left':[50,250],'right':[930,250]}
        self.color = colour
        self.screen = scren
        self.Velocity = velocity
        self.Paadls, self.sec_rect ,self.Paadlvlc = {},{}, {}
        for Side in Coord:
            Cord = Coord[Side]
            Cord_X, Cord_Y ,width, height = Cord[0] , Cord[1], 8 , 100
            Rect = pygame.Rect(Cord_X,Cord_Y, width, height)
            rect = pygame.Rect(Cord_X+1,Cord_Y+1, width-2, height-2)
            self.Paadls[Side] ,self.sec_rect[Side] = Rect, rect
            self.Paadlvlc[Side]  = 0    
    def Move_paddle(self,paddle_side,direction):
        if direction == 'up': Velocity = -1*self.Velocity
        else: Velocity = self.Velocity
        self.Paadlvlc[paddle_side] = Velocity
    def check_movement(self,side): 
        Padl = self.Paadls[side]
        pad1 = self.sec_rect[side]
        if (Padl.top < 45 or Padl.bottom > 565):
            self.stop_paddle(side)
            if Padl.top < 45: Padl.top, pad1.top = 46,47
            elif Padl.bottom > 565: Padl.bottom, pad1.bottom= 564, 563
        else: 
            pad1.y += self.Paadlvlc[side]
            Padl.y += self.Paadlvlc[side]
    def stop_paddle(self, paddle_side):
        self.Paadlvlc[paddle_side] = 0 
    def Get_paddle(self):
        return self.Paadls.copy()
    def Draw(self):
        for Padls in self.Paadls:
            self.check_movement(Padls)
            pygame.draw.rect(self.screen,(214,250,238),self.Paadls[Padls])
            pygame.draw.rect(self.screen,self.color,self.sec_rect[Padls])

class Ball():
    def __init__(self, screen, velocity=2):
        self.screen = screen
        self.PositionX, self.PositionY, self.size = 500, 300, 10
        self.velocityx, self.velocityy = velocity, velocity
        self.colour = (200,200,200)
        self.x, self.y = self.PositionX-self.size , self.PositionY-self.size
        self.rect = pygame.Rect(self.x, self.y,2*self.size,2*self.size) 
        self.neon_particle = []
        self.collided = False
    def check_collision(self,paddle,walls,Win_wal,music):
        z = False
        for padl in paddle:
            if (self.rect.x > paddle['left'].x + 4 and self.rect.x < paddle['right'].x + 4):
                r = paddle[padl]
                if self.rect.colliderect(r):
                    if not self.collided:
                        self.velocityx *= -1
                        self.collided , z = True, True 
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.collided: self.collided=False
                self.velocityy *= -1
                z = True
        for win in Win_wal:
            r = Win_wal[win]
            if self.rect.colliderect(r): return str(win)
        if z:
            z = False 
            music.play()
        else: return None
    def Move(self):
        self.PositionX += self.velocityx 
        self.rect.x += self.velocityx
        self.PositionY += self.velocityy
        self.rect.y +=  self.velocityy
    def recenter(self):
        self.PositionX, self.PositionY = 500,300
        self.rect.x, self.rect.y = self.PositionX-self.size , self.PositionY-self.size
    def neon_effect(self):
        x = [self.PositionX,self.PositionY,self.size-0.5]
        self.neon_particle.append(x)
        for partcl in self.neon_particle:
            partcl[2] -= 0.6
            if partcl[2] <= 3: self.neon_particle.remove(partcl)
    def draw_neon_particles(self):
        for particle in self.neon_particle:
            s = int(particle[2]) + 5
            surf = pygame.Surface((s,s))
            pygame.draw.circle(surf, (20,20,20), ( int(particle[2]) , int(particle[2]) ), s)
            surf.set_colorkey((0,0,0))
            self.screen.blit(surf, (particle[0]-s+2, particle[1]-s+2 ), special_flags=BLEND_RGB_ADD)
        for particle in self.neon_particle:
            pygame.draw.circle(self.screen,(230,57,70),(particle[0],particle[1]), int(particle[2])-1)
    def Draw(self):
        self.Move()
        self.neon_effect()
        self.draw_neon_particles()
        pygame.draw.circle(self.screen, (255,255,255),(self.PositionX, self.PositionY), self.size)
