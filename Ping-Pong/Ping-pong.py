import pygame
from time import sleep
from random import randint
from os import path as P
from pygame import mixer
#=======================================================================================================================================
# Initialise Pygame
pygame.init()
# Create the screen
Width, Height = 1000, 600
screen = pygame.display.set_mode((Width, Height))
# Caption and Icon
pygame.display.set_caption('Ping Pong')
#=======================================================================================================================================
# FPS Setting
Clock = pygame.time.Clock()
FPS = 60
# Globally Used Variables
Left , Right = 25, 975
Top , Buttom = 25, 575
MiddleX , MiddleY = Width/2, Height/2
# Globally Used Colours
But_colour , Font_colour, Hovercolour, Exit_Font, BackGround = (241,250,238), (35,35,35),(217,217,217),(230,60,70), (5,16,28)
# Scores
Score_Player1 , Score_Player2 = 0 , 0
# Levels [1,2,3]
Level_Speed = [2,4,6]
Level_thoughness = Level_Speed[0]
Level = ["   Easy","Medium"," Though"]
Level_text = Level[0]
# Themes Colour
themes = {"White":(255,255,255),"Red":(210,60,70),"Blue":(142,202,230),"Yellow":(255,182,2)}
Colours = ["White","Red","Blue","Yellow"]
# Theme variable
thme = "White"
Ball_Colour = Colours[1]
Paddle_Colour = Colours[2]
Colour = [0,1,2,3]

# Basic Path of the Asset File-folder
path = "E:\\Python Programs\\Games\\Ping-Pong"
def import_game_files():
    """Returns True if all the required images and sound effect are imported and available for the game"""
    global path
    i = 0
    try:
        # Icon of the Game
        icon = pygame.image.load(P.join(f"{path}",'Ping-pong.png'))
        pygame.display.set_icon(icon)
        i += 1
        # Sound playing in the Background
        mixer.music.load(P.join(f"{path}","BackgroundMusic.wav"))    
        mixer.music.play(-1)
        i += 1
        if i == 2: return True
    except Exception:
        return False
#Sounds-Music
Bounce = pygame.mixer.Sound(P.join(f"{path}",'Bounce-back.wav'))
#=======================================================================================================================================
# Custom Classes for the Game
# Button
class PyButton():
    """ Used to Create a button with parameters -> colour, x , y, width , height, **text"""
    def __init__(self,Display, colour, x, y, width, height, text="", font_size=30, font_colour=(0,0,0), Hover_colour=None, Outline=False, Outline_Size=None, Outline_colour=None, Command=None):
        self.x, self.y = x, y
        self.window = Display
        self.width, self.height = width, height
        self.text = text
        self.font_size = font_size
        self.font_colour = font_colour
        self.colour = colour
        self.pos = [0,0]
        if Hover_colour:
            self.hover_colour = Hover_colour
        if Outline:
            self.outline = True
            self.Outline_colour = Outline_colour
            self.Outline_Size = Outline_Size
        else:
            self.outline = False
            self.Outline_colour = None
            self.Outline_Size = None
        if Command:
            self.command = Command
    def Draw(self):
        if self.outline:
            pygame.draw.rect(self.window, self.Outline_colour , ((self.x - int(self.Outline_Size/2)),(self.y - int(self.Outline_Size/2)),(self.width + self.Outline_Size),(self.height + self.Outline_Size)))
        if ((self.width + self.x) > self.pos[0] > self.x) and ((self.height + self.y) > self.pos[1] > self.y):
            pygame.draw.rect(self.window, self.hover_colour, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.window, self.colour, (self.x, self.y, self.width, self.height))
        if self.text != "":
            But_font = pygame.font.SysFont('forte',self.font_size)
            But_text = But_font.render(self.text, 1,self.font_colour)
            self.window.blit(But_text,( self.x + (self.width/2 - But_text.get_width()/2),self.y + (self.height/2 - But_text.get_height()/2)))  
    def Pressed(self):
        if ((self.width + self.x) > self.pos[0] > self.x) and ((self.height + self.y) > self.pos[1] > self.y):
            self.command()
            return True
    def get_pos(self,Pos):
        self.pos = Pos
