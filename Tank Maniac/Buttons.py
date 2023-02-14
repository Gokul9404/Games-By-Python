import pygame
from pygame import mouse, BLEND_RGB_ADD
from pygame import mixer

mixer.init()

Colours = {"red":[(255,0,0),(255,77,77),(220,0,0)],"white":[(240,240,240),(250,250,250),(210,215,220)],"green":[(0,255,0),(77,255,77),(38,128,38)]}
#==================================================================================================
path = "E:/Python Programs/Projects/Self-Projects/Tank_maniac/Assets" 
Button_pressed_sound = mixer.Sound(f"{path}/Music/Button_pressed.wav")
Button_pressed_sound.set_volume(0.4)
Hover_sound = mixer.Sound(f"{path}/Music/hover.wav")
Hover_sound.set_volume(0.2)
#==================================================================================================
class Show_Text():
    def __init__(self,Display,Text,Size,Colour,PosX,PosY,Font="georgia",Bold=False,Italic=False):
        self.display = Display
        self.text = Text
        self.Colour = Colour
        self.Posx,self.Posy = PosX, PosY
        self.font = pygame.font.SysFont(Font, Size ,bold=Bold,italic=Italic)
    
    def Update(self, text):
        self.text = text
    
    def Draw(self):
        self.Update(self.text)
        txt = self.font.render(self.text,True,self.Colour)
        self.display.blit(txt,(self.Posx,self.Posy))

    def Delete(self):
        del self
#==================================================================================================
class Button():
    """ Used to Create a button with parameters -> colour, x , y, width , height, **text"""
    def __init__(self,Display, colour, x, y, width, height, text="",font='rockwell', font_size=30, font_colour=(0,0,0),fill=(177,167,166), Hover_colour=None,Fill=True, Command=None,Bold=False):
        self.x, self.y = x, y
        self.window = Display
        self.width, self.height = width, height
        self.colour =  colour
        self.pos = [0,0]
        self.cmd_done, self.cur_press, self.pressed = False, False, False
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
        self.fill_button = fill

    def Draw(self):
        self.pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(self.pos[0],self.pos[1], 1, 1)
        if self.rect.colliderect(mouse_rect):
            self.cur_press = pygame.mouse.get_pressed()[0]
            pygame.draw.rect(self.surf, self.fill_button, self.hover_rect)
            self.window.blit(self.surf, (self.rect.x,self.rect.y), special_flags=BLEND_RGB_ADD)       
            if self.cur_press:       
                self.pressed = True
                Button_pressed_sound.play()
                if self.command:
                    self.command()
                    self.cmd_done = True
                else: self.cmd_done = False     
        pygame.draw.rect(self.window, self.colour, self.rect,self.main_rect_width)
        if self.text: self.window.blit(self.text,( self.x + (self.width/2 - self.text.get_width()/2),self.y + (self.height/2 - self.text.get_height()/2)))  

    def Pressed(self):
        if self.pressed: return True
        return False
    
    def Delete(self):
        del self
#==================================================================================================
class Hover_button():
    def __init__(self,Display, colour, x, y, width, height, text="",font='bookmanoldstlye', font_size=30, font_colour=(0,0,0), Hover_colour=None,bold=False, Command=None):
        self.x, self.y = x, y
        self.window = Display
        self.width, self.height = width, height
        self.text ,self.font = text, font
        self.font_size, self.font_colour = font_size, font_colour
        self.colour, self.bold = colour, bold
        self.pos = [0,0]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.cmd_done , self.press = False, False
        if Hover_colour: self.hover_colour = Hover_colour
        else: self.hover_colour = Colours[self.colour]
        if Command: self.command = Command
        else: self.command = None
        self.hoverred = 0

    def Draw(self):
        self.pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(self.pos[0],self.pos[1], 1, 1)
        But_font = pygame.font.SysFont(self.font,self.font_size, bold=self.bold)
        if self.text != "":
            pressed = pygame.mouse.get_pressed()[0]
            if self.rect.colliderect(mouse_rect):
                self.hoverred += 1
                if self.hoverred == 1: Hover_sound.play()
                
                But_text = But_font.render(self.text, 1 ,self.hover_colour)
                self.window.blit(But_text,( self.x + (self.width/2 - But_text.get_width()/2),self.y + (self.height/2 - But_text.get_height()/2)))
                if pressed: 
                    self.press = True
                    Button_pressed_sound.play()
                    if self.command:
                        self.command()
                    self.cmd_done = True
                else: self.cmd_done = False
            else:
                self.hoverred = 0
                But_text = But_font.render(self.text, 1 ,self.font_colour)
                self.window.blit(But_text,( self.x + (self.width/2 - But_text.get_width()/2),self.y + (self.height/2 - But_text.get_height()/2)))

    def Hover(self):
        self.pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(self.pos[0],self.pos[1], 1, 1)
        if self.rect.colliderect(mouse_rect): return True
        return False
    
    def Pressed(self):
        if self.press: return True
        return False

    def Delete(self):
        del self
#==================================================================================================