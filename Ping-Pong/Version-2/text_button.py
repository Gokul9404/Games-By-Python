import pygame
from pygame import mouse, BLEND_RGB_ADD

class Show_Text():
    def __init__(self,Display,Text,Size,Colour,PosX,PosY,Font="georgia",Bold=False,Italic=False,Mutable_text=False):
        self.display = Display
        self.text = Text
        self.Colour = Colour
        self.mutable_text = Mutable_text
        self.Posx, self.Posy = PosX, PosY
        self.font = pygame.font.SysFont(Font, Size ,bold=Bold,italic=Italic)
    def Update(self, text):
        self.text = text
    def Draw(self):
        if self.mutable_text is False: self.Update(self.text)
        txt = self.font.render(self.text,True,self.Colour)
        self.display.blit(txt,(self.Posx,self.Posy))

class Button():
    """ Used to Create a button with parameters -> colour, x , y, width , height, **text"""
    def __init__(self,Display, colour, x, y, width, height, text="",font='cooperblack', font_size=30, font_colour=(0,0,0), Hover_colour=None,Fill=True, Command=None,Bold=False):
        self.x, self.y, self.width, self.height= x, y ,width, height
        self.window = Display
        self.colour =  colour
        self.pos = [0,0]
        self.cmd_done, self.pressed = False, False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover_rect = pygame.Rect(0, 0, self.width, self.height)
        self.main_rect_width = 2
        if Hover_colour: self.hover_colour = Hover_colour
        else:  self.hover_colour = colour
        if Command: self.command = Command
        else: self.command = None
        But_font = pygame.font.SysFont(font,font_size, bold=Bold)
        if text != "": self.text = But_font.render(text, 1 ,font_colour)
        else : self.text = None
        self.surf = pygame.Surface((width,height))
        self.surf.set_colorkey((0,0,0))
    def Draw(self):
        self.pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(self.pos[0],self.pos[1], 1, 1)
        self.pressed = pygame.mouse.get_pressed()[0]
        if self.rect.colliderect(mouse_rect):
            pygame.draw.rect(self.surf, (177,167,166), self.hover_rect)
            self.window.blit(self.surf, (self.rect.x,self.rect.y), special_flags=BLEND_RGB_ADD)
            if self.pressed:            
                if self.command: self.command()
                self.cmd_done = True
            else: self.cmd_done = False        
        pygame.draw.rect(self.window, self.colour, self.rect,self.main_rect_width)
        if self.text: self.window.blit(self.text,( self.x + (self.width/2 - self.text.get_width()/2),self.y + (self.height/2 - self.text.get_height()/2)))  
    def Pressed(self):
        if self.cmd_done: return True
        return False