#=======================================================================================================================================
# Ball
class Ball():
    def __init__(self, display, size=0, Velox=0, Veloy=0, typee="", theme=None,Hollow_and_width=None):
        self.display = display
        self.size,  self.Velo = size, Velox
        self.Velox, self.Veloy = Velox, Veloy
        self.PositionX , self.PositionY = MiddleX, MiddleY
        self.type = typee.lower()
        if Hollow_and_width:
            self.Hollow_width = Hollow_and_width
        else:
            self.Hollow_width = None
        if theme: 
            self.colour = themes[theme]
    def Draw(self):
        if self.type == "circle":
            if self.Hollow_width: 
                pygame.draw.circle(self.display, self.colour,(int(self.PositionX), int(self.PositionY)), self.size,self.Hollow_width)
            else:
                pygame.draw.circle(self.display, self.colour,(int(self.PositionX), int(self.PositionY)), self.size)
        else:
            x , y = int(self.PositionX - self.size/2) , int(self.PositionY - self.size/2)
            pygame.draw.rect(self.display, self.colour, (x, y, self.size, self.size))
    def Move(self, Width_of_wall):
        if self.PositionY -  Width_of_wall - self.Velo <= Top or self.PositionY +  Width_of_wall + self.Velo >= Buttom:
            self.Veloy *= -1
        self.PositionX = self.PositionX + self.Velox
        self.PositionY = self.PositionY + self.Veloy  
    def notCollid(self, ColliodX=0, ColliodY=[0,0], Paddle_no=0):
        if ((self.PositionY>=ColliodY[0]) and (int(self.PositionY)<=ColliodY[1])):
            if self.PositionX >= ColliodX - self.Velo and self.PositionX <= ColliodX + self.Velo:
                self.Velox *= -1
                Bounce.play()
                return False
        elif self.PositionX < ColliodX - 10 and  Paddle_no == 1:
            return True
        elif self.PositionX > ColliodX + 10 and  Paddle_no == 2:
            return True
#=======================================================================================================================================
# Paddle
class Paddle():
    def __init__(self, display, Distance, Length, theme=None):
        self.display = display
        self.Veloy = 5
        self.length = Length
        self.P1 = [Distance,  int(MiddleY - Length/2)]
        self.P2 = [Distance,  int(MiddleY + Length/2)]
        self.Dis = Distance
        self.Width = 8
        if theme: 
            self.colour = themes[theme]
    def Draw(self):
        pygame.draw.line(self.display, self.colour, self.P1 , self.P2, self.Width)
    def move(self,Width_of_wall , Mv=0):
        if self.P1[1] >= Top + Width_of_wall +2 and Mv == 1:
            self.P1[1] -= self.Veloy
            self.P2[1] -= self.Veloy
        elif self.P2[1] <= Buttom - Width_of_wall - 2 and Mv == -1:
            self.P1[1] += self.Veloy
            self.P2[1] += self.Veloy
        else:
            self.P2[1] += 0
            self.P1[1] += 0
#=======================================================================================================================================
# Wall 
class Wall():
    def __init__(self, Display, Point1, Point2, width,theme=None):
        self.display = Display
        self.P1 = Point1
        self.P2 = Point2
        self.Width = width
        if theme: 
            self.colour = themes[theme]
        else: 
            self.colour = (255,255,255)
    def Draw(self):
        pygame.draw.line(self.display, self.colour, self.P1 , self.P2, self.Width)
#=======================================================================================================================================
# Text
class Show_Text():
    def __init__(self,Display,Text,Size,Colour,PosX,PosY,Font="georgia",Bold=False,Italic=False):
        self.display = Display
        self.text = Text
        self.Colour = Colour
        self.Posx = PosX
        self.Posy = PosY
        self.font = pygame.font.SysFont(Font, Size ,bold=Bold,italic=Italic)
    def Draw(self):
        txt = self.font.render(self.text,True,self.Colour)
        self.display.blit(txt,(self.Posx,self.Posy))
#=======================================================================================================================================
# Functions to be used in the Game
def Draw_object(*args):
    for Obeject in args:
        Obeject.Draw()

def Give_Mouse_Pos(*args):
    for Button in args:
        Button.get_pos(pygame.mouse.get_pos())

def Check_Pressed(*args):
    for Button in args:
        Button.Pressed()

def add_Score(Player):
    global bal
    a = randint(1,6)
    if a%2==0:
        bal.Velox *= -1   
    bal.PositionX, bal.PositionY = MiddleX, MiddleY
    Player += 1
    return Player
    
