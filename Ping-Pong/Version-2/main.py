import pygame
from pygame import init, time, Surface, BLEND_RGB_ADD
from Game_base import Wall, Paddle , Ball
from text_button import  Show_Text, Button
#=================== Function to Initialise Pygame and to set Caption and Icon ======================
def Initialise(Game,*args):
    global WindowSize
    #====================================== Initialise Pygame =====================================
    init()
    #====================================== Caption and Icon ======================================
    pygame.display.set_caption(Game)
    #====================================== Create the screen =====================================
    Width, Height = 1000, 600
    WindowSize = (Width, Height) 
    Window = pygame.display.set_mode(WindowSize)
    #==================================== Game Surface to render ===================================
    Game_Surface = Surface(WindowSize)
    #============================================ ============== ===================================
    return Window , Game_Surface
#================================= Functions Used to Make Game working ==============================
def Shoow_score():
    global Score_player_1,Score_player_2
    for info in Score:
        s = 'Player '
        if info is 'Right': 
            s += f"1:- {Score[info]}"
            Score_player_1.Update(s)
        else:
            s += f"2:- {Score[info]}"
            Score_player_2.Update(s)
    Score_player_1.Draw()
    Score_player_2.Draw()

def Draw_object(*args):
    for Obeject in args:
        Obeject.Draw()

def Add_points(Player):
    global Score
    Score[Player] += 1 

def Home_screen():
    while True:
        Screen.fill((30,20,60))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Drawing Every Object
        Draw_object(home_wall,start_button,exit_button_home, Home_text,Home_text1)
        
        # Blitting The Game Surface on the Screen
        surf = pygame.transform.scale(Screen, WindowSize)
        Window.blit(surf,(0,0))

        # Keeping the Frame Limiter on , And Updating the Display 
        Clock.tick(FPS) 
        pygame.display.update()

def Game_Screen():
    global WindowSize
    while True:
        Screen.fill((30,20,60))
        Col_wall = walls.coll_walls()
        Col_pad = Paadle.Get_paddle()
        Win_waals = walls.Win_wall()
        Shoow_score()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:          
                if event.key == pygame.K_w: Paadle.Move_paddle('left','up')
                if event.key == pygame.K_s: Paadle.Move_paddle('left','down')      
                if event.key == pygame.K_UP: Paadle.Move_paddle('right','up')
                if event.key == pygame.K_DOWN: Paadle.Move_paddle('right','down')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s: Paadle.stop_paddle('left')
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: Paadle.stop_paddle('right')

        Score_add = ball.check_collision(Col_pad,Col_wall,Win_waals,collid_music)
        # Check to Udate Score
        if Score_add: 
            Add_points(Score_add)
            ball.recenter()

        # Drawing Every Object
        Draw_object(walls, Paadle, ball,home_button,exit_button_game)
        
        # Blitting The Game Surface on the Screen
        surf = pygame.transform.scale(Screen, WindowSize)
        Window.blit(surf,(0,0))

        # Keeping the Frame Limiter on , And Updating the Display 
        Clock.tick(FPS) 
        pygame.display.update()

def exiit():
    pygame.quit()
#============================================ Initialise Game =======================================
Window, Screen = Initialise('Ping-Pong')
#============================================ ============== ========================================
# FPS Setting
Clock = time.Clock()
FPS = 60
#============================================ Walls of the Game =====================================
walls = Wall(Screen)
home_wall =  Wall(Screen)
home_wall.game_wall = False
#========================================== Paddles for the Player ==================================
Paadle = Paddle(Screen,2,(69,123,157))
#============================================ Ball ========================================
ball = Ball(Screen,3)
#============================================= Home Button =========================================
start_button = Button(Screen,(255,255,255),300,400,100,50,'Start',font_colour=(58,12,163),Command=Game_Screen)
exit_button_home = Button(Screen,(208,0,0),600,400,100,50,'Exit',font_colour=(215,38,60),Command=exiit)
#========================================== Game Screen Button ======================================69,123,157
home_button = Button(Screen,(168,218,220),400,3,60,20,'Home',font_colour=(17,138,178),font_size=18,Command=Home_screen)
exit_button_game = Button(Screen,(208,0,0),540,3,60,20,'Exit',font_colour=(215,38,60),font_size=18,Command=exiit)
home_button.main_rect_width, exit_button_game.main_rect_width = 1, 1
#============================================ ============== ========================================
Score = {"Left":0, "Right":0}
Score_player_1 = Show_Text(Screen,"Player 1 : 0",18,(255,220,210),30,3)
Score_player_2 = Show_Text(Screen,"Player 2 : 0",18,(255,220,210),865,3)
#============================================ ============== ========================================
Home_text = Show_Text(Screen,"Ping - Pong",110,(237,242,244),245,150,Font='rage')
Home_text1 = Show_Text(Screen,"By Using Pygame",12,(230,240,245),725,280,Font="rockwell",Italic=True)
#============================================ ============== ======================================== 
collid_music = pygame.mixer.Sound('E:\\Python Programs\\Games\\Ping-Pong\\Version-2\\Bounce-back.wav')
#============================================ ============== ======================================== 
if __name__ == "__main__":
    Home_screen()