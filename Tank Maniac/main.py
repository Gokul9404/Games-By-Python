import pygame

from pygame import *
from pygame import mixer
from pygame import K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_UP, K_ESCAPE, K_BACKSPACE
from pygame import K_q, K_s, K_a, K_d, K_h, KEYUP, KEYDOWN, QUIT, init, Surface

from Buttons import Hover_button, Button, Show_Text
from Game_player import Player, Cannon_ball
from Platform_loader import Tiles

from random import randint
#============================================ Initialise Pygame ============================================
init()
mixer.init()
#============================================ Path for the assets =================================
path = "E:/Python Programs/Games on PC/Tank_maniac/Assets"   # If path changed goto Load_map and set path their too
#============================================ Create the screen ============================================
Width, Height = 912, 504
WindowSize = (Width, Height) 
screen = pygame.display.set_mode(WindowSize)
icon = pygame.image.load(f"{path}/icon.png")
pygame.display.set_icon(icon)
#============================================ Caption and Icon =============================================
pygame.display.set_caption('Tank Battle')
#============================================ Game Surface to render =======================================
Game_Surface = Surface(WindowSize)
#============================================ ============== ======================================
# FPS Setting
Clock = pygame.time.Clock()
FPS = 60
#==================================================================================================
burst_music = mixer.Sound(f"{path}/Music/burst_sound.wav")   
shoot_music = mixer.Sound(f"{path}/Music/shoot_music.wav")
shoot_music.set_volume(0.4)
burst_music.set_volume(0.4)
# Playing the Background Music
mixer.music.load(f"{path}/Music/background_music.mp3")
mixer.music.set_volume(0.2)
mixer.music.play(-1)
#==================================================================================================
BG = (110,110,110)
BACK_IMAGE =  pygame.image.load(f"{path}/background/background.png").convert_alpha()
BACK_IMAGE = pygame.transform.scale(BACK_IMAGE,(Width,Height))
WINNER = ""
MODE_TYPE = "oneplayer"
exit_func_loop = False
#==================================================================================================
def exiit():
    """ Will set the Exit_fun_loop value -> True; thus the game will be finished/destroyed """
    global exit_func_loop
    exit_func_loop = True

def Hovver(*args):
    """Will check whether the Mouse pointer is on Hover Button or not 
    Returns:
        True: If mouse is on any hover buton
    """
    n = 0
    for object in args:
        x = object.Hover()
        n+=1
        if x: return n 
    else: return 0 

def Draw_object(*args):
    """ Will Draw all the Object entity that are passed into the Arguments; Drawing of Object depends on the game-surface given to them at initialisation
    """
    for Object in args:
        Object.Draw()

def Del_objects(*args):
    """ Will Delete all the Object entity that are passed into the Arguments.
    """
    for Obeject in args:
        Obeject.Delete()
    
def Check_Mouse_button_down(*args):
    """ Will check whether the button is Pressed or not;
    Returns:
        True: if any Button pressed
    """
    for Object in args:
        x = Object.Pressed()
        if x: return True
    else: return False
#==================================================================================================
def collision_check_rect(player1 : Player, player2 : Player):
    """
    Args:
        player1 , player2 : Player class entity from 'the_player' module
    Returns:
        List of the Rect of the Players
    """
    rect_list = []
    rect_list.append(player1.get_rect())
    rect_list.append(player2.get_rect())
    return rect_list
