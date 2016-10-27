import pygame
import os
import sys
from pygame.locals import *

from ball import Ball
from ball import BallManager
from user import User

pygame.init()

class Main(object):

    def __init__(self):
        # print "INIT STARTED"
        
        pygame.display.set_caption("Press S to Spawn. Press Q to Quit.")
        screensize = (640, 480)
        surface = pygame.display.set_mode(screensize)
        
        file = 'music/bg3.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1,0.0)        
        
        man = BallManager()
        user = User(man)

        if pygame.font:
            font = pygame.font.Font(None, 36)
            
        pygame.display.flip()
        done = False

        timer = pygame.time.Clock()
        milliseconds = 0.
        seconds = 0
        minutes = 0
        score = 0 #score = numBalls*time

        while not done:
            surface.fill((50,50,50))
            man.draw(surface)
            done = user.getInput()
            if milliseconds > 1000:
                seconds += 1
                milliseconds -= 1000
                score += len(man.balls)
          
            milliseconds += timer.tick_busy_loop(200)
            text = font.render("Score: "+str(score), 1, (255,255,255))
            textpos = text.get_rect(centerx=surface.get_width()/2)
            surface.blit(text, textpos)
            pygame.display.flip()
            #pygame.time.Clock().tick(250)


Main()
    
