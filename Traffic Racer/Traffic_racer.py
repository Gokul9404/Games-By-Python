# Importing Pygame module ===================================================
import pygame
from random import randint
from time import sleep
from os.path import join
from pygame import mixer
from pygame import K_RIGHT, K_LEFT, K_SPACE, K_ESCAPE, K_a, K_d, KEYUP, KEYDOWN, QUIT, init, quit, MOUSEBUTTONDOWN

# ==  Button Class  ==========================================================
class button():
    """ Used to Create a button on the screen """

    def __init__(self, colour, x, y, width, height, text=" ", font_size=30, font_colour=(0, 0, 0)):
        self.colour = colour
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text
        # Available Fonts - comicsans, algerian, castellar, chiller
        self.font_size, self.font_colour = font_size, font_colour

    def draw(self, windoow, outline=None):
        if outline:
            pygame.draw.rect(windoow, outline, (self.x-2,
                             self.y-2, self.width+2, self.height+2))
        pygame.draw.rect(windoow, self.colour,
                         (self.x, self.y, self.width, self.height), 0)
        if self.text != " ":
            But_font = pygame.font.SysFont('forte', self.font_size)
            But_text = But_font.render(self.text, 1, self.font_colour)
            windoow.blit(But_text, (self.x + (self.width/2 - But_text.get_width()/2),
                         self.y + (self.height/2 - But_text.get_height()/2)))

    def hover(self, pos):
        if ((self.width + self.x) > pos[0] > self.x) and ((self.height + self.y) > pos[1] > self.y):
            return True
        return False

# == Functions Used to Play game ==============================================
def import_assets():
    """Import all the Required assets for the game"""
    global playerImg, Car1, Car2, Car3, Car4, Car5, screen, path, background_home, background, road, Road2, crash, crash_sound
    # Set the Directory path of the files, to get all the required assets for the game
    path = "E:\\Python Programs\\Games\\Traffic Racer"
    try:
        # Game Images
        background_home = pygame.image.load(path.join(
            f"{path}", "Assets\\home_background.png"))  # Home-BackGround Image
        # BackGround Image Of Game Screen
        background = pygame.image.load(
            join(f"{path}", "Assets\\Road_Main.png"))
        crash = pygame.image.load(join(
            f"{path}", "Assets\\carcrash.png"))                  # Car Crash Image
        # Car Crash Sound
        crash_sound = mixer.Sound(join(f"{path}", "Assets\\crash.wav"))
        mixer.music.load(path.join(f"{path}", "Assets\\back_music.wav"))
        Car1 = pygame.image.load(join(
            f"{path}", "Assets\\car02.png"))                      # Other Car's
        Car2 = pygame.image.load(join(
            f"{path}", "Assets\\car03.png"))                      # Other Car's
        Car3 = pygame.image.load(join(
            f"{path}", "Assets\\car04.png"))                      # Other Car's
        Car4 = pygame.image.load(join(
            f"{path}", "Assets\\car05.png"))                      # Other Car's
        Car5 = pygame.image.load(join(
            f"{path}", "Assets\\car06.png"))                      # Other Car's
        playerImg = pygame.image.load(join(
            f"{path}", "Assets\\Main_car.png"))              # Player's Car Image
        road = pygame.image.load(join(
            f"{path}", "Assets\\road4lane.png"))                  # Road Image 1
        Road2 = pygame.image.load(join(
            f"{path}", "Assets\\road4lane.png"))                 # Road Image 1
        # Icon of the Game
        icon = pygame.image.load(join(f"{path}", 'Assets\\Icon.png'))
        # Set Icon of the Game
        pygame.display.set_icon(icon)
        music = mixer.music.load(join(f"{path}", "Assets\\back_music.wav"))
    except Exception as e:
        print("! Unable to load game-asset-files !")
        print(e)

# ============================================================================

def game_init():
    """Initialise the Game and set the basic required arguments"""
    global playerX, playerX_change, playerY, score_value, level_value, cars_start_X, cars_start_y, other_cars, Screen_Widht, Screen_Height, screen, Car1, Car2, Car3, Car4, Car5
    playerX, playerX_change, playerY = 300, 0, 475
    # Score & Level of the Player
    score_value, level_value = 0, 1
    # Other Car's X & Y Co-ordiate
    cars_start_X, cars_start_y = [145, 255, 370, 480], [35, -2, 20, -10]
    other_cars = [Car1, Car2, Car3, Car4,  Car5]
    # Creating the screen ======================================================
    Screen_Widht, Screen_Height = 700, 700
    screen = pygame.display.set_mode((Screen_Widht, Screen_Height))
    # Set Caption of the Game
    pygame.display.set_caption('Traffic_racer_car')

