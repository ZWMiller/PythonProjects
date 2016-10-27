import pygame
from pygame.locals import *

class User:

    def __init__(self,man):
        self.balls = man
    
    def getInput(self):
        events = pygame.event.get()

        for e in events:
            if e.type is QUIT:
                return True
            
            elif e.type is KEYDOWN:
                if e.key is K_q:
                    return True
                if e.key is K_s:
                    self.balls.spawnBall()

        return False
