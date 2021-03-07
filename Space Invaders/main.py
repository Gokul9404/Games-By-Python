import math,  random, os,  pygame
from pygame import mixer
# Intialize the pygame
pygame.init()  
#=======================================================================================================================================
# Function to Import Every File 
z = os.getcwd()
path = f"{z}\\Games\\Space Invaders\\assets_Spaceinvaders\\"
#=======================================================================================================================================
def import_game_files():
    """Returns True if all the required images and sound effect are imported and available for the game"""
    global path, i
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
        if i == 9: return True
    except Exception:
        return False
#=======================================================================================================================================
chk1 = import_game_files()
open_game = False
if chk1: open_game = True
#=======================================================================================================================================
# create the screen
screen = pygame.display.set_mode((800, 600))
# Background
background_Game = pygame.image.load(os.path.join(f"{path}",'background.png'))
background_home = pygame.image.load(os.path.join(f"{path}",'background_home.png'))
background_over = pygame.image.load(os.path.join(f"{path}",'gameover.png'))
# Caption and Icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load(os.path.join(f"{path}",'Icon.png'))
pygame.display.set_icon(icon)
#=======================================================================================================================================
# Player
playerImg = pygame.image.load(os.path.join(f"{path}",'player.png'))
playerX , playerY= 370, 500
playerX_change, playerx_varchange = 0 , 5
#=======================================================================================================================================
# Enemies constant here
enemyY_change = 40  # Change in Y Co-ordinate
enemyx_changevar, num_of_enemies = 3 , 6
#=======================================================================================================================================
# Bullet
bulletImg = pygame.image.load(os.path.join(f"{path}",'bullet.png'))
bulletX , bulletY = 400, 500
bulletX_change, bulletY_change  = 0, 10     # Fire - The bullet is currently moving
bullet_state = "ready"                      # Ready - You can't see the bullet on the screen
#=======================================================================================================================================
# Score Value
score_value , level_value = 0, 1
# Game Over
over_font =  pygame.font.SysFont('chiller', 64,bold=True)
#Inserting Sounds effect
explosionSound = mixer.Sound(os.path.join(f"{path}",'explosion.wav'))
bulletSound = mixer.Sound(os.path.join(f"{path}",'laser.wav'))
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
    def draw(self, windoow, outline=None):
        if outline:
            pygame.draw.rect(windoow, outline, (self.x-2, self.y-2,self.width+2,self.height+2))
        pygame.draw.rect(windoow, self.colour, (self.x, self.y, self.width, self.height))
        if self.text != " ":
            But_font = pygame.font.SysFont('forte',self.font_size)
            But_text = But_font.render(self.text, 1,self.font_colour)
            windoow.blit(But_text,( self.x + (self.width/2 - But_text.get_width()/2),self.y + (self.height/2 - But_text.get_height()/2)))
    def hover(self, pos):
        if ((self.width + self.x) > pos[0] > self.x) and ((self.height + self.y) > pos[1] > self.y):
            return True
        return False