def Show_Score():
    global Score_Player1, Score_Player2
    Score1 = Show_Text(screen,f"Score of Player 1:- {Score_Player1}",12,(255,255,0),22,4)  
    Score1.Draw()
    Score2 = Show_Text(screen,f"Score of Player 2:- {Score_Player2}",12,(255,255,0),850,4)  
    Score2.Draw()
    
def Game_Screen():
    global Score_Player1, Score_Player2, Level_thoughness, Wall_width, bal, Wall_width, Top_wall, Buttom_wall,Left_wall , Right_wall,Centre_line,Centre_Circle , Ball_Colour, Paddle_Colour
    bal = Ball(screen, Velox=Level_thoughness, Veloy=Level_thoughness ,size=8,typee="circle",theme=Ball_Colour)   # Ball object  
    Paddle1 = Paddle(screen,50,100,theme=Paddle_Colour)                                                           # Paddle No 1
    Paddle2 = Paddle(screen,950,100,theme=Paddle_Colour)                                                          # Paddle No 1
    PadMv1, PadMv2 = 0,0                                                                                          # Paddle Movement 1  & 2
    Score_Player1,Score_Player2 =0,0
    sleeep = False
    Home_but = PyButton(screen,But_colour,425,2,50,16,"Home",12,Font_colour,Hovercolour,Outline=True,Outline_Size=4,Outline_colour=(75,80,105),Command=Home_Screen)
    exit_but = PyButton(screen,But_colour,525,2,50,16,"Exit",12,Exit_Font,Hovercolour,Outline=True,Outline_Size=4,Outline_colour=(155,40,45),Command=Quit)
    while True:
        screen.fill(BackGround)
        Give_Mouse_Pos(Home_but,exit_but)
        Show_Score()
        sleeep = False
        # Events Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
            if event.type == pygame.KEYDOWN:          
                if event.key == pygame.K_w: PadMv1 = 1
                if event.key == pygame.K_s: PadMv1 = -1      
                if event.key == pygame.K_UP: PadMv2 = 1
                if event.key == pygame.K_DOWN: PadMv2 = -1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s: PadMv1 = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: PadMv2 = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                Check_Pressed(Home_but,exit_but)
        # Moving the Paddle Objects(here the position of object is changing)
        Paddle1.move(Wall_width,Mv=PadMv1)
        Paddle2.move(Wall_width,Mv=PadMv2)
        # Drawing/Displaying Every Object
        Draw_object(Top_wall ,Buttom_wall, Left_wall, Right_wall,Centre_line,Centre_Circle, Paddle1, Paddle2 ,bal, Home_but,exit_but)
        # Check for Collision with Paddles
        # For Paddle No. 1
        Col1 = bal.notCollid(ColliodX=Paddle1.Dis + Paddle1.Width,ColliodY=[int(Paddle1.P1[1]),int(Paddle1.P2[1])],Paddle_no=1)
        if Col1:
            sleeep = True
            Scoreply2 = Show_Text(screen,f"Player 2 Score:-{Score_Player2} + 1",40,(255,255,0),340,280)
            Scoreply2.Draw()
            Score_Player2 = add_Score(Score_Player2)
        # For Paddle No. 1
        Col2 = bal.notCollid(ColliodX=Paddle2.Dis - Paddle2.Width,ColliodY=[int(Paddle2.P1[1]),int(Paddle2.P2[1])],Paddle_no=2)
        if Col2:
            sleeep = True
            Scoreply1 = Show_Text(screen,f"Player 1 Score:-{Score_Player1} + 1",40,(255,255,0),340,280)
            Scoreply1.Draw()
            Score_Player1 = add_Score(Score_Player1)
        # Keeping the Frame Limiter on , And Updating the Display 
        Clock.tick(FPS) 
        pygame.display.update()
        if sleeep: sleep(1)
        bal.Move(Wall_width)            # Moving the ball Objects(here the position of object is changing)

