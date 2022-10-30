import pygame
from pygame import mouse
from pygame import mixer

mixer.init()

Colours = {"red":[(255,0,0),(255,77,77),(220,0,0)],"white":[(240,240,240),(250,250,250),(210,215,220)],"green":[(0,255,0),(77,255,77),(38,128,38)]}
path = ""
def set_music_path(paath):
    global path, Pressed_sounnd
    path = paath
    Pressed_sounnd = mixer.Sound(f"{path}/Music/level_up.wav")

class PyButton():
    """ Used to Create a button with parameters -> colour, x , y, width , height, **text"""
    def __init__(self,Display, colour, x, y, width, height, text="",font='bookmanoldstlye', font_size=30, font_colour=(0,0,0), Hover_colour=None,Fill=True, Command=None,bold=False):
        self.Colours = {"red":[(255,0,0),(255,77,77),(204,0,0)],"white":[(240,240,240),(250,250,250),(210,215,220)],"green":[(0,255,0),(94,255,100),(77,210,85)]}
        self.x, self.y = x, y
        self.window = Display
        self.width, self.height = width, height
        self.text , self.font = text, font
        self.font_size, self.font_colour = font_size, font_colour
        self.colour, self.colour1,self.colour2 =  self.Colours[colour][0], self.Colours[colour][1] , self.Colours[colour][2]
        self.pos = [0,0]
        self.bold = bold        
        self.cmd_done, self.pressed = False, False
        self.Fill = Fill
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.hover_colour = Hover_colour if Hover_colour else colour
        if Command: self.command = Command
        else: self.command = None
    
    def Draw(self):
        self.pos = pygame.mouse.get_pos()
        self.mouse_rect = pygame.Rect(self.pos[0], self.pos[1], 1,1)
        if self.rect.colliderect(self.mouse_rect):
            if self.Fill:
                pygame.draw.rect(self.window, self.colour2, pygame.Rect(self.x, self.y, self.width, self.height))
                pygame.draw.rect(self.window, self.colour1, pygame.Rect(self.x, self.y, self.width-3, self.height-3))
                pygame.draw.rect(self.window, self.hover_colour, pygame.Rect(self.x+3, self.y+3, self.width-6, self.height-6))
            self.pressed = pygame.mouse.get_pressed()[0]
            if self.pressed:            
                if self.command: 
                    self.command()
                    Pressed_sounnd.play()
                self.cmd_done = True
            else: self.cmd_done = False
        else:
            if self.Fill:
                pygame.draw.rect(self.window, self.colour2, pygame.Rect(self.x, self.y, self.width, self.height))
                pygame.draw.rect(self.window, self.colour1, pygame.Rect(self.x, self.y, self.width-3, self.height-3))
                pygame.draw.rect(self.window, self.colour, pygame.Rect(self.x+2, self.y+3, self.width-6, self.height-6))        
        if self.text != "":
            But_font = pygame.font.SysFont(self.font,self.font_size, bold=self.bold)
            But_text = But_font.render(self.text, 1 ,self.font_colour)
            self.window.blit(But_text,( self.x + (self.width/2 - But_text.get_width()/2),self.y + (self.height/2 - But_text.get_height()/2)))  

    def Pressed(self):
        if self.cmd_done: return True
        return False

class Hover_button():
    def __init__(self,Display, colour, x, y, width, height, text="",font='bookmanoldstlye', font_size=30, font_colour=(0,0,0), Hover_colour=None,bold=False, Command=None):
        self.x, self.y = x, y
        self.window = Display
        self.width, self.height = width, height
        self.text ,self.font = text, font
        self.font_size, self.font_colour = font_size, font_colour
        self.colour, self.bold = colour, bold
        self.pos = [0,0]
        self.cmd_done = False
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.hover_colour = Hover_colour if Hover_colour else self.colour
        self.command = Command if Command else None
        

    def Draw(self):
        self.pos = pygame.mouse.get_pos()
        But_font = pygame.font.SysFont(self.font,self.font_size, bold=self.bold)
        if self.text != "":
            pressed = pygame.mouse.get_pressed()[0]
            if ((self.width + self.x) > self.pos[0] > self.x) and ((self.height + self.y) > self.pos[1] > self.y) and self.command:
                But_text = But_font.render(self.text, 1 ,self.hover_colour)
                self.window.blit(But_text,( self.x + (self.width/2 - But_text.get_width()/2),self.y + (self.height/2 - But_text.get_height()/2)))
                if pressed: 
                    if self.command: 
                        Pressed_sounnd.play()
                        self.command()
                    self.cmd_done = True
                else: self.cmd_done = False
            else:
                But_text = But_font.render(self.text, 1 ,self.font_colour)
                self.window.blit(But_text,( self.x + (self.width/2 - But_text.get_width()/2),self.y + (self.height/2 - But_text.get_height()/2)))

    def Hover(self):
        self.pos = pygame.mouse.get_pos()
        self.mouse_rect = pygame.Rect(self.pos[0], self.pos[1], 1,1)
        if self.rect.colliderect(self.mouse_rect): return True
        return False
    
    def Pressed(self):
        if self.cmd_done: return True
        return False