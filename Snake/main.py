import random as rand
import pygame as pg
import time as tm
import os

pg.init()
screenX, screenY = 480, 480
screen = pg.display.set_mode((screenX, screenY))
pg.display.set_caption("Snake")
icon = pg.image.load(os.path.join("images", "Snake.jpg"))
pg.display.set_icon(icon)

score = 0
step = 15
fullBody = []
appleX = rand.randint(40, 440)
appleY = rand.randint(40, 440)
direction = "up"
forward = 0
FPS = 15

class Snake:
    #Constructor
    def __init__(self, x, y, width, height):
        global screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def body(self):
        pg.draw.rect(screen, (255, 0, 0), pg.Rect(self.x, self.y, self.width, self.height))

    def addX(self, step):
        self.x += step
    def addY(self, step):
        self.y += step

    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y

head = Snake(100, 100, 15, 15)

def restart():
    global fullBody, head, screen, screenY, screenX, score, appleX, appleY
    fullBody.clear()
    score = 0
    head = Snake(rand.randint(40, screenX-40), rand.randint(40, screenY-40), 15, 15)
    appleX = rand.randint(40, 440)
    appleY = rand.randint(40, 440)
    tm.sleep(1)
    menu()

def move():
    global appleY, appleX, direction, head, step, forward, score, head
    keys = pg.key.get_pressed()

    if (appleX <= head.getX() + 7.5 <= (appleX + screenX/20) and (appleY - screenY/20) <= head.getY() <= appleY):
        appleX = rand.randint(0, 440)
        appleY = rand.randint(0, 440)
        score += 1
        if len(fullBody) > 0:
            newBody = Snake(fullBody[len(fullBody)-1].getX(), fullBody[len(fullBody)-1].getY(), 15, 15)
        else:
            newBody = Snake(head.getX(), head.getY(), 15, 15)
        fullBody.append(newBody)

    if keys[pg.K_UP] and direction != "down":
        direction = "up"
        forward = 0
    elif keys[pg.K_DOWN] and direction != "up":
        direction = "down"
        forward = 1
    elif keys[pg.K_RIGHT] and direction != "left":
        direction = "right"
        forward = 2
    elif keys[pg.K_LEFT] and direction != "right":
        direction = "left"
        forward = 3

    if head.getX() >= 480: head.setX(0)
    elif head.getX() <= 0: head.setX(480)
    elif head.getY() >= 480: head.setY(0)
    elif head.getY() <= 0: head.setY(480)

    if forward == 0: head.addY(-step)
    elif forward == 1: head.addY(step)
    elif forward == 2: head.addX(step)
    elif forward == 3: head.addX(-step)

    x, y = 0, 0
    for i in range(len(fullBody)-1, 0, -1):
        x = fullBody[i-1].getX()
        y = fullBody[i-1].getY()
        fullBody[i].setX(x)
        fullBody[i].setY(y)

        if (head.getX() == fullBody[i].getX() and
            head.getY() == fullBody[i].getY()):
            file = open("High Score", "r")
            if score > int(file.readline()):
                file = open("High Score", "w")
                file.write(str(score))
                file.close()
            pg.display.update()
            restart()

    if len(fullBody) > 0:
        x = head.getX()
        y = head.getY()
        fullBody[0].setX(x)
        fullBody[0].setY(y)

def redraw():
    global screen, screenY, screenX, head, fullBody
    #BackGround
    bg = pg.transform.scale(
        pg.image.load(
            #"PyGame/Snake/images/BackGround.png"
            os.path.join("images", "BackGround.png")
        )
    , (screenX, screenY))
    screen.blit(bg, (0, 0))

    #Apple
    ap = pg.transform.scale(
        pg.image.load(
            #"PyGame/Snake/images/apple.png"
            os.path.join("images", "apple.png")
        )
    , (screenX/40, screenY/40))
    screen.blit(ap, (appleX, appleY))
    scoreFont = pg.font.SysFont("freesansbold", 32, True, (255, 255, 255)).render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(scoreFont, (0, 0))

    head.body()
    for i in range(len(fullBody)): fullBody[i].body()

def main():
    global FPS
    while True:
        pg.time.Clock().tick(FPS)

        for events in pg.event.get():
            if events.type == pg.QUIT:
                quit()
        redraw()
        move()
        pg.display.update()

def set_level():
    global FPS, screen, screenY, screenX

    while True:
        pg.time.delay(50)
        #BackGround
        bg1 = pg.transform.scale(
            pg.image.load(
                #"PyGame/Snake/images/BackGround.png"
                os.path.join("images", "BackGround.png")
            )
        , (screenX, screenY))
        screen.blit(bg1, (0, 0))

        for events in pg.event.get():
            if events.type == pg.QUIT:
                quit()

        level1 = pg.font.SysFont("freesansbold", 32, True, (255, 255, 255)).render("Level 1 (Press 1)", True, (255, 255, 255))
        level2 = pg.font.SysFont("freesansbold", 32, True, (255, 255, 255)).render("Level 2 (Press 2)", True, (255, 255, 255))
        level3 = pg.font.SysFont("freesansbold", 32, True, (255, 255, 255)).render("Level 3 (Press 3)", True, (255, 255, 255))

        if pg.key.get_pressed()[pg.K_1]:
            FPS = 15
            main()
        elif pg.key.get_pressed()[pg.K_2]:
            FPS = 30
            main()
        elif pg.key.get_pressed()[pg.K_3]:
            FPS = 60
            main()

        screen.blit(level1, ((screenX / 2) - (level1.get_width()/2), (screenY / 2)-50))
        screen.blit(level2, ((screenX / 2) - (level2.get_width()/2), (screenY / 2)))
        screen.blit(level3, ((screenX / 2) - (level3.get_width()/2), (screenY / 2)+50))
        pg.display.update()

def menu():
    global screen, screenY, screenX, FPS

    while True:
        pg.time.delay(50)

        #BackGround
        bg1 = pg.transform.scale(
            pg.image.load(
                #"PyGame/Snake/images/BackGround.png"
                os.path.join("images", "BackGround.png")
            )
        , (screenX, screenY))
        menuFont = pg.font.SysFont("freesansbold", 32, True, (255, 255, 255)).render("Press Space to begin...", True, (255, 255, 255))
        file = open("High Score", "r")
        highScore = pg.font.SysFont("freesansbold", 32, True, (255, 255, 255)).render(f"High Score: {file.readline()}", True, (255, 255, 255))
        file.close()
        screen.blit(bg1, (0, 0))
        screen.blit(menuFont, (screenX/2 - menuFont.get_width()/2, screenY/2))
        screen.blit(highScore, (screenX/2 - highScore.get_width()/2, screenY/2.5))
        for events in pg.event.get():
            if events.type == pg.QUIT:
                quit()
        if pg.key.get_pressed()[pg.K_SPACE]:
            set_level()

        pg.display.update()

if __name__ == "__main__":
    menu()