import pygame
from pygame import init, Surface , time
from pygame import mixer
from random import randint
from pygame import KEYDOWN, KEYUP, K_a, K_d, K_w, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, K_r
from text_and_button import Show_Text, Button
from characters import Player, Enemy_sprites
# Initialise Pygame
init()
mixer.init()
#=================== Function to Initialise Pygame and to set Caption and Icon ======================
def Initialise(Game,*args):
    global WindowSize
    init()                                          #====== Initialise Pygame =====
    pygame.display.set_caption(Game)                #====== Caption and Icon ======
    Width, Height = 800, 500                        # set width and height of game
    WindowSize = (Width, Height)                    #
    Window = pygame.display.set_mode(WindowSize)    #====== Create the screen =====
    Game_Surface = Surface(WindowSize)              #=== Game Surface to render ===
    #============================================ ============== ===================================
    return Window , Game_Surface
#============================================ ============== ========================================
Window, Screen = Initialise("Space-Invaders")
#============================================ ============== ========================================
# FPS Setting
Clock = pygame.time.Clock()
FPS = 30
# Scoe 
actual_score = 0
# Game Font
game_font = pygame.font.SysFont("m5x7 medium",12)
#============================================ Path for the assets ============================================
path = "E:/Python Programs/Games/Space Invaders Type-2/Assets"   # If path changed goto Load_map and set path their too
#============================================ Importing Assets in Game =======================================
side_img0 = pygame.image.load(f"{path}/Side.png")                                                               # side image for left side
side_img0 = pygame.transform.scale(side_img0,( int(side_img0.get_width()*1.8) ,(side_img0.get_height() * 3) ))  # resizing side image
side_img1 = pygame.transform.flip(side_img0,True,False)                                                         # side image for right side
bg_img = pygame.image.load(f"{path}/background.jpeg")                                                           # background image of the game
bg_img = pygame.transform.scale(bg_img,(800,500))                                                               # resizing background image
loc_img = pygame.image.load(f"{path}/Line_of_site.png")                                                         # Line of Site image
explosion_sound = mixer.Sound(f"{path}/explosion.wav")                                                          # Explosion Sound
explosion_sound.set_volume(0.3)                                                                                 # Setting Volume of Explosion Sound
shoot_sound = mixer.Sound(f"{path}/shoot.wav")                                                                  # Shooting Sound i.e. Fire Sound
#============================================== Importing Characters ==========================================
enemy = Enemy_sprites({"Enemy1":[f"{path}/En1.png",f"{path}/En2.png"],"Enemy2":[f"{path}/En3.png",f"{path}/En4.png"],"Enemy3":[f"{path}/En5.png",f"{path}/En6.png"]})
player = Player([f"{path}/Sp1.png",f"{path}/Sp2.png"],f"{path}/Bullet.png",425)
player.shoot_sound = shoot_sound
#============================================ ============== ========================================
def load_background(surface):
    x, y, h = -12, 0, side_img0.get_height()
    w = loc_img.get_width()
    surface.blit(bg_img,(0,0))
    while True:
        if x == 767: i = side_img1
        else: i = side_img0
        surface.blit(i,(x,y))
        y += h
        if y > 800: 
            if x == 767: 
                x, y = side_img0.get_width()-5 , 375
                i = loc_img
                break
            x, y = 767, 0
    while True:
        surface.blit(i,(x,y))
        x+=w
        if x>800-side_img0.get_width(): break