# ============================================================================

def isCollision(car_enemyX, car_enemyY, Player_X, Player_Y):
    """Returns True if cars had Collided or Not"""
    if ((car_enemyX < Player_X < (car_enemyX + 72)) or (car_enemyX < Player_X + 60 < (car_enemyX + 70))):
        if (car_enemyY < Player_Y < (car_enemyY + 118)):
            return True
        elif Player_Y < car_enemyY and (car_enemyY < Player_Y + 124 < (car_enemyY + 118)):
            return True
    else:
        return False

# ============================================================================

def Enemy_car_coordinate():
    """Returns Other car's Image , it's X & Y co-ordinate"""
    Enemy_car = other_cars[randint(0, 4)]
    Enemy_car_x = cars_start_X[randint(0, len(cars_start_y)-1)]
    Enemy_car_y = cars_start_y[randint(0, len(cars_start_y)-1)]
    return Enemy_car, Enemy_car_x, Enemy_car_y

# ============================================================================

def show_score():
    """Shows Score and Level on the Screen"""
    text_colour = (220, 47, 2)
    score_font = pygame.font.SysFont('algerian', 25, italic=True)
    score = score_font.render("Score : " + str(score_value), True, text_colour)
    screen.blit(score, (190, 0))
    level = score_font.render(f"Level:- {level_value}", True, text_colour)
    screen.blit(level, (420, 0))

# ============================================================================

def Game_screen():
    """Play Screen of the Game"""
    global playerImg, Car1, Car2, Car3, Car4, Car5, other_cars, screen, playerX, playerY, playerX_change, score_value, level_value, cars_start_X, cars_start_y, background, road, Road2, crash, crash_sound, Screen_Widht, Screen_Height
    Game_run_screen, Finnish, Exitt, home_start = True, False, False, False
    speed_of_car, playerx_varchange, road_Y = 2, 5, 30
    # = Screen Top Part ======================================================
    # Top Screen-Part colour
    top_colour = (241, 250, 238)
    Home_Button = button(top_colour, 5, 2, 80, 25,
                         text="Home", font_size=20)     # Home Button
    Exit_Button = button(top_colour, 615, 2, 80, 25,
                         text="Exit", font_size=20)   # Exit Button

    Enemy_car = Enemy_car_coordinate()

    # Play the Back-ground Music
    mixer.music.load(join(f"{path}", "Assets\\back_music.wav"))
    mixer.music.play(-1)

    # Enemy Car's Images, it's X & Y Co-ordinates List, with First Enemy car too
    car_enemy, car_enemy_x, car_enemy_y = [
        Enemy_car[0]], [Enemy_car[1]], [Enemy_car[2]]

    while Game_run_screen:
        score_value_in = 0
        # == Roads Y Co-ordinate ==========================
        Road2_y = road_Y - Road2.get_height()
        road_Y = road_Y % 620
        # == Screen Background ===========================
        pygame.draw.rect(screen, (94, 100, 114), [78, 0, 548, 680])
        # Background Image
        screen.blit(background, (0, 30))
        # Road Image 1
        screen.blit(road, (78, road_Y))
        # Road Image 2
        screen.blit(Road2, (78, Road2_y))

        # =====================================================================
        home_Button_button_active = Home_Button.hover(pygame.mouse.get_pos())
        exit_Button_button_active = Exit_Button.hover(pygame.mouse.get_pos())

        Home_Button.font_colour = (
            235, 210, 5) if home_Button_button_active else (0, 0, 0)
        Exit_Button.font_colour = (
            255, 0, 0) if exit_Button_button_active else (0, 0, 0)
        # =====================================================================

        for event in pygame.event.get():                             # Handling Events in Game Screen
            if event.type == QUIT:
                Game_run_screen, Exitt = False, True

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Game_run_screen, home_start = False, True
                # Moving Player Car Left & Right
                if (event.key == K_LEFT) or (event.key == K_a):
                    # If Left Key Pressed
                    playerX_change = (-1 * playerx_varchange)
                if (event.key == K_RIGHT) or (event.key == K_d):
                    # If Right Key Pressed
                    playerX_change = playerx_varchange

            if event.type == KEYUP:
                if event.key in (K_a, K_d, K_LEFT, K_RIGHT):
                    playerX_change = 0  # If any Key Unpressed stop moving the car

            if event.type == MOUSEBUTTONDOWN:          # Button's Click
                if home_Button_button_active:
                    Game_run_screen, home_start = False, True
                if exit_Button_button_active:
                    Game_run_screen, Exitt = False, True
        # =====================================================================
        playerX += playerX_change
        # If Car Reaches at Left/Right Side of the Road stop moving car Left/Right
        if playerX <= 130:
            playerX = 130
        elif playerX >= 515:
            playerX = 515
        # ==== Showing Non-Player on the Screen and check for collision with them ====
        for x in range(len(car_enemy)):
            # => Showing Non Player car on the Screen
            screen.blit(car_enemy[x], (car_enemy_x[x], car_enemy_y[x]))
            # ==  If Car not collided and at bottom of the screen  ===================
            if car_enemy_y[x] >= 650:
                car_enemy[x], car_enemy_x[x], car_enemy_y[x] = Enemy_car_coordinate()
                score_value_in += 1
                car_enemy_x.append(car_enemy_x[x])
                car_enemy_y.append(car_enemy_y[x])
                if score_value % 5 == 0 and score_value != 0:
                    level_value += 1
                    speed_of_car += 1
                    playerx_varchange += 2
                    if level_value < 3:
                        Enemy_car0 = Enemy_car_coordinate()
                        car_enemy.append(Enemy_car0[0])
                        car_enemy_x.append(Enemy_car0[1])
                        car_enemy_y.append(Enemy_car0[2])
            # ======================================================================
            # => Check for Collision
            Collild = isCollision(
                car_enemy_x[x], car_enemy_y[x], playerX, playerY)
            if Collild:
                screen.blit(crash, ((Screen_Widht/2 - crash.get_width()/2),
                            (Screen_Height/2 - (crash.get_height()+1 / 2))))
                crash_sound.play()
                Finnish = True
            car_enemy_y[x] += speed_of_car
        if score_value_in >= 1:
            score_value += 1
            score_value_in = 0
        # ==============================================
        # Showing Player on the Screen
        screen.blit(playerImg, (playerX, playerY))
        # Rectangle at the Top of the screens
        pygame.draw.rect(screen, top_colour, [0, 0, 700, 30])
        # Blitting Home Button on the screen
        Home_Button.draw(screen)
        # Blitting Exit Button on the screen
        Exit_Button.draw(screen)
        # Show Score on the Top
        show_score()
        # Rectangle at the Bottom of the screen
        pygame.draw.rect(screen, (145, 124, 111), [0, 680, 700, 50])
        road_Y += speed_of_car                                      # Scrooling Road
        # =====================================================================
        pygame.display.update()
        # =====================================================================
        if Finnish:  # => If car's had collided then Game get's Finished
            playerX_change = 0
            sleep(1)
            score_value, level_value = 0, 1
            Game_run_screen, home_start = False, True
        if home_start:
            Home_screen()
        if Exitt:
            quit()