#==================================================================================================
def Enemy_controls(list_of_state : list, State_to_do : list, shoot : bool):
    """ Generates the Controls for the Enemy [to move, rotate it's vessle, and change it's thrust]
    Args:
        list_of_state [list]: the current state of the Enemy
        State_to_do [list]: the state of Enemy to be set
        shoot : the current value of shoot in the function
    Returns:
        [List]: Automated-Controls list for the Enemy (Played by Comp.)
    """
    [Center, angle, thrust_per] = list_of_state
    [set_Center_x, set_angle, set_thrust_per] = State_to_do
    [Vessle_Rotating_direction, Movement_direction, change_shoot_thrust] = [0, 0, 0]
    C, A, T= True, True, True
    
    if (Center != set_Center_x):
        if Center> set_Center_x: Movement_direction = -1
        elif Center < set_Center_x: Movement_direction = 1
    else: C = False
    
    if angle < 0:
        angle *= -1
        set_angle *= -1    
    if (angle != set_angle):
        if angle > set_angle: Vessle_Rotating_direction = -1
        elif angle < set_angle: Vessle_Rotating_direction = 1
    else: A = False
    
    if (thrust_per != set_thrust_per):
        if thrust_per > set_thrust_per : change_shoot_thrust = -1
        elif thrust_per < set_thrust_per : change_shoot_thrust = 1
    else: T = False

    z = (C == A == T == False)
    if z: shoot = True
    return  [Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, shoot]
