# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random
import pygame
import sys
import math
from dataclasses import dataclass
from pygame.locals import *

@dataclass
class Apple:
    coord: dict
    color: tuple

@dataclass
class Worm:
    coords: dict
    color: tuple
    direction: str

@dataclass
class Bullet:
    coords: dict
    direction: str

@dataclass
class Rocks:
    coord: dict

FPS = 5
WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
CELLSIZE = 20
RADIUS = math.floor(CELLSIZE/2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
GRAY = (131, 131, 131)
YELLOW = (255,255,0)
SNAKEGREEN = (14, 181, 14)
SNAKEORANGE = (226, 112, 17)
SNAKEPINK = (112, 0, 63)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Sneaky Snake')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    startx2 = random.randint(5, CELLWIDTH - 6)
    starty2 = random.randint(5, CELLHEIGHT - 6)

    Worm1 = Worm([{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}], GREEN, RIGHT)

    Worm2 = Worm([{'x': startx2,     'y': starty2},
                  {'x': startx2 - 1, 'y': starty2},
                  {'x': startx2 - 2, 'y': starty2}], SNAKEORANGE, RIGHT)

    # Start the apple in a random place.
    Red_Apple = Apple(getRandomLocation(), RED)
    Green_Apple = Apple(getRandomLocation(), GREEN)
    Yellow_Apple = Apple(getRandomLocation(), YELLOW)
    Orange_Apple = Apple(getRandomLocation(), SNAKEORANGE)
    Pink_Apple = Apple(getRandomLocation(), SNAKEPINK)

    bullets = []
    rocks = []
    spawned_rocks = False


    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT and Worm1.direction != RIGHT):
                    Worm1.direction = LEFT
                    if (Worm2.direction != RIGHT):
                        Worm2.direction = LEFT
                elif (event.key == K_RIGHT and Worm1.direction != LEFT):
                    Worm1.direction = RIGHT
                    if (Worm2.direction != LEFT):
                        Worm2.direction = RIGHT
                elif (event.key == K_UP and Worm1.direction != DOWN):
                    Worm1.direction = UP
                    if (Worm2.direction != DOWN):
                        Worm2.direction = UP
                elif (event.key == K_DOWN and Worm1.direction != UP):
                    Worm1.direction = DOWN
                    if (Worm2.direction != UP):
                        Worm2.direction = DOWN
                elif (event.key == K_SPACE):
                    d = Worm1.direction
                    if (d == RIGHT):
                        x = Worm1.coords[HEAD]['x'] + 1
                        y = Worm1.coords[HEAD]['y']
                    elif (d == LEFT):
                        x = Worm1.coords[HEAD]['x'] - 1
                        y = Worm1.coords[HEAD]['y']
                    elif (d == UP):
                        x = Worm1.coords[HEAD]['x']
                        y = Worm1.coords[HEAD]['y'] - 1
                    elif (d == DOWN):
                        x = Worm1.coords[HEAD]['x']
                        y = Worm1.coords[HEAD]['y'] + 1
                    c = {'x': x, 'y': y}
                    B = Bullet(c, d)
                    bullets.append(B)
                elif (event.key == K_q):
                    d = Worm2.direction
                    if (d == RIGHT):
                        x = Worm2.coords[HEAD]['x'] + 1
                        y = Worm2.coords[HEAD]['y']
                    elif (d == LEFT):
                        x = Worm2.coords[HEAD]['x'] - 1
                        y = Worm2.coords[HEAD]['y']
                    elif (d == UP):
                        x = Worm2.coords[HEAD]['x']
                        y = Worm2.coords[HEAD]['y'] - 1
                    elif (d == DOWN):
                        x = Worm2.coords[HEAD]['x']
                        y = Worm2.coords[HEAD]['y'] + 1
                    c = {'x': x, 'y': y}
                    B = Bullet(c, d)
                    bullets.append(B)
                elif (event.key == K_a and Worm2.direction != RIGHT):
                    Worm2.direction = LEFT
                elif (event.key == K_d and Worm2.direction != LEFT):
                    Worm2.direction = RIGHT
                elif (event.key == K_w and Worm2.direction != DOWN):
                    Worm2.direction = UP
                elif (event.key == K_s and Worm2.direction != UP):
                    Worm2.direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if Worm1.coords[HEAD]['x'] == -1 or Worm1.coords[HEAD]['x'] == CELLWIDTH or Worm1.coords[HEAD]['y'] == -1 or Worm1.coords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for b in bullets:
            if Worm1.coords[HEAD]['x'] == b.coords['x'] and Worm1.coords[HEAD]['y'] == b.coords['y']:
                rock = {'x': b.coords['x'], 'y': b.coords['y']}
                Rock = Rocks(rock) 
                rocks.append(Rock)
        for r in rocks:
            if Worm1.coords[HEAD]['x'] == r.coord['x'] and Worm1.coords[HEAD]['y'] == r.coord['y']:
                return #game over
        seg = 0
        for wormBody in Worm1.coords[1:]:
            seg += 1
            for b in bullets:
                if wormBody['x'] == b.coords['x'] and wormBody['y'] == b.coords['y']:
                    rock = {'x': b.coords['x'], 'y': b.coords['y']}
                    Rock = Rocks(rock) 
                    rocks.append(Rock)
                    for x in range(0, seg):   
                        del Worm1.coords[-1]
            if wormBody['x'] == Worm1.coords[HEAD]['x'] and wormBody['y'] == Worm1.coords[HEAD]['y']:
                return # game over
            elif wormBody['x'] == Worm2.coords[HEAD]['x'] and wormBody['y'] == Worm2.coords[HEAD]['y']:
                return # game over
        
        if Worm2.coords[HEAD]['x'] == -1 or Worm2.coords[HEAD]['x'] == CELLWIDTH or Worm2.coords[HEAD]['y'] == -1 or Worm2.coords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for b in bullets:
            if Worm2.coords[HEAD]['x'] == b.coords['x'] and Worm2.coords[HEAD]['y'] == b.coords['y']:
                rock = {'x': b.coords['x'], 'y': b.coords['y']}
                Rock = Rocks(rock) 
                rocks.append(Rock)
        for r in rocks:
            if Worm2.coords[HEAD]['x'] == r.coord['x'] and Worm2.coords[HEAD]['y'] == r.coord['y']:
                return #game over
        seg = 0
        for wormBody in Worm2.coords[1:]:
            seg += 1
            for b in bullets:
                if wormBody['x'] == b.coords['x'] and wormBody['y'] == b.coords['y']:
                    rock = {'x': b.coords['x'], 'y': b.coords['y']}
                    Rock = Rocks(rock) 
                    rocks.append(Rock)
                    for x in range(1, seg):   
                        del Worm2.coords[-1]
            if wormBody['x'] == Worm2.coords[HEAD]['x'] and wormBody['y'] == Worm2.coords[HEAD]['y']:
                return # game over
            elif wormBody['x'] == Worm1.coords[HEAD]['x'] and wormBody['y'] == Worm1.coords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apple
        if Worm1.coords[HEAD]['x'] == Red_Apple.coord['x'] and Worm1.coords[HEAD]['y'] == Red_Apple.coord['y']:
            # don't remove worm's tail segment
            Red_Apple.coord = getRandomLocation() # set a new apple somewhere
        elif Worm1.coords[HEAD]['x'] == Green_Apple.coord['x'] and Worm1.coords[HEAD]['y'] == Green_Apple.coord['y']:
            Green_Apple.coord = getRandomLocation()
        elif Worm1.coords[HEAD]['x'] == Yellow_Apple.coord['x'] and Worm1.coords[HEAD]['y'] == Yellow_Apple.coord['y']:
            Yellow_Apple.coord = getRandomLocation()
        elif Worm1.coords[HEAD]['x'] == Orange_Apple.coord['x'] and Worm1.coords[HEAD]['y'] == Orange_Apple.coord['y']:
            Orange_Apple.coord = getRandomLocation()
        elif Worm1.coords[HEAD]['x'] == Pink_Apple.coord['x'] and Worm1.coords[HEAD]['y'] == Pink_Apple.coord['y']:
            Pink_Apple.coord = getRandomLocation()
        else:
            del Worm1.coords[-1] # remove worm's tail segment

        if Worm2.coords[HEAD]['x'] == Red_Apple.coord['x'] and Worm2.coords[HEAD]['y'] == Red_Apple.coord['y']:
            # don't remove worm's tail segment
            Red_Apple.coord = getRandomLocation() # set a new apple somewhere
        elif Worm2.coords[HEAD]['x'] == Green_Apple.coord['x'] and Worm2.coords[HEAD]['y'] == Green_Apple.coord['y']:
            Green_Apple.coord = getRandomLocation()
        elif Worm2.coords[HEAD]['x'] == Yellow_Apple.coord['x'] and Worm2.coords[HEAD]['y'] == Yellow_Apple.coord['y']:
            Yellow_Apple.coord = getRandomLocation()
        elif Worm2.coords[HEAD]['x'] == Orange_Apple.coord['x'] and Worm2.coords[HEAD]['y'] == Orange_Apple.coord['y']:
            Orange_Apple.coord = getRandomLocation()
        elif Worm2.coords[HEAD]['x'] == Pink_Apple.coord['x'] and Worm2.coords[HEAD]['y'] == Pink_Apple.coord['y']:
            Pink_Apple.coord = getRandomLocation()
        else:
            del Worm2.coords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if Worm1.direction == UP:
            newHead = {'x': Worm1.coords[HEAD]['x'], 'y': Worm1.coords[HEAD]['y'] - 1}
        elif Worm1.direction == DOWN:
            newHead = {'x': Worm1.coords[HEAD]['x'], 'y': Worm1.coords[HEAD]['y'] + 1}
        elif Worm1.direction == LEFT:
            newHead = {'x': Worm1.coords[HEAD]['x'] - 1, 'y': Worm1.coords[HEAD]['y']}
        elif Worm1.direction == RIGHT:
            newHead = {'x': Worm1.coords[HEAD]['x'] + 1, 'y': Worm1.coords[HEAD]['y']}
        Worm1.coords.insert(0, newHead)   #have already removed the last segment

        if Worm2.direction == UP:
            newHead = {'x': Worm2.coords[HEAD]['x'], 'y': Worm2.coords[HEAD]['y'] - 1}
        elif Worm2.direction == DOWN:
            newHead = {'x': Worm2.coords[HEAD]['x'], 'y': Worm2.coords[HEAD]['y'] + 1}
        elif Worm2.direction == LEFT:
            newHead = {'x': Worm2.coords[HEAD]['x'] - 1, 'y': Worm2.coords[HEAD]['y']}
        elif Worm2.direction == RIGHT:
            newHead = {'x': Worm2.coords[HEAD]['x'] + 1, 'y': Worm2.coords[HEAD]['y']}
        Worm2.coords.insert(0, newHead)   #have already removed the last segment

        for b in bullets:
            if b.direction == UP:
                newCoord = {'x': b.coords['x'], 'y': b.coords['y'] - 1}
            elif b.direction == DOWN:
                newCoord = {'x': b.coords['x'], 'y': b.coords['y'] + 1}
            elif b.direction == LEFT:
                newCoord = {'x': b.coords['x'] - 1, 'y': b.coords['y']}
            elif b.direction == RIGHT:
                newCoord = {'x': b.coords['x'] + 1, 'y': b.coords['y']}
            b.coords = newCoord


        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(Worm1)
        drawWorm(Worm2)
        drawApple(Red_Apple)
        drawApple(Green_Apple)
        drawApple(Yellow_Apple)
        drawApple(Orange_Apple)
        drawApple(Pink_Apple)
        drawScore(Worm1)
        drawScore(Worm2)
        for i in bullets:
            drawBullet(i)
        for i in rocks:
            drawRock(i)
        worm1_length = len(Worm1.coords)
        worm2_length = len(Worm2.coords)
        if (spawned_rocks == False and worm1_length > 10 or worm2_length > 10):
            stone = Rocks(getRandomLocation())
            throwStones(stone)
            rocks.append(stone)
            spawned_rocks = True
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, YELLOW)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Sneaky!', True, SNAKEGREEN, SNAKEORANGE)
    titleSurf2 = titleFont.render('Snake!', True, SNAKEPINK)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 10)
    overRect.midtop = (math.floor(WINDOWWIDTH / 2), gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(Worm):
    score = len(Worm.coords) - 3
    if (Worm.color == SNAKEORANGE):
        scoreSurf = BASICFONT.render('Snake2 Score: %s ' % (score), True, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 150, 15)
        DISPLAYSURF.blit(scoreSurf, scoreRect)
    else:
        scoreSurf2 = BASICFONT.render('Snake1 Score: %s  ' % (score), True, WHITE)
        scoreRect2 = scoreSurf2.get_rect()
        scoreRect2.topright = (WINDOWWIDTH - 150, 15)
        DISPLAYSURF.blit(scoreSurf2, scoreRect2)


def drawBullet(Bullet):
    if (Bullet.direction == LEFT):
        x = Bullet.coords['x'] * CELLSIZE
        y = Bullet.coords['y'] * CELLSIZE
    elif (Bullet.direction == RIGHT):
        x = Bullet.coords['x'] * CELLSIZE
        y = Bullet.coords['y'] * CELLSIZE
    elif (Bullet.direction == UP):
        y = Bullet.coords['y'] * CELLSIZE
        x = Bullet.coords['x'] * CELLSIZE
    elif (Bullet.direction == DOWN): 
        x = Bullet.coords['x'] * CELLSIZE
        y = Bullet.coords['y'] * CELLSIZE
    xcenter = x + math.floor(CELLSIZE/2)
    ycenter = y + math.floor(CELLSIZE/2)
    #appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    #pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    pygame.draw.circle(DISPLAYSURF, WHITE,(xcenter,ycenter),RADIUS)

def drawWorm(Worm):
    for coord in Worm.coords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        if (Worm.color == SNAKEORANGE):
            pygame.draw.rect(DISPLAYSURF, SNAKEPINK, wormSegmentRect)
        else:
            pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, Worm.color, wormInnerSegmentRect)


