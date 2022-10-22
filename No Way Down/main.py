import pygame
import player
from pygame import *
from time import sleep
from Button import PyButton, Hover_button, set_music_path
from Load_map import load_map, load_tiles, set_map_path, total_levels, player_y_of_level
from pygame import K_UP, K_DOWN, K_RIGHT, K_LEFT,K_SPACE,K_UP,K_ESCAPE,K_r,K_a,K_w,K_d,KEYUP,KEYDOWN, QUIT, init, Surface, quit
#============================================ Initialise Pygame ============================================
init()
#============================================ Caption and Icon ============================================
pygame.display.set_caption('No Way Down')
#============================================ Create the screen ============================================
Width, Height = 600, 600
WindowSize = (Width, Height) 
screen = pygame.display.set_mode(WindowSize)
#============================================ Game Surface to render ============================================
Game_Surface = Surface(WindowSize)
#============================================ Path for the assets ============================================
path = "E:/Python Programs/Games/No Way Down/Assets"
#============================================ Player ============================================
img_anim = {"forward":f"{path}/Sprites/Player/forward", "run" : f"{path}/Sprites/Player/run","idle":f"{path}/Sprites/Player/idle"}
img_anim_frame = {"forward":[12,12,12,12], "run" : [12,12,12,12],"idle":[30,30]}
Player = player.Player(img_anim,img_anim_frame)
Player.Load_Animation()
#============================================ Screen Images ============================================
Home_1 = pygame.image.load(f"{path}/Sprites/screen/Home_0.png")
Home_2 = pygame.image.load(f"{path}/Sprites/screen/Home_2.png")
Home_3 = pygame.image.load(f"{path}/Sprites/screen/Home_3.png")
levelup_image = pygame.image.load(f"{path}/Sprites/screen/levelup.png")
win = pygame.image.load(f"{path}/Sprites/screen/win.png")
Home_screen_img = [Home_1, Home_2,Home_3]
#============================================ Music and Sounds ============================================
pygame.mixer.music.load(f"{path}/Music/background.wav")     # Loading Background Music
pygame.mixer.music.play(-1)                                 # Playing Background Music
level_up_music = pygame.mixer.Sound(f"{path}/Music/level_up.wav")
#============================================ ============== ============================================
# FPS Setting
Clock = pygame.time.Clock()
FPS = 60
#============================================ ============== ============================================
# Game Constants and Variables
level = 1
scroll = [64,0]
Levelup, Restart = False, False
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
#============================================ ============== ============================================
def Draw_object(*args):
    for Obeject in args:
        Obeject.Draw()

def Check_Mouse_button_down(*args):
    for Object in args:
        x = Object.Pressed()
        if x: return True
    else: return False

def Hovver(*args):
    n = 0
    for obeject in args:
        x = obeject.Hover()
        n+=1
        if x: return n 
    else: return 0 

def Level_up():
    global level
    while True:
        lvl = total_levels() + 1
        level+=1 
        level = level % lvl
        if level==0:
            end_screen()
            break
        if level!=0: level_upscreen()
        break

def reset():
    global scroll, level
    scroll = [64,0]
    y = player_y_of_level(level)
    Player.reposite(y)

def exiit(): quit()

def Home_screen():
    Font_colour, Hovercolour = (35,35,35),(217,217,217)
    Start = PyButton(screen,"green",150,430,100,50,"Start",'bookmanoldstlye',35,Font_colour,Hovercolour,Command=Game_screen)
    Exitt = PyButton(screen,"red",350,430,100,50,"Exit",'bookmanoldstlye',35,Font_colour,Hovercolour,Command=exiit)
    Controls = Hover_button(screen,"white",510,340,90,20,"Controls",'bookmanoldstlye',25,(220,47,2),bold=True)
    About = Hover_button(screen,"white",510,420,90,20,"About",'bookmanoldstlye',25,(220,47,2),bold=True)
    i = 0
    Pressed = False
    while True:
        if i == 0: screen.blit(Home_screen_img[i],(0,0))
        for event in pygame.event.get():
            if event.type ==QUIT: quit()
        i = Hovver(Controls,About)
        Draw_object(Start,Controls,About,Exitt)
        Pressed =  Check_Mouse_button_down(Start)
        if i != 0: screen.blit(Home_screen_img[i],(0,0))
        if Pressed: break
        pygame.display.update()

