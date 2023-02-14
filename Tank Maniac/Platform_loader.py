import csv, pygame
from random import randint

path = "E:/Python Programs/Projects/Self-Projects/Tank_maniac/Assets"
Tile_size = 24

# Path for Level Files
levels = [f"{path}\Level\level_1.csv",f"{path}\Level\level_2.csv",f"{path}\Level\level_3.csv"]
#==================================================================================================
class Tiles:
    def __init__(self,Surface):
        self.path = f"{path}/Tile"
        self.screen = Surface
        self.level = ''
        self.tiles_list = self.load_tile_sprites()
        self.tiles_rects = []

    def load_tile_sprites(self):
        tile_image = pygame.image.load(f"{self.path}/tiles_sprite.png")
        tiles_set = tile_image.get_width()
        total_image = tiles_set // Tile_size
        img_list = []
        for img_no in range(total_image):
            image = pygame.Surface((Tile_size,Tile_size))
            image.blit(tile_image, (0,0), ( (img_no * Tile_size), 0, Tile_size,Tile_size) )
            image.set_colorkey((0,0,0))
            img_list.append(image)
        image = pygame.Surface((Tile_size,Tile_size))
        tile_image = pygame.image.load(f"{self.path}/tile.png")
        image.blit(tile_image, (0,0), ( (img_no * Tile_size), 0, Tile_size,Tile_size) )
        image.set_colorkey((0,0,0))
        img_list.append(image)
        
        return img_list
    
    def load_level(self):
        global levels
        no = randint(0, 2)
        f = open(levels[no],"r")
        rd = csv.reader(f)
        lvl = []
        for line in rd:
            x = line
            lvl.append(x)
            self.level = lvl

    def get_tile_rect(self):
        return self.tiles_rects

    def Draw(self):
        Level = self.level
        tiles_rect = []
        y =  0
        for row in Level:
            x = 0
            for tile in row:
                if tile == "0": 
                    self.screen.blit(self.tiles_list[1],(x*Tile_size, y*Tile_size))
                if tile == "1": 
                    left_rotate = pygame.transform.rotate(self.tiles_list[4],90)
                    self.screen.blit(left_rotate,(x*Tile_size, y*Tile_size))
                if tile == "2":
                    right_rotate = pygame.transform.rotate(self.tiles_list[4],-90)
                    self.screen.blit(right_rotate,(x*Tile_size, y*Tile_size))
                if tile == "4": 
                    self.screen.blit(self.tiles_list[4],(x*Tile_size, y*Tile_size))
                if tile == "5": 
                    self.screen.blit(self.tiles_list[3],(x*Tile_size, y*Tile_size))
                if tile == "6": 
                    self.screen.blit(self.tiles_list[5],(x*Tile_size, y*Tile_size))
                if tile in ["0","1","2","4","5","6"]: 
                    tiles_rect.append(pygame.Rect(x*Tile_size,y * Tile_size, Tile_size, Tile_size))
                x+=1
            y+=1
        self.tiles_rects = tiles_rect
    
    def Delete(self):
        del self
#==================================================================================================