#==================================================================================================
def Generate_controls(anglee : list):
    """When their is Chance of Comp./Automated Enemy
        it will generate the random Value for the Enemy to be done
    Args:
        anglee: List of Max. and Min. andgle of the Enemy 

    Returns:
        State_to_do [list]: The state to which the Enemy have to obtain for it's next Shoot
    """
    lower , higher = anglee
    set_Center_x = randint(540,820)
    set_angle = randint(lower*10, higher*10)
    set_thrust = randint(40, 75)

    if (set_Center_x % 5 != 0): 
        x = set_Center_x//5
        set_Center_x = x * 5 
    if (set_Center_x % 2 == 1): set_Center_x -= 1

    if (set_thrust % 2 == 0): set_thrust = set_thrust - 1

    if (set_angle % 5 != 0): 
        set_angle = (set_angle//5) * 5

    return [set_Center_x, set_angle, set_thrust]
#==================================================================================================
def game_requirements():
    """
    Returns:
        [list]: Assets list required for the Game-screen [include home/exit button, Players; their health-status,power status bars]
    """
    Home_but = Hover_button(Game_Surface,"white",20,10,90,20,"Home",'Georgia',20,(255,55,55),Hover_colour=(212,21,24),bold=True)   #,(200,37,2)
    Exit_but = Hover_button(Game_Surface,"white",800,10,90,20,"Exit",'Georgia',20,(255,55,55),Hover_colour=(255,5,5),bold=True,Command=exiit)   #,(200,37,2)
    
    health_bar_color = (90,100,80)
    plyr = Player(Game_Surface,90,350,40,400,type_char='player1')
    health_show_1 = Show_Text(Game_Surface,f"Health Player 1:{plyr.get_health()}",18,health_bar_color,20,50,'Georgia')
    enmy = Player(Game_Surface,750,350,512,872,type_char='player2')
    health_show_2 = Show_Text(Game_Surface,f"Health Player 2 :{enmy.get_health()}",18,health_bar_color,720,50,'Georgia')
    
    Players = [plyr, enmy]
    Turn_no = 0

    Cannon = Cannon_ball(Game_Surface)
    Cannon.stop()
    play_burst_music = True
    sht_per = '0'
    Shoot_thrust_percent = Show_Text(Game_Surface,sht_per,34,(68,69,92),360,10,'forte')

    platform = Tiles(Game_Surface)

    quit_count = 0
    exit_func_loop, shoot, shooted = False, False, False
    wait_over = True
    Vessle_Rotating_direction, Movement_direction, change_shoot_thrust = 0, 0, 0
    return [Home_but, Exit_but, plyr, health_show_1, enmy, health_show_2, Players, Turn_no, Cannon, sht_per, Shoot_thrust_percent, quit_count, shoot, shooted, wait_over, exit_func_loop, play_burst_music, Vessle_Rotating_direction, Movement_direction, change_shoot_thrust,platform]
#==================================================================================================
def controls(Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, quit_count, wait_over, exit_func_loop, shoot):
    """ Func that used will take Commands from the Players(s) 
    
    Returns:
        list of command that are generated by user
    """
    shoot, Go_to_home = False, False
    for event in pygame.event.get():
        if event.type ==QUIT: exit_func_loop = True
        
        if event.type == KEYDOWN:
            if event.key == K_q: 
                exit_func_loop = True if quit_count == 2 else False 
            if wait_over and (WINNER == ""):
                if event.key == K_LEFT: Movement_direction = -1
                if event.key == K_RIGHT: Movement_direction = 1

                if event.key == K_UP: Vessle_Rotating_direction = 1
                if event.key == K_DOWN: Vessle_Rotating_direction = -1

                if event.key == K_a: change_shoot_thrust = -1
                if event.key == K_d: change_shoot_thrust = 1

        if event.type == KEYUP:
            if event.key == K_h: Go_to_home = True

            if event.key == K_q: quit_count += 1

            if (event.key == K_LEFT) or (event.key == K_RIGHT): Movement_direction = 0
            if (event.key == K_UP) or (event.key == K_DOWN): Vessle_Rotating_direction = 0
            if (event.key == K_a) or (event.key == K_d): change_shoot_thrust = 0

            if event.key == K_SPACE: 
                if wait_over: shoot = True

    return [ [Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, shoot], [quit_count, wait_over, exit_func_loop, Go_to_home] ]
#==================================================================================================
def One_player_mode():
    """ Game-Function used for only Single Player game"""
    global WINNER, exit_func_loop
    WINNER = ""
    Game_assests = game_requirements()
    Home_but, Exit_but, plyr, health_show_1, enmy, health_show_2, Players, Turn_no,  Cannon, sht_per, Shoot_thrust_percent, quit_count, shoot, shooted, wait_over, exit_func_loop, play_burst_music, Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, platform = Game_assests
    platform.load_level()
    Game_assests = []
    Player_Can_shoot = True
    Enemy_can_shoot = True
    State_to_do = [0, 0, 0]
    #=============================================================================================
    Go_to_home, Go_to_win_screen, Go_home_screen = False, False, False
    #==============================================================================================
    while True:
        # Game_Surface.fill(BG)
        Game_Surface.blit(BACK_IMAGE,(0,0))
        # Taking Input from the Player 
        Game_Controlls = controls(Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, quit_count, wait_over, exit_func_loop, shoot)
        if Player_Can_shoot and (Turn_no == 0):
            [Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, shoot], [quit_count, wait_over, exit_func_loop, Go_home_screen] = Game_Controlls
        else:
            _ ,  [quit_count, wait_over, exit_func_loop, Go_home_screen] = Game_Controlls
        #==========================================================================================
        if Turn_no == 1:
            [Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, shoot] = Enemy_controls(Players[Turn_no].get_states(),State_to_do,shoot)
            if shoot: Player_Can_shoot = True
        #==========================================================================================
        if exit_func_loop: break
        #==========================================================================================
        if shoot and ((Player_Can_shoot and Turn_no==0) or (Player_Can_shoot and Enemy_can_shoot)):
            X_thrust, Y_thrust, blt_x, blt_y, shot_power = Players[Turn_no].Shoot()
            Cannon.set_velocity(X_thrust,Y_thrust)
            Cannon.set_position(blt_x,blt_y)
            shoot, wait_over = False, False
            shooted, play_burst_music = True, True
            shoot_music.play()  
            if Turn_no == 0: Genrate_Enemy_controls = True
            if Enemy_can_shoot: Enemy_can_shoot = False
        #==========================================================================================
        else:
            # Checking for collision
            Damage_plyr_no, bursted, cannon_fin = Cannon.check_collision(Turn_no,collision_check_rect(plyr,enmy),platform.get_tile_rect() )
            
            if Damage_plyr_no != -1:
                Players[Damage_plyr_no].get_damage(shot_power)
                ply1 = plyr.get_health()
                ply2 = enmy.get_health()
                health_show_1.Update(f"Health Player 1:{ply1}")
                health_show_2.Update(f"Health Player 2:{ply2}")
                if ply1 < 2: WINNER = "Player 2"
                elif ply2 < 2: WINNER = "Player 1"
                if WINNER: wait_over = True

            if bursted:
                if play_burst_music:
                    burst_music.play()
                    play_burst_music = False
                if cannon_fin: wait_over = True
            
            if (wait_over and shooted) :
                Turn_no += 1
                Turn_no = Turn_no % len(Players)
                if Turn_no == 0: Player_Can_shoot = True  
                elif Turn_no == 1:
                    Player_Can_shoot = False
                    if Genrate_Enemy_controls:
                        Enemy_can_shoot = True
                        State_to_do = Generate_controls(Players[Turn_no].get_states(True) )
                        Genrate_Enemy_controls = False
                shooted = False  
            #======================================================================================
            if Vessle_Rotating_direction == 1 : Players[Turn_no].rotate_gun_vessle('up')
            elif Vessle_Rotating_direction == -1 :  Players[Turn_no].rotate_gun_vessle('down')
            Players[Turn_no].Move(Movement_direction)
            sht_per = f"Power :- {Players[Turn_no].adjust_shoot_thrust(change_shoot_thrust)}"
            Shoot_thrust_percent.Update(sht_per)
        #==========================================================================================
        # Drawing he players and the oblect of the level
        Draw_object(platform,Home_but,Exit_but,plyr,enmy,Cannon,Shoot_thrust_percent,health_show_1,health_show_2)
        #==========================================================================================
        # Keeping the Frames on Limit, And Updating the Display  
        Clock.tick(FPS)
        # Updating the Game Surface/Screen
        if not exit_func_loop: screen.blit(Game_Surface,(0,0))
        pygame.display.update()
        #==========================================================================================
        if WINNER:
            fin = Players[Turn_no].finished_animation()
            if fin: Go_to_win_screen = True
        #==========================================================================================
        Go_to_home =  (Check_Mouse_button_down(Home_but) or Go_home_screen)
        #==================================================================================================
        if exit_func_loop or Go_to_home or Go_to_win_screen: 
            Del_objects(Home_but,Exit_but,plyr,enmy,health_show_1,health_show_2,Cannon,Shoot_thrust_percent,platform)
        #==========================================================================================
        if Go_to_home: Home_screen()
        if Go_to_win_screen: win_screen()
        #==========================================================================================
        if exit_func_loop or Go_to_home or Go_to_win_screen: break
#==================================================================================================
def double_player_offline():
    """ Game function used for Two-Players Game """
    global WINNER, exit_func_loop
    WINNER = ""
    Game_assests = game_requirements()
    Home_but, Exit_but, plyr, health_show_1, enmy, health_show_2, Players, Turn_no,  Cannon, sht_per, Shoot_thrust_percent, quit_count, shoot, shooted, wait_over, exit_func_loop, play_burst_music, Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, platform = Game_assests
    Game_assests = []
    platform.load_level()
    #=============================================================================================
    Go_to_home, Go_to_win_screen, Go_home_screen = False, False, False
    #==============================================================================================
    while True:
        Game_Surface.blit(BACK_IMAGE,(0,0))
        # Taking Input from the Player(s)
        Game_Controlls = controls(Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, quit_count, wait_over, exit_func_loop, shoot)
        [Vessle_Rotating_direction, Movement_direction, change_shoot_thrust, shoot], [quit_count, wait_over, exit_func_loop, Go_home_screen] = Game_Controlls
        #==========================================================================================
        if shoot:
            X_thrust, Y_thrust, blt_x, blt_y, shot_power = Players[Turn_no].Shoot()
            Cannon.set_velocity(X_thrust,Y_thrust)
            Cannon.set_position(blt_x,blt_y)
            shoot, wait_over = False, False
            shooted, play_burst_music = True, True
            shoot_music.play()
        #==========================================================================================
        else:
            # Checking for collision
            Damage_plyr_no, bursted, cannon_fin = Cannon.check_collision(Turn_no,collision_check_rect(plyr,enmy),platform.get_tile_rect())
            #======================================================================================
            if Damage_plyr_no != -1:
                Players[Damage_plyr_no].get_damage(shot_power)
                ply1 = plyr.get_health()
                ply2 = enmy.get_health()
                health_show_1.Update(f"Health Player 1:{ply1}")
                health_show_2.Update(f"Health Player 2:{ply2}")

                if ply1 < 2: WINNER = "Player 2"
                elif ply2 < 2: WINNER = "Player 1"
                if WINNER: wait_over = True

            if bursted:
                if play_burst_music:
                    burst_music.play()
                    play_burst_music = False
                if cannon_fin: wait_over = True
            
            if (wait_over and shooted) :
                Turn_no += 1
                Turn_no = Turn_no % len(Players)
                shooted = False
            #======================================================================================
            if Vessle_Rotating_direction == 1 : Players[Turn_no].rotate_gun_vessle('up')
            elif Vessle_Rotating_direction == -1 :  Players[Turn_no].rotate_gun_vessle('down')
            Players[Turn_no].Move(Movement_direction)
                
            sht_per = f"Power :- {Players[Turn_no].adjust_shoot_thrust(change_shoot_thrust)}"
            Shoot_thrust_percent.Update(sht_per)
        #==========================================================================================
        # Drawing he players and the oblect of the level
        Draw_object(platform,Home_but,Exit_but,plyr,enmy,Cannon,Shoot_thrust_percent,health_show_1,health_show_2)
        #==========================================================================================
        # Keeping the Frames on Limit, And Updating the Display  
        Clock.tick(FPS)
        # Updating the Game Surface/Screen
        if not exit_func_loop: screen.blit(Game_Surface,(0,0))
        pygame.display.update()
        #==========================================================================================
        if WINNER:
            fin = Players[Turn_no].finished_animation()
            if fin: Go_to_win_screen = True
        #==========================================================================================
        Go_to_home =  (Check_Mouse_button_down(Home_but) or Go_home_screen)
        #==========================================================================================
        if exit_func_loop or Go_to_home or Go_to_win_screen: 
            Del_objects(Home_but,Exit_but,plyr,enmy,health_show_1,health_show_2,Cannon,Shoot_thrust_percent,platform)
        #==========================================================================================
        if Go_to_home: Home_screen()
        if Go_to_win_screen: win_screen()
        #==========================================================================================
        if exit_func_loop or Go_to_home or Go_to_win_screen: break
#==================================================================================================
def game_screen():
    """ Will use Game-Mode-Function according to Mode_type selected by the Player(s) """
    global WINNER
    WINNER = ""

    if MODE_TYPE == 'oneplayer':
        One_player_mode()

    elif MODE_TYPE == 'twoplayers':
        double_player_offline()
#==================================================================================================
def set_game_mode():
    """Game-Screen used to set the Game-Mode according to the Player(s)"""
    global MODE_TYPE, exit_func_loop
    
    def One_Player_offline():
        global MODE_TYPE
        MODE_TYPE = 'oneplayer'
    
    def Two_Player_offline():
        global MODE_TYPE
        MODE_TYPE = 'twoplayers'
    #==============================================================================================
    # Game name text that to be shown in the Home Screen
    gmtxt = '- Tank Battle -'
    Game_nm_text = Show_Text(Game_Surface,gmtxt,70,(20,20,20),240,130,'forte')
    #==============================================================================================
    Font_sizze = 24
    Font_type = 'Georgia'
    Font_colour = (144,106,80)
    Hover_color =(120,80,60)
    #==============================================================================================
    option_text = Show_Text(Game_Surface,'Select a mode',30,(120,80,60),330,300,Font_type,Bold=True,Italic=True)
    set_one_player = Hover_button(Game_Surface,"white",350,360,180,20,"Single Player",Font_type,Font_sizze,Font_colour,Hover_colour=Hover_color,bold=True,Command=One_Player_offline)
    set_two_offline = Hover_button(Game_Surface,"white",350,410,180,20,"Double Players",Font_type,Font_sizze,Font_colour,Hover_colour=Hover_color,bold=True,Command=Two_Player_offline)
    #==============================================================================================
    quit_count = 0
    Pressed, exit_func_loop = False, False
    Go_to_home, One_player_game, Two_player_game = False, False, False
    #==================================================================================================
    while True:
        Game_Surface.blit(BACK_IMAGE,(0,0))
        Pressed =  Check_Mouse_button_down(set_one_player, set_two_offline)
        #==========================================================================================
        # Taking the input from the user
        for event in pygame.event.get():
            if event.type ==QUIT: exit_func_loop = True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    if quit_count == 2: exit_func_loop = True
            if event.type == KEYUP:
                if event.key in [K_d,K_s]: exit_func_loop, Pressed = True, True
                if event.key == K_s: One_player_game = True
                if event.key == K_d: Two_player_game = True
                
                if event.key == K_h:
                    exit_func_loop ,Go_to_home = True, True
                if event.key == K_q: quit_count += 1
        #==========================================================================================
        Draw_object(set_one_player, set_two_offline,Game_nm_text,option_text)
        #==========================================================================================
        # Keeping the Frames on Limit, And Updating the Display  
        Clock.tick(FPS)
        # Updating the Game Surface/Screen
        if not exit_func_loop: screen.blit(Game_Surface,(0,0))
        pygame.display.update()
        #==================================================================================================
        if exit_func_loop or Pressed or Go_to_home or One_player_game or Two_player_game:
            Del_objects(set_one_player, set_two_offline,Game_nm_text,option_text)
        #==========================================================================================
        if Go_to_home: Home_screen()
        if One_player_game: One_Player_offline()
        if Two_player_game: Two_Player_offline()
        if Pressed: game_screen()
        #==========================================================================================
        if exit_func_loop or Pressed or Go_to_home or One_player_game or Two_player_game: break   
#==================================================================================================
def Home_screen():
    """ Home Screen of the Game """
    global exit_func_loop
    Font_colour = (55,55,55)
    # Game name text that to be shown in the Home Screen
    gmtxt = '- Tank Battle -'
    Game_nm_text = Show_Text(Game_Surface,gmtxt,70,(20,20,20),240,130,'forte')
    #==============================================================================================
    Start = Button(Game_Surface,(200,200,200),290,370,120,45,"Start",'bookmanoldstlye',35,Font_colour,(15,18,25))
    Exitt = Button(Game_Surface,(250,70,70),460,370,120,45,"Exit",'bookmanoldstlye',35,Font_colour,(250,0,0),Command=exiit)
    #==============================================================================================
    Control_color = (68,69,92)
    control_x = 230
    control_font_type = 'Georgia'
    # Hover Button --> If mouse hover on this button Below written Controls will be Shown in the Screen
    Show_Control = Hover_button(Game_Surface,"white",400,435,90,20,"Controls",'Georgia',20,Font_colour,bold=True)   #,(200,37,2)
    # Controls texts
    ply_m = "Player & Gun Vessle Movements "
    ply = Show_Text(Game_Surface,ply_m,32,Control_color,190,80,Bold=True)
    Player_movement = "To Move :- Left/Right arrow key"
    Plyr_movmnt_show = Show_Text(Game_Surface,Player_movement,24,Control_color,control_x,140,control_font_type)
    vssl_movmnt = "Vessle Movement :- UP/DOWN arrow key"
    vssl_movmnt_show = Show_Text(Game_Surface,vssl_movmnt,24,Control_color,control_x,185,control_font_type)
    power_chng = "Adjust Shoot Power :-  'A' / 'D' keys"
    Change_power_show = Show_Text(Game_Surface,power_chng,24,Control_color,control_x,230,control_font_type)
    go_home_shortcut = "Home shortcut :- 'H' key"
    go_home_shortcut_show = Show_Text(Game_Surface,go_home_shortcut,24,Control_color,control_x,275,control_font_type)
    sht = "Space Bar: To-Shoot/Start Game"
    shoot = Show_Text(Game_Surface,sht,24,Control_color,control_x,320,control_font_type)
    qgt = "To exit :- Press 'Q'--> 3 Times"
    qgt_s = Show_Text(Game_Surface,qgt,24,Control_color,control_x,365,control_font_type)
    #==============================================================================================
    i, quit_count = 0, 0
    Pressed, exit_func_loop, Go_to_set_game_mode = False, False, False
    #==============================================================================================
    while True:
        Game_Surface.blit(BACK_IMAGE,(0,0))
        i = Hovver(Show_Control)
        if i == 0:
            Draw_object(Start,Show_Control,Exitt,Game_nm_text)
            Pressed =  Check_Mouse_button_down(Start)
        else:
            Draw_object(ply,Plyr_movmnt_show,Change_power_show,vssl_movmnt_show,go_home_shortcut_show,shoot,qgt_s)
        #==========================================================================================
        # Taking the input from the user
        for event in pygame.event.get():
            if event.type ==QUIT: exit_func_loop = True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    if quit_count == 2: exit_func_loop = True
            if event.type == KEYUP:
                if event.key == K_SPACE: exit_func_loop, Go_to_set_game_mode = True, True
                if event.key == K_q: quit_count += 1
        #==========================================================================================
        # Keeping the Frames on Limit, And Updating the Display  
        Clock.tick(FPS)
        # Updating the Game Surface/Screen
        if not exit_func_loop:screen.blit(Game_Surface,(0,0))
        pygame.display.update()
        #==========================================================================================
        Go_to_set_game_mode = (Pressed or Go_to_set_game_mode)
        #==========================================================================================
        if exit_func_loop or Go_to_set_game_mode: 
            Del_objects(ply,Plyr_movmnt_show,Change_power_show,vssl_movmnt_show,go_home_shortcut_show,shoot,qgt_s,Start,Show_Control,Exitt,Game_nm_text)
        #==========================================================================================
        if Go_to_set_game_mode: set_game_mode()
        #==========================================================================================
        if exit_func_loop or Go_to_set_game_mode: break
#==================================================================================================
def win_screen():
    """ Win-Screen of the Game """
    global WINNER, exit_func_loop
    Font_colour = (55,55,55)
    # Game name text that to be shown in the Home Screen
    winnertext = f"Winner is :- {WINNER}"
    winner_text_show = Show_Text(Game_Surface,winnertext,70,(60,60,80),170,140,'forte')
    #==============================================================================================
    Home_but = Button(Game_Surface,(200,200,200),250,370,100,45,"Home",'bookmanoldstlye',35,Font_colour,(15,8,35))
    ReStart_but = Button(Game_Surface,(200,250,200),370,370,120,45,"Restart",'bookmanoldstlye',35,Font_colour,(15,18,35))
    Exitt = Button(Game_Surface,(250,70,70),530,370,100,45,"Exit",'bookmanoldstlye',35,Font_colour,(250,0,0),Command=exiit)
    #==============================================================================================
    quit_count = 0
    Go_to_home, Go_to_game, exit_func_loop = False, False, False
    #==============================================================================================
    while True:
        Game_Surface.blit(BACK_IMAGE,(0,0))
        Draw_object(Home_but,ReStart_but,Exitt,winner_text_show)
        #==========================================================================================
        # Taking the input from the user
        for event in pygame.event.get():
            if event.type == QUIT: exit_func_loop = True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    if quit_count == 2: exit_func_loop = True
            if event.type == KEYUP:
                if event.key == K_q: quit_count += 1
        #==========================================================================================
        # Keeping the Frames on Limit, And Updating the Display  
        Clock.tick(FPS)
        # Updating the Game Surface/Screen
        if not exit_func_loop: screen.blit(Game_Surface,(0,0))
        pygame.display.update()
        #==========================================================================================
        Go_to_home = Check_Mouse_button_down(Home_but)
        Go_to_game = Check_Mouse_button_down(ReStart_but)
        #==========================================================================================
        if exit_func_loop or Go_to_home or Go_to_game: 
            Del_objects(Home_but,ReStart_but,Exitt,winner_text_show)
        #==========================================================================================
        if Go_to_home: Home_screen()
        if Go_to_game: game_screen()
        #==========================================================================================
        if exit_func_loop or Go_to_home or Go_to_game: break
#==================================================================================================
if __name__ == "__main__":    
    Home_screen()