def Home_screen():
    qt = False
    home_text = Show_Text(Screen,'Space - Invaders',50,(173,181,189),140,120)
    home_text2 = Show_Text(Screen,'By Pygame',15,(173,181,189),600,180)
    start_game = Button(Screen,(222,226,218),180,300,100,40,'Start',font_colour=(127,127,127),fill=(52,58,64),Command=Game_screen)
    exit_game = Button(Screen,(222,226,218),520,300,100,40,'Exit',font_colour=(186,24,27),fill=(52,58,64),Command=exit)
    while True:    
        Screen.blit(bg_img,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: qt = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: qt = True
        
        home_text.draw()
        home_text2.draw()
        start_game.draw()
        exit_game.draw()
        
        # Blitting The Game Surface on the Screen
        surf = pygame.transform.scale(Screen, WindowSize)
        Window.blit(surf,(0,0))
        # Updating the Display
        pygame.display.update()
        if qt: pygame.quit()

def Game_screen():
    global actual_score
    global WindowSize
    qt = False
    start= 0
    score , actual_score = 0, 0
    home_button = Button(Screen,(222,226,218),45,5,50,20,'Home',font_colour=(127,127,127),font_size=15,fill=(52,58,64),Command=Home_screen)
    fin_game = Button(Screen,(222,226,218),705,5,50,20,'Exit',font_colour=(186,24,27),font_size=18,fill=(52,58,64),Command=exit)
    score_text = Show_Text(Screen,f"Score {actual_score}",22,(217,217,217),325,5)
    while True:
        if start < 2: 
            start += 1
            enemy.load_pos()
        delta = Clock.tick(60) * 0.001 * 60
        Screen.fill((15,10,30))
        player.parameters(delta,Screen)
        enemy.parameters(delta,Screen)
        bullet_rect = player.get_bullet_rect()
        collid = enemy.check_for_collision(bullet_rect)
        if collid: 
            player.reload()
            score += 5
            actual_score = int(score - (0.4 * player.bullet_count)) 
            score_text.Update(f"Score {actual_score}")
            explosion_sound.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: qt = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: qt = True
                if event.key == K_RIGHT or event.key == K_d: player.set_movement('right')
                elif event.key == K_LEFT or event.key == K_a: player.set_movement('left')
                if event.key == K_SPACE: player.shoot_bullet()
                if event.key == K_r: 
                    enemy.load_pos()
                    score, actual_score = 0, 0
                    score_text.Update(f"Score {actual_score}")
                    player.reload()
                    player.bullet_count=0
            if event.type == KEYUP:
                if  event.key in [K_RIGHT, K_d]: player.move_right = False
                elif event.key in [K_LEFT, K_a]: player.move_left = False
        load_background(Screen)
        player.draw()
        enemy.draw()
        home_button.draw()
        fin_game.draw()
        score_text.draw()
        Check = enemy.check_for_win_and_lose()
        if Check:
            if Check == 'win': Win_screen()
            if Check == 'lose': lose_screen()
        # Blitting The Game Surface on the Screen
        surf = pygame.transform.scale(Screen, WindowSize)
        Window.blit(surf,(0,0))
        # Updating the Display
        pygame.display.update()
        if qt: pygame.quit()

def Win_screen():
    global actual_score
    qt = False
    win_text = Show_Text(Screen,f"You Won! ",70,(168,177,175),175,100)
    score_text = Show_Text(Screen,f"Your Score is {actual_score}",50,(168,177,175),160,220)
    home_but = Button(Screen,(222,226,218),175,340,100,40,'Home',font_colour=(127,127,127),fill=(52,58,64),Command=Home_screen)
    retry_but = Button(Screen,(222,226,218),310,340,100,40,'Retry',font_colour=(127,127,127),fill=(52,58,64),Command=Game_screen)
    exit_game = Button(Screen,(222,226,218),525,340,100,40,'Exit',font_colour=(186,24,27),fill=(52,58,64),Command=exit)
    while True:
        Screen.blit(bg_img,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: qt = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: qt = True

        win_text.draw()
        score_text.draw()
        home_but.draw()
        retry_but.draw()
        exit_game.draw()

        # Blitting The Game Surface on the Screen
        surf = pygame.transform.scale(Screen, WindowSize)
        Window.blit(surf,(0,0))
        # Updating the Display
        pygame.display.update()

        if qt: pygame.quit()

def lose_screen():
    global actual_score
    qt = False
    lose_text = Show_Text(Screen,'You Lose!!',70,(173,181,189),180,120)
    lose_text2 = Show_Text(Screen,f'Your Score is {actual_score}',22,(173,181,189),290,200)
    lose_text3 = Show_Text(Screen,'What you would like to do!',15,(173,181,189),260,290)
    retry_but = Button(Screen,(222,226,218),220,310,100,40,'Retry',font_colour=(177,177,177),fill=(52,58,64),Command=Game_screen)
    exit_game = Button(Screen,(222,226,218),480,310,100,40,'Exit',font_colour=(186,24,27),fill=(52,58,64),Command=exit)
    while True:    
        Screen.blit(bg_img,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: qt = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: qt = True
        lose_text.draw()
        lose_text2.draw()
        lose_text3.draw()
        retry_but.draw()
        exit_game.draw()
        # Blitting The Game Surface on the Screen
        surf = pygame.transform.scale(Screen, WindowSize)
        Window.blit(surf,(0,0))
        # Updating the Display
        pygame.display.update()
        if qt: pygame.quit()

if __name__ == "__main__":
    Home_screen()