# ============================================================================

def Home_screen():
    """Welcome Screen Or Home Screen of the Game"""
    global screen, background_home
    home_run, Game_start, exitt = True, False, False
    Game_run = button((255, 0, 0), 10, 500, 100, 50, text="Start")
    Exit_but = button((255, 0, 0), 595, 500, 100, 50, text="Exit")

    while home_run:
        screen.fill((176, 176, 176))
        screen.blit(background_home, (115, 0))        # Background Image
        # Blitting Start Button on the screen
        Game_run.draw(screen)
        # Blitting Exit Button on the screen
        Exit_but.draw(screen)

        # =====================================================================
        game_run_button_active = Game_run.hover(pygame.mouse.get_pos())
        exit_run_button_active = Exit_but.hover(pygame.mouse.get_pos())
        if game_run_button_active:
            Game_run.colour, Game_run.font_colour = (185, 0, 0), (235, 210, 5)
        else:
            Game_run.colour, Game_run.font_colour = (255, 0, 0), (0, 0, 0)

        if exit_run_button_active:
            Exit_but.colour, Exit_but.font_colour = (235, 210, 5), (185, 0, 0)
        else:
            Exit_but.colour, Exit_but.font_colour = (255, 0, 0), (0, 0, 0)

        # =====================================================================
        for event in pygame.event.get():             # Exit Game
            if event.type == pygame.QUIT:
                home_run, exitt = False, True

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    home_run, Game_start = False, True

            if event.type == pygame.MOUSEBUTTONDOWN:  # Button Clicked
                if game_run_button_active:
                    home_run, Game_start = False, True
                if exit_run_button_active:
                    home_run, exitt = False, True

        # =====================================================================
        pygame.display.update()
        # =====================================================================
        if Game_start:
            Game_screen()
        if exitt:
            quit()

# ============================================================================
if __name__ == "__main__":
    init()
    import_assets()
    game_init()
    Home_screen()