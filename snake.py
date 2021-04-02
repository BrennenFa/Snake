import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_ESCAPE,
    K_w,
    K_a,
    K_s,
    K_d,
    K_y,
    KEYDOWN,
    QUIT,
    )

pygame.init()
clock = pygame.time.Clock()
screenWidth = 800
screenHeight = 800

win = pygame.display.set_mode((screenWidth, screenHeight))


class Snake(object):
    def __init__(self, x, y, sideLength, speed):
        self.x = x
        self.y = y
        self.sideLength = sideLength
        self.list = [[self.x, self.y, self.sideLength, self.sideLength]]
        self.facing = 0
        self.length = 5
        self.speed = speed

        #test variables
        #self.now = pygame.time.get_ticks()
        #-self.lastActivate = pygame.time.get_ticks()


    def move(self, keys):
        #changing heading
        if keys[K_w] or keys[K_UP]:
            if self.length > 1:
                if self.facing != 1:
                    self.facing = 0
            else:
                self.facing = 0
            
        if keys[K_s] or keys[K_DOWN]:
            if self.length > 1:
                if self.facing != 0:
                    self.facing = 1
            else:
                self.facing = 1
            
        if keys[K_d] or keys[K_RIGHT]:
            if self.length > 1:
                if self.facing != 3:
                    self.facing = 2
            else:
                self.facing = 2
                
        if keys[K_a] or keys[K_LEFT]:
            if self.length > 1:
                if self.facing != 2:
                    self.facing = 3
            else:
                self.facing = 3

        #moving
        first = self.list[0].copy()
        if self.facing == 0:
            self.y -= self.speed
            #first[1] = self.y
            #self.list.append(first)

        elif self.facing == 1:
            self.y += self.speed
            #first[1] = self.y
            
            #self.list.append(first)
                         
        elif self.facing == 2:
            self.x += self.speed
            #first[0] = self.x

            #self.list.append(first)
               
        elif self.facing == 3:
            self.x -= self.speed
            #first[0] = self.x

            #self.list.append(first)
                         
#new ones go to end, removed ones go the the beginning
        
    def create(self):
        last = self.list[len(self.list)-1].copy()    
        if self.facing == 0:
            #endValue = (last[0], last[1] + self.height, self.width, self.height)
            last[1] = self.y
            self.list.append(last)
            
        elif self.facing == 1:
            #endValue = (last[0], last[1] - self.height, self.width, self.height)
            last[1] = self.y
            self.list.append(last)
    
        elif self.facing == 2:
           #endValue = (last[0] - self.width, last[1], self.width, self.height)
            last[0] = self.x
            self.list.append(last)

        elif self.facing == 3:
            #endValue = (last[0] + self.width, last[1], self.width, self.height)
            last[0] = self.x
            self.list.append(last)
        if len(self.list) > self.length:
            self.list.pop(0)



class Food(object):
    def __init__(self, sideLength):
        self.x = random.randint(0, screenWidth)
        self.x -= self.x % 20
        self.y = random.randint(0, screenHeight)
        self.y -= self.y % 20
        self.sideLength = sideLength
        self.hitbox = (self.x, self.y, self.sideLength, self.sideLength)



snake = Snake(int(screenWidth/2), int(screenHeight/2), 20, 20)
foodList = []
font1 = pygame.font.SysFont('comicsans', 30, False, False)

def redrawWindow(score):
    win.fill((0, 0, 0))
    for i in snake.list:
        pygame.draw.rect(win, (0, 255, 0), i)
    for pellet in foodList:
        pygame.draw.rect(win, [255, 255, 255], pellet.hitbox)
    score = font1.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score, (screenWidth - score.get_width() - 10, 10))
    pygame.display.flip()



running = True
game = True
score = 0

redrawWindow(score)
while running:
    events = pygame.event.get()
    while game:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game = False
            elif event.type == QUIT:
                game = False
        redrawWindow(score)
        keys = pygame.key.get_pressed()
        if len(foodList) < 1:
            pellet = Food(20)
            foodList.append(pellet)

        snake.move(keys)
        snake.create()
        
        for square in snake.list:
            for pellet in foodList:
                if square[0] < pellet.hitbox[0] + pellet.hitbox[2] and square[0] + square[2] > pellet.hitbox[0]:
                    if square[1] < pellet.hitbox[1] + pellet.hitbox[3] and square[1] + square[2] > pellet.hitbox[1]:        
                        snake.length += 5
                        score += 1
                        foodList.clear()


        secondList = snake.list.copy()
        head = secondList.pop(len(secondList) - 1)
        for square in secondList:
            if square == head:
                game = False
        if head[0] + head[2] < 0 or head[0] > screenWidth or head[1] < 0 or head[1] - head[3] > screenHeight:
            game = False


        clock.tick(10)

    again = font1.render("Press 'y' to Play Again", 1, (255, 255, 255))
    win.blit(again, (int(screenWidth/2) - int(again.get_width()/2), int(screenHeight/2)))
    pygame.display.flip()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                game = True
                snake = Snake(int(screenWidth/2), int(screenHeight/2), 20, 20)
                foodList = []
                break

        



    #for i in range(0, len(snake.list) - 1):
    #    if snake.list[0][0] < snake.list[len(snake.list) - i][0] + snake.list[len(snake.list) - i][2] and snake.list[0][0] + snake.list[0][2] > snake.list[len(snake.list) - i][0]:
    #        if snake.list[0][1] < snake.list[len(snake.list) - i][1] + snake.list[len(snake.list) - i][3] and snake.list[0][1] + snake.list[0][2] > snake.list[len(snake.list) - i][1]:
    #            game = False


    #if snake.list[0][0] < snake.list[3][0] + snake.list[3][2] and snake.list[0][0] + snake.list[0][2] > snake.list[3][0]:
    #    if snake.list[0][1] < snake.list[3][1] + snake.list[3][3] and snake.list[0][1] + snake.list[0][2] > snake.list[3][1]:
    #        print('hello')
    #for square in snake.list:
    #    if square[0] < snake.list[len(snake.list) - 1][0] + snake.list[len(snake.list) - 1][2] and square[0] + square[2] > snake.list[len(snake.list) - 1][0]:
    #        if square[1] < snake.list[len(snake.list) - 1][1] + snake.list[len(snake.list) - 1][3] and square[1] + square[2] > snake.list[len(snake.list) - 1][1]:
    #            if square != snake.list[len(snake.list) - 1]:
    #                game = False

    #for i in range(0, len(snake.list) - 2):
    #    if snake.list[i + 1] == snake.list[0]:
    #        game = False
