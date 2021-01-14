from typing import Tuple

import pygame
import sys
import os

worldx = 1024
worldy = 700
fps = 40  # frame rate
ani = 4  # animation cycles
world = pygame.display.set_mode((worldx, worldy))
pygame.display.set_caption("MARSOBOT BY M3nti0nl3ss")

backdrop = pygame.image.load(os.path.join('images', 'texture_06.png'))
backdropbox = world.get_rect()

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

steps = 10
rot = 90


'''
Main Classes
'''

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
    #for i in range(1, 5):
        img = pygame.image.load(os.path.join('images', 'robot.png')).convert_alpha()
        img = pygame.transform.scale(img, (100, 100))
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  # set alpha
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x
        self.movey += y
    
    def rotate(self,angle):
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        """
        Update sprite position
        """

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        
        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            #self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            #self.image = self.images[self.frame//ani]
            
class Goal(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images',img))
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Pass(pygame.sprite.Sprite):
    def __init__(self, x,y,img="passe.png"):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images',img))
        self.image = pygame.transform.scale(self.image, (650, 350))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Level():
    def good(stat,eloc):
        enemy = Goal(eloc[0], eloc[1], 'box_'+str(stat)+'.png')
        enemy_list = pygame.sprite.Group()
        enemy_list.add(enemy)
        return enemy_list
    def renderPass(eloc):
        passe = Pass(x=eloc[0], y=eloc[1])
        passes = pygame.sprite.Group()
        passes.add(passe)
        return passes
    

'''
Setup
'''

clock = pygame.time.Clock()
pygame.init()
main = True

player = Player()
player.rect.x = 10  
player.rect.y = 10
player.rotate(rot)
player_list = pygame.sprite.Group()
player_list.add(player)

eloc = [730, 450]
enemy_list = []
enemy_list.append(Level.good(1,eloc))
eloc2 = [360, 60]

keys = [
    [pygame.K_DOWN,pygame.K_UP],
    [pygame.K_LEFT,pygame.K_RIGHT]
    ]


index,oc = 0,1

'''
Main Loop
'''


while main:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == ord('e'):
                player.rotate(rot)
                index = not index
            if event.key == ord('r'):
                player.rotate(-rot)
                index = not index
            if event.key == ord('o'):
                oc = int(not oc)
                enemy_list[0] = Level.good(oc,eloc)
                if len(enemy_list) == 1:
                    enemy_list.append(Level.renderPass(eloc2))
                else:
                    enemy_list.pop()
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                if event.key in keys[index]:
                    player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                if event.key in keys[index]:
                    player.control(steps, 0)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                if event.key in keys[index]:
                    player.control(0, steps)
            if event.key == pygame.K_UP or event.key == ord('w'):
                if event.key in keys[index]:
                    player.control(0, -steps)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                if event.key in keys[index]:
                    player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                if event.key in keys[index]:
                    player.control(-steps, 0)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                if event.key in keys[index]:
                    player.control(0, -steps)
            if event.key == pygame.K_UP or event.key == ord('w'):
                if event.key in keys[index]:
                    player.control(0, steps)
            if event.key == ord('o'):
                enemy_list[0] = Level.good(oc,eloc)

                
    
    #world.fill(WHITE)
    world.blit(backdrop, backdropbox)
    player.update()
    player_list.draw(world)
    #print(player.rect.x,player.rect.y)
    for enemy in enemy_list:
        enemy.draw(world)
    pygame.display.flip()
    clock.tick(fps)