# Used to reco-ordinate the Images of the enemy
start_game = False
#=======================================================================================================================================
# Functions Used in the game
def Home_screen():
    """Welcome Screen Or Home Screen of the Game"""
    global start_game 
    home_run, start, exiit = True, False, False
    Game_run = button((185,0,0),180,530,100,50,text="Start")
    Exit_but = button((185,0,0),520,530,100,50,text="Exit")
    while home_run:
        screen.blit(background_home, (0, 0))                    # Background Image
        Game_run.draw(screen)
        Exit_but.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: home_run, exiit = False, True
            if event.type == pygame.MOUSEMOTION:
                if Game_run.hover(pygame.mouse.get_pos()): Game_run.colour, Game_run.font_colour = (185,0,0), (235,210,5)
                else: Game_run.colour , Game_run.font_colour = (255,0,0), (0,0,0)
                if Exit_but.hover(pygame.mouse.get_pos()): Exit_but.colour , Exit_but.font_colour = (185,0,0), (235,210,5)
                else: Exit_but.colour , Exit_but.font_colour = (255,0,0), (0,0,0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Game_run.hover(pygame.mouse.get_pos()): home_run , start_game , start = False, True, True
                if Exit_but.hover(pygame.mouse.get_pos()): home_run, exiit = False, True
        pygame.display.update()
        if start: Game_screen()
        if exiit: pygame.quit()
#=======================================================================================================================================
def Game_screen():
    """This the Game Window in which the user enjoys the game"""
    global game_run, playerX, playerY, playerX_change, bulletX, bulletY,bullet_state , enemyX, enemyY, score_value, level_value, enemyx_changevar, bulletY_change, playerx_varchange, enemyImg, enemyX ,enemyY , enemyX_change, start_game
    if start_game:            # Enemies 
        enemyImg = []         # Image
        enemyX , enemyY, enemyX_change = [] , [], []      # X & Y Co-ordinate , Change in X Co-ordinates of each enemy
        for i in range(num_of_enemies):
            enemyImg.append(pygame.image.load(os.path.join(f"{path}",'enemy.png')))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(50, 125))
            enemyX_change.append(4)
        start_game = False
    game_run, home_screen, Game_over = True, False, False   # Game Loop
    score_value , level_value = 0, 1
    while game_run:
        screen.blit(background_Game, (0, 0))                # Background Image
        show_score()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_run = False
            if event.type == pygame.KEYDOWN:                # if keystroke is pressed check whether its right or left
                if event.key == pygame.K_LEFT: playerX_change = (-1 * playerx_varchange)
                if event.key == pygame.K_RIGHT: playerX_change = playerx_varchange
                if event.key == pygame.K_ESCAPE: game_run, home_screen = False, True
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletSound.play()
                        bulletX = playerX             # Get the current x cordinate of the spaceship
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
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: playerX_change = 0
        playerX += playerX_change
        if playerX <= 0: playerX = 0
        elif playerX >= 736: playerX = 736
        # Enemy Movement
        for i in range(num_of_enemies):
            if enemyY[i] > 428:             # Game Over 
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_run, Game_over = False, True
                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = enemyx_changevar
                enemyY[i] += enemyY_change
            elif enemyX[i] >= 736:
                enemyX_change[i] = (enemyx_changevar * -1)
                enemyY[i] += enemyY_change
            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound.play()
                bulletY, bulletX  = 480, 400
                bullet_state = "ready"
                score_value += 1
                enemyX[i], enemyY[i] = random.randint(0, 736), random.randint(75, 175)
                if score_value % 12 == 0:
                    level_value += 1 
                    enemyx_changevar += 1
                    bulletY_change += 1
                    playerx_varchange += 1
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
        if home_screen: Home_screen()
        if Game_over: game_over_screen()
#=======================================================================================================================================
def game_over_screen():
    """When user loses the game, this Screen appears"""
    global screen, score_value
    game_over_run , hoome_screen = True, False
    retry_but = button((255,155,45),180,530,100,50,text="Home")
    Exit_butun = button((255,0,0),520,530,100,50,text="Exit")
    while game_over_run:
        screen.blit(background_over, (0, 0))        # Background Image
        retry_but.draw(screen)
        Exit_butun.draw(screen)
        total = over_font.render(f"Total Score : {str(score_value)}", True, (255, 255,13))
        screen.blit(total, (360, 40))
        level_scored = over_font.render(f"Level {level_value}", True, (255, 255, 0))
        screen.blit(level_scored , (45, 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_over_run = False
            if event.type == pygame.MOUSEMOTION:
                if retry_but.hover(pygame.mouse.get_pos()): retry_but.colour, retry_but.font_colour = (255,0,0), (235,210,5)
                else: retry_but.colour , retry_but.font_colour =(255,155,45), (0,0,0)
                if Exit_butun.hover(pygame.mouse.get_pos()): Exit_butun.colour, Exit_butun.font_colour = (255,0,0), (235,210,5)
                else: Exit_butun.colour , Exit_butun.font_colour= (255,0,0), (0,0,0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_but.hover(pygame.mouse.get_pos()):
                    game_over_run, hoome_screen = False, True
                    score_value = 0
                if Exit_butun.hover(pygame.mouse.get_pos()):
                    game_over_run = False
                    pygame.quit()
        pygame.display.update()
        if hoome_screen : Home_screen()
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
    if distance < 40: return True
    else: return False
#=======================================================================================================================================
def show_score():
    """Shows Score and Level on the Screen"""
    score =  pygame.font.SysFont('castellar',35,italic=True).render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (600, 10))
    level = pygame.font.SysFont('algerian',40,bold=True).render(f"Level:- {level_value}", True, (255, 255, 0))
    screen.blit(level , (200, 10))
#=======================================================================================================================================
if open_game == True: Home_screen()