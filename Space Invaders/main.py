import math,  random, os
import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()  
#assets_Spaceinvaders
#=======================================================================================================================================
#=======================================================================================================================================
# Function to Import Every File 
z = os.getcwd()
print(z)
path = f"{z}\\Games\\Space Invaders\\assets_Spaceinvaders\\"
def import_game_files():
    """Returns True if all the required images and sound effect are imported and available for the game"""
    global path
    i = 0
    try:
        # Background of the Main/Welcome/Home Screen
        pygame.image.load(os.path.join(f"{path}","background_home.png"))
        i += 1
        # Background of the Game Screen
        pygame.image.load(os.path.join(f"{path}",'background.png'))
        i += 1
        # Icon of the Game
        pygame.image.load(os.path.join(f"{path}",'Icon.png'))
        i += 1
        # Player's image 
        pygame.image.load(os.path.join(f"{path}",'player.png'))
        i += 1
        # Enemy's image 
        pygame.image.load(os.path.join(f"{path}",'enemy.png'))
        i += 1
        # Bullet
        pygame.image.load(os.path.join(f"{path}",'bullet.png'))
        i += 1
        # Explosion Sounds effect
        mixer.Sound(os.path.join(f"{path}",'explosion.wav'))
        i += 1
        # Bullet/Laser Fired Sound effect
        mixer.Sound(os.path.join(f"{path}",'laser.wav'))
        i += 1
        # Sound playing in the Background
        mixer.music.load(os.path.join(f"{path}","background.wav"))
        mixer.music.play(-1)
        i += 1
        if i == 9:
            return True

    except Exception:
        pass
#=======================================================================================================================================
# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background_Game = pygame.image.load(os.path.join(f"{path}",'background.png'))
background_home = pygame.image.load(os.path.join(f"{path}",'background_home.png'))
background_over = pygame.image.load(os.path.join(f"{path}",'gameover.png'))
# Caption and Icon
pygame.display.set_caption(os.path.join(f"{path}",'Space Invader'))
icon = pygame.image.load(os.path.join(f"{path}",'Icon.png'))
pygame.display.set_icon(icon)

#=======================================================================================================================================
#=======================================================================================================================================
# Player
playerImg = pygame.image.load(os.path.join(f"{path}",'player.png'))
playerX = 370
playerY = 500
playerX_change = 0
#=======================================================================================================================================
# Enemies 
enemyImg = []         # Image
enemyX = []           # X Co-ordinate
enemyY = []           # Y Co-ordinate
enemyX_change = []    # Change in X Co-ordinates of each enemy
enemyY_change = []    # Change in Y Co-ordinate
enemyx_changevar = 5 
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(os.path.join(f"{path}",'enemy.png')))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
#=======================================================================================================================================
#=======================================================================================================================================
# Bullet
bulletImg = pygame.image.load(os.path.join(f"{path}",'bullet.png'))
bulletX = 400
bulletY = 500
bulletX_change = 0
bulletY_change = 12     # Fire - The bullet is currently moving
bullet_state = "ready"  # Ready - You can't see the bullet on the screen
#=======================================================================================================================================
# Score Value
score_value = 0
# Score Font 
font = pygame.font.Font('freesansbold.ttf', 32)

#=======================================================================================================================================
# Game Over
over_font =  pygame.font.SysFont('chiller', 64,bold=True)
#=======================================================================================================================================
#Inserting Sounds effect
explosionSound = mixer.Sound(os.path.join(f"{path}",'explosion.wav'))
bulletSound = mixer.Sound(os.path.join(f"{path}",'laser.wav'))
#=======================================================================================================================================
#=======================================================================================================================================
# Button Class
class button():
    """ Used to Create a button with parameters -> colour, x , y, width , height, **text"""
    def __init__(self, colour,x,y,width,height,text=" ",font_size=30, font_colour=(0,0,0)):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.text = text
        self.font_colour = font_colour
    
    # Fonts - comicsans, algerian, castellar, chiller, 
    def draw(self, windoow, outline=None):
        if outline:
            pygame.draw.rect(windoow, outline, (self.x-2, self.y-2,self.width+2,self.height+2))
        pygame.draw.rect(windoow, self.colour, (self.x, self.y, self.width, self.height), 0)
        if self.text != " ":
            But_font = pygame.font.SysFont('forte',self.font_size)
            But_text = But_font.render(self.text, 1,self.font_colour)
            windoow.blit(But_text,( self.x + (self.width/2 - But_text.get_width()/2), self.y + (self.height/2 - But_text.get_height()/2)))
        
    def hover(self, pos):
        if ((self.width + self.x) > pos[0] > self.x) and ((self.height + self.y) > pos[1] > self.y):
            return True
        
        return False