def drawApple(Apple):
    x = Apple.coord['x'] * CELLSIZE
    y = Apple.coord['y'] * CELLSIZE
    xcenter = Apple.coord['x'] * CELLSIZE + math.floor(CELLSIZE/2)
    ycenter = Apple.coord['y'] * CELLSIZE+ math.floor(CELLSIZE/2)
    pygame.draw.circle(DISPLAYSURF, Apple.color,(xcenter,ycenter),RADIUS)

def drawRock(rock):
    x = rock.coord['x'] * CELLSIZE
    y = rock.coord['y'] * CELLSIZE
    xcenter = rock.coord['x'] * CELLSIZE + math.floor(CELLSIZE/2)
    ycenter = rock.coord['y'] * CELLSIZE+ math.floor(CELLSIZE/2)
    pygame.draw.circle(DISPLAYSURF, GRAY,(xcenter,ycenter),RADIUS)

def throwStones(Stone):
    x = Stone.coord['x'] * CELLSIZE
    y = Stone.coord['y'] * CELLSIZE
    xcenter = Stone.coord['x'] * CELLSIZE + math.floor(CELLSIZE/2)
    ycenter = Stone.coord['y'] * CELLSIZE+ math.floor(CELLSIZE/2)
    pygame.draw.circle(DISPLAYSURF, GRAY,(xcenter,ycenter),RADIUS)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()