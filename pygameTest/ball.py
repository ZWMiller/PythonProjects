import pygame
from random import randint

class Ball(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.counter = 0
        self.isRand = randint(0,1)
        self.vx = 1
        self.vy = 1
        self.size = (randint(20,50),randint(20,50))
        self.color = (255,255,255)

    def update(self,man):
        self.x += self.vx
        self.y += self.vy
        self.counter += 1
        
        if self.counter > 500:
            self.regenBall()
                
        if self.x > 640:
            temp = self.vx
            self.vx = -temp

        if self.x < 0:
            temp = self.vx
            self.vx = -temp

        if self.y > 480:
            temp = self.vy
            self.vy = -temp

        if self.y < 0:
            temp = self.vy
            self.vy = -temp
        
        if self.isRand==1:
            self.vx = randint(-1,1)
            self.vy = randint(-1,1)
        
    def draw(self,surface):
        geom = pygame.Rect((self.x,self.y),self.size)
        pygame.draw.ellipse(surface,self.color,geom)

    def regenBall(self):
        r = randint(0,255)
        g = randint(0,255)
        b = randint(0,255)
        self.color = (r,g,b)
        self.isRand = randint(0,1)
        self.vx = randint(-2,2)
        self.vy = randint(-2,2)
        self.counter = 0

class BallManager(object):
    
    def __init__(self):
        self.balls = []

    def spawnBall(self):
        ball = Ball()
        r = randint(0,255)
        g = randint(0,255)
        b = randint(0,255)
        ball.color = (r,g,b)
        ball.x = randint(0,640)
        ball.y = randint(0,480)
        ball.vx = randint(-2,2)
        ball.vy = randint(-2,2)
        self.balls.append(ball)

    def __iter__(self):
        return self.balls._iter_()

    def draw(self,surface):
        for ball in self.balls:
            ball.update(self)
            ball.draw(surface)

    

        
