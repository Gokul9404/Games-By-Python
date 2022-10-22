import csv, pygame

path = "E:/Python Programs/Games/No Way Down/Assets"
# Path for Level Files
levels = [f"{path}/Level/level1.csv",f"{path}/Level/Level3.csv",f"{path}/Level/Level4.csv",f"{path}/Level/Level6.csv",f"{path}/Level/Level7.csv"]
# Each level Y value such tahe player is always at the buttom of the level 
level_y = [0,3,3,0,-3,-3]
player_y = [0,456,456,576,576,576]

Tile_size = 30
Tiles_frame = {}

def set_map_path(Path):
    global path 
    path = Path
    
def total_levels():
    return len(levels)

def load_tiles(paath=f"{path}/Sprites/Tile"):
    global Tiles_frame
    tile_name = paath.split("/")[-1]
    tile_frame_data = []
    for i in range(5):
        tile_id = tile_name + "_" + str(i)
        img_loc = paath + "/" + tile_id + ".png"
        image = pygame.image.load(img_loc)
        tile_image = pygame.transform.scale(image,(Tile_size,Tile_size))
        Tiles_frame[tile_id] = tile_image.copy()
        tile_frame_data.append(tile_id)
    return tile_frame_data

def load_level(x):
    global levels
    f = open(levels[x-1],"r")
    rd = csv.reader(f)
    lvl = []
    for line in rd:
        x = line
        lvl.append(x)
    return lvl

def load_map(Surface,Game_level,scroll=[0,0]):
    Level = load_level(Game_level)
    y = level_y[Game_level]
    tiles_rect ,win_rect= [], []
    win_pos = [0,0]
    for row in Level:
        x = 0
        for tile in row:
            if tile == "0": Surface.blit(Tiles_frame["Tile_0"],(x*Tile_size+scroll[0], y*Tile_size+scroll[1]))
            if tile == "1": Surface.blit(Tiles_frame["Tile_1"],(x*Tile_size+scroll[0], y*Tile_size+scroll[1]))
            if tile == "2": Surface.blit(Tiles_frame["Tile_2"],(x*Tile_size+scroll[0], y*Tile_size+scroll[1]))
            if tile == "3": Surface.blit(Tiles_frame["Tile_3"],(x*Tile_size+scroll[0], y*Tile_size+scroll[1]))
            if tile == "4":
                Surface.blit(Tiles_frame["Tile_4"],(x*Tile_size+scroll[0], y*Tile_size+scroll[1]))
                win_pos = [ x*Tile_size+scroll[0], y*Tile_size+scroll[1]] 
                win_rect.append(pygame.Rect(x * Tile_size , y * Tile_size, Tile_size, Tile_size))
            if tile !="0"and tile !="4": tiles_rect.append(pygame.Rect(x*Tile_size,y * Tile_size, Tile_size, Tile_size))
            x+=1
        y+=1
    return tiles_rect, win_rect , win_pos

def player_y_of_level(lvl):
    return player_y[lvl]