#=======================================================================================================================================
# Functions Used in the game
#=======================================================================================================================================
def show_score():
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (600, 10))

#=======================================================================================================================================
def game_over_screen():
    global screen, score_value
    game_over_run = True
    retry_but = button((255,155,45),180,530,100,50,text="Home")
    Exit_butun = button((255,0,0),520,530,100,50,text="Exit")
    while game_over_run:
        # Background Image
        screen.blit(background_over, (0, 0))
        retry_but.draw(screen)
        Exit_butun.draw(screen)
        total = over_font.render(f"Total Score : {str(score_value)}", True, (255, 255,13))
        screen.blit(total, (210, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_run = False
            if event.type == pygame.MOUSEMOTION:
                if retry_but.hover(pygame.mouse.get_pos()):
                    retry_but.colour = (255,0,0)
                    retry_but.font_colour=(235,210,5)
                else:
                    retry_but.colour =(255,155,45)
                    retry_but.font_colour=(0,0,0)
                if Exit_butun.hover(pygame.mouse.get_pos()):
                    Exit_butun.colour = (255,0,0)
                    Exit_butun.font_colour=(235,210,5)
                else:
                    Exit_butun.colour =(255,0,0)
                    Exit_butun.font_colour=(0,0,0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_but.hover(pygame.mouse.get_pos()):
                    game_over_run = False
                    score_value = 0
                    Home_screen()
                if Exit_butun.hover(pygame.mouse.get_pos()):
                    game_over_run = False
                    pygame.quit()
        pygame.display.update()
            
#=======================================================================================================================================
def fire_bullet(x, y):
    """Used to fire the bullet/laser & Change Bullet's state to Fire"""
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

#=======================================================================================================================================
def isCollision(enemyX, enemyY, bulletX, bulletY):
    """Returns True if Bullet had Collided with Enemy & Change Bullet's state to Ready"""
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False

#=======================================================================================================================================
def Game_screen():
    """This the Game Window in which the user enjoys the game"""
    global game_run, playerX, playerY, playerX_change, bulletX, bulletY,bullet_state , enemyX, enemyY, score_value
    # Game Loop
    game_run = True
    while game_run:
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background_Game, (0, 0))
        show_score()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_ESCAPE:
                    game_run = False
                    Home_screen()
                if event.key == pygame.K_f:
                    if bullet_state is "ready":
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship:
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                if (0<int(m_pos[0])<800) and (75< int(m_pos[1]) < 600):
                    if bullet_state is "ready":
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship:
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # 5 = 5 + -0.1 -> 5 = 5 - 0.1
        # 5 = 5 + 0.1

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        # Enemy Movement
        for i in range(num_of_enemies):
            # Game Over
            if enemyY[i] > 428:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_run = False
                game_over_screen()
                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = enemyx_changevar
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = (enemyx_changevar * -1)
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(75, 175)

            #enemy(enemyX[i], enemyY[i], i)
            screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 500
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        screen.blit(playerImg, (playerX, playerY))
        pygame.display.update()

#=======================================================================================================================================
def Home_screen():
    home_run = True
    Game_run = button((185,0,0),180,530,100,50,text="Start")
    Exit_but = button((185,0,0),520,530,100,50,text="Exit")
    while home_run:
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background_home, (0, 0))
        Game_run.draw(screen)
        Exit_but.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                home_run = False
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                if Game_run.hover(pygame.mouse.get_pos()):
                    Game_run.colour = (185,0,0)
                    Game_run.font_colour=(235,210,5)
                else:
                    Game_run.colour =(255,0,0)
                    Game_run.font_colour=(0,0,0)
                if Exit_but.hover(pygame.mouse.get_pos()):
                    Exit_but.colour = (185,0,0)
                    Exit_but.font_colour=(235,210,5)
                else:
                    Exit_but.colour =(255,0,0)
                    Exit_but.font_colour=(0,0,0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Game_run.hover(pygame.mouse.get_pos()):
                    home_run = False
                    Game_screen()
                if Exit_but.hover(pygame.mouse.get_pos()):
                    home_run = False
                    pygame.quit()
        pygame.display.update()
            

#=======================================================================================================================================
chk = import_game_files()
if chk:
    Home_screen()
