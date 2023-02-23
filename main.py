import pygame
from pygame.locals import *
import csv
import asyncio

pygame.init()

height = 1000
width = 1600

player_x = 500
player_y = 500

screen = pygame.display.set_mode([width,height])

pygame.display.set_caption("test")

test_map = open("tiled.csv", 'r')

tileset_1 = pygame.image.load("test.png").convert_alpha()

tileset_size = 32

emme = tileset_1.subsurface([32,32,tileset_size, tileset_size])

clock = pygame.time.Clock()
effeps=100

reader = csv.reader(test_map)

white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

tileset_2 = pygame.image.load("tiles.png").convert_alpha()
erba = tileset_2.subsurface([0,0,tileset_size,tileset_size,])
acqua = tileset_2.subsurface([32,0,tileset_size, tileset_size])
rocce = tileset_2.subsurface([0,32,tileset_size, tileset_size])
deserto = tileset_2.subsurface([32,32,tileset_size, tileset_size]) 
class Player():
    
    def __init__(self, x,y):
        
        self.img = emme        
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.direction = pygame.math.Vector2()
        
    def update(self):
        
        global player_x,player_y


        move_velocity = 5
        
        

        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.direction.y = -1
        elif key[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
           
        if key[pygame.K_RIGHT]:
            self.direction.x = 1
        elif key[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
           
        #collisioni tiles
    
        for tile in world.tile_list:
            if tile[0] == acqua or tile[0] == rocce:
                if tile[1].colliderect(self.rect.x + self.direction.x * move_velocity, self.rect.y, self.width, self.height):
                    self.direction.x = 0
                      
                if tile[1].colliderect(self.rect.x, self.rect.y + self.direction.y * move_velocity, self.width, self.height):
                    self.direction.y = 0
                    
                 
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.rect.x += self.direction.x * move_velocity
        self.rect.y += self.direction.y * move_velocity
        
        #collisione bordi
        if self.rect.bottom > height:
            self.rect.bottom = height
            self.direction.y = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.direction.y = 0

        if self.rect.left < 0:
            self.rect.left = 0
            self.direction.x = 0

        if self.rect.right > width:
            self.rect.right = width
            self.direction.x = 0

        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, red, self.rect)

class World():
    def __init__(self, data):
        self.tile_list = []   
          

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 0:
                    img = erba
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tileset_size
                    img_rect.y = row_count * tileset_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 1:
                    img = acqua
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tileset_size
                    img_rect.y = row_count * tileset_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = rocce
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tileset_size
                    img_rect.y = row_count * tileset_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = deserto
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tileset_size
                    img_rect.y = row_count * tileset_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, white, tile[1], 1)

list_map = []

for row in reader:
    list_map.append(row)

for n, i in enumerate(list_map):
    for k, j in enumerate(i):
        list_map[n][k] = int(j)
            
            
class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, red )
 
    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, red)
        display.blit(self.text, (200, 150))
 
player = Player(player_x,player_y)
world = World(list_map)

async def main():
    
    fps = FPS() 
    running = True

    global player_x, player_y
    
    
    
    while running:  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        world.draw()
        player.update()
        

        fps.render(screen)
        pygame.display.update()
       
        fps.clock.tick(effeps)
        
        await asyncio.sleep(0)
        
        if not running:
            pygame.quit()
                

asyncio.run(main())