def Game_screen():
    global level, scroll, Restart , Levelup
    load_tiles()
    reset()
    player_action = "idle"
    player_frame = 0
    Scroll, qt = False, False
    Restart = False
    Font_colour, Hovercolour = (35,35,35),(217,217,217)
    Home = Hover_button(screen,"white",10,5,50,25,"Home","californianfb",20,Font_colour,Hovercolour,Command=Home_screen)
    Exit = Hover_button(screen,"red",545,5,50,25,"Exit",'bookmanoldstlye',35,(250,25,255),Hovercolour,Command=exiit)
    while True:
        Game_Surface.fill((145,244,255))
        # Load map of the level
        wall_tile , win_tile , win_tile_pos = load_map(Game_Surface,level,scroll)
        # Movement & Events Handling
        for event in pygame.event.get():
            if event.type == QUIT: qt = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: qt = True
                if event.key == K_RIGHT or event.key == K_d:
                    Player.Right, Player.Left, Player.Up =True, False, False
                    player_action = 'run'
                if event.key == K_LEFT or event.key == K_a:
                    Player.Left, Player.Right, Player.Up = True, False, False
                    player_action = 'run'
                if event.key == K_UP or event.key == K_w:
                    Player.Up, Player.Left, Player.Right = True ,False, False
                    player_action = "forward"
                if event.key == K_r: Restart = True
            if event.type == KEYUP:
                if (event.key == K_LEFT) or (event.key == K_RIGHT) or (event.key == K_UP) or  (event.key == K_d) or (event.key == K_a) or (event.key == K_w): 
                    player_action = 'idle'
                    Player.Left, Player.Right, Player.Up = False, False, False
        # Player Movement , Action , Frame, Scroll Handling
        player_frame = Player.Set_draw_para(player_action,player_frame,wall_tile,win_tile,scroll)
        # Check for level finish
        Levelup = Player.Check_for_win()
        Player.draw(Game_Surface)                       
        # Blitting The Game Surface on the Screen
        surf = pygame.transform.scale(Game_Surface, WindowSize)
        screen.blit(surf,(0,0))
        Draw_object(Home,Exit)
        Pressed =  Check_Mouse_button_down(Home)
        # Keeping the Frames on Limit, And Updating the Display  
        Clock.tick(FPS)
        pygame.display.update()
        # Scrolling down the screen, when player reaches top of the game screen
        Pos = Player.get_player_pos()
        if Pos[1] <= 15: Scroll = True                                           # Start Scrolling 
        if Scroll:                                                               # If scrolling check for stop or scroll
            if (Pos[1] >= 576) or (win_tile_pos[1] >= 45): Scroll = False        # Stop Scrolling
            else: scroll[1]+=5                                                     # Scrolling speed  in px
        if Restart or Levelup or Pressed:
            Player.Left, Player.Right, Player.Up = False, False, False
            break
        # Quit the game
        if qt: quit()

def level_upscreen():
    global level
    Font_colour, Hovercolour = (35,35,35),(217,217,217)
    Cont = PyButton(screen,"green",150,450,100,50,"Continue",'bookmanoldstlye',30,Font_colour,Hovercolour)
    Exitt = PyButton(screen,"red",350,450,100,50,"Exit",'bookmanoldstlye',35,Font_colour,Hovercolour,Command=exiit)
    coont = Show_Text(screen,f"You completed level {level} !",30,(255,255,0),170,275)
    level_up_music.play()
    while True:
        screen.blit(levelup_image,(0,0))
        Draw_object(coont,Cont,Exitt)
        for event in pygame.event.get():
            if event.type == QUIT: quit()
        # Keeping the Frames on Limit, And Updating the Display  
        Clock.tick(FPS)
        pygame.display.update()
        if Cont.Pressed(): break

def end_screen():
    Font_colour, Hovercolour = (35,35,35),(217,217,217)
    Home = PyButton(screen,"green",150,430,100,50,"Restart",'bookmanoldstlye',30,Font_colour,Hovercolour,Command=Home_screen)
    Exitt = PyButton(screen,"red",350,430,100,50,"Exit",'bookmanoldstlye',35,Font_colour,Hovercolour,Command=exiit)
    while True:
        screen.blit(win,(0,0))
        for event in pygame.event.get():
            if event.type == QUIT: quit()
        Draw_object(Home,Exitt)
        # Keeping the Frames on Limit, And Updating the Display  
        Clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":    
    set_map_path(path)
    set_music_path(path)
    Home_screen()
    while True:
        if Restart or Levelup:
            if Restart:
                reset()
                Game_screen()
            if Levelup:
                reset()
                Level_up()
                Game_screen()
        else: break