def Home_Screen():
    """Welcome Screen Or Home Screen of the Game"""
    global  Top_wall, Buttom_wall,Left_wall , Right_wall, Level_but
    home_run, exiit = True, False
    Game_run = PyButton(screen,But_colour,250,420,100,50,"start",26,Font_colour,Hovercolour,Outline=True,Outline_Size=6,Outline_colour=(65,60,55),Command=Game_Screen)
    Exit_but = PyButton(screen,But_colour,650,420,100,50,"Exit",26,Exit_Font,Hovercolour,Outline=True,Outline_Size=6,Outline_colour=(255,15,85),Command=Quit)
    Level_but = PyButton(screen,BackGround,382,545,80,24,"        ",16,But_colour,(120,8,6),Outline=True,Outline_Size=2,Outline_colour=But_colour,Command=Set_Level)
    Colour_but1 = PyButton(screen,BackGround,490,545,75,24,"        ",10,But_colour,(221,161,94),Outline=True,Outline_Size=2,Outline_colour=But_colour,Command=Set_BColour)
    Colour_but2 = PyButton(screen,BackGround,575,545,80,24,"        ",16,But_colour,(221,161,94),Outline=True,Outline_Size=2,Outline_colour=But_colour,Command=Set_PColour)
    Home_text = Show_Text(screen,"Ping - Pong",100,Hovercolour,275,180,Font="rage",Italic=True)
    Home_text1 = Show_Text(screen,"By Using Pygame",12,(230,240,245),725,300,Font="rockwell",Italic=True)
    Home_text2 = Show_Text(screen,"Created By:- Gokul",10,(230,240,245),875,555,Font="rockwell")
    Set_text = Show_Text(screen," Difficulty Level               Set Colour  ",15,(140,155,175),375,525,Font="rockwell",Italic=True)
    # Sound playing in the Background
    #pygame.mixer.music.load("E:\\Assets & Extras\\New fold\\PingPong.wav")
    #pygame.mixer.music.play(-1)
    while home_run:
        screen.fill(BackGround)
        Give_Mouse_Pos(Game_run,Exit_but,Level_but,Colour_but1,Colour_but2)
        Draw_object(Top_wall,Buttom_wall,Left_wall,Right_wall,Game_run,Exit_but,Home_text,Home_text1, Home_text2, Set_text,Level_but,Colour_but1,Colour_but2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: home_run, exiit = False, True
            if event.type == pygame.MOUSEBUTTONDOWN:
                Check_Pressed(Game_run,Exit_but, Level_but,Colour_but1,Colour_but2)
        Show_level_and_Colour()
        pygame.display.update()
        if exiit : Quit()

def Show_level_and_Colour():
    global Ball_Colour, Paddle_Colour, Level_text
    a = Show_Text(screen,str(Level_text),15,Hovercolour,395,547,Font="script",Italic=True)
    b = Show_Text(screen,f"B:- {Ball_Colour}",15,(240,35,60),495,547,Font="script",Italic=True)
    c = Show_Text(screen,f"Pd:- {Paddle_Colour}",15,(240,35,60),578,547,Font="script",Italic=True)
    Draw_object(a,b,c)

def Set_Level():
    global Level_thoughness, Level_text, Level_Speed, Level, Level_but
    x, y , l= Level_Speed.index(Level_thoughness), Level.index(Level_text), len(Level_Speed)
    Level_thoughness, Level_text = Level_Speed[(x+1)%l], Level[(y+1)%l]

def Set_BColour():
    global Ball_Colour,  Colours, Colour
    x, l = Colours.index(Ball_Colour), len(Colours)
    Ball_Colour = Colours[(x+1)%l]

def Set_PColour():
    global Paddle_Colour, Colours, Colour
    z,c = Colours.index(Ball_Colour), len(Colours)
    Paddle_Colour = Colours[(z+1)%c]

def Quit(): pygame.quit()
#=======================================================================================================================================
# Basic Structure of the Pool
Wall_width = 10                                                                                         # Width Of Each Wall
Top_wall = Wall(screen,[Left,Top],[Right, Top],Wall_width, thme)                                        # Top wall
Buttom_wall = Wall(screen,[Left,Buttom],[Right, Buttom],Wall_width, thme)                               # Buttom wall
Left_wall = Wall(screen,[Left-4,Top-4],[Left-4,Buttom+(Wall_width/2)],Wall_width, thme)                 # Left wall
Right_wall = Wall(screen,[Right+4,Top-4],[Right+4,Buttom+(Wall_width/2)],Wall_width, thme)              # Right wall
Centre_line = Wall(screen,[MiddleX,Top],[MiddleX,Buttom],int(Wall_width/2),thme)                        # Central line
Centre_Circle = Ball(screen,size=100,typee="circle",theme="White",Hollow_and_width=8)                   # Central Circle
#=======================================================================================================================================
if __name__ == "__main__":    
    if import_game_files(): Home_Screen()