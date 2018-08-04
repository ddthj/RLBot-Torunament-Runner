import string
import time
import random
import pygame
import sys

from runner import start

"""
RLBot Semi-Swiss matchmaker and gui

This program generates a modified Swiss tournament that includes elimination to help minimize the number of matches and minimize unfairness
also gui

Please spare me for my trash code I had to start writing this before I could plan it
"""

window, boxBgImage = start()

hype = gui()

"""
class playerBox():
    def __init__(self,playerName):
        self.name = playerName
        self.pos = [-100,540]
        self.xv = 0
        self.yv = 0
        self.target = [960,540]
        self.a = 2
        self.colorFlag = 0 #none

    def render(self):
        #box
        x = self.pos[0] - RECT_SIZE[0]/2
        y = self.pos[1] - RECT_SIZE[1]/2
        pygame.draw.rect(window,grey,(x,y,RECT_SIZE[0],RECT_SIZE[1]))
        #text
        string = str(self.name) + "  " + str(self.points)
        textRECT = boxFont.render(string,True,white)
        window.blit(textRECT,(x + FONT_HEIGHT/4, y + FONT_HEIGHT/4 )) 
    def tick(self):
        xd = s(self.target[0] - self.pos[0]) #direction
        yd = s(self.target[1] - self.pos[1])
        xdis = abs(self.target[0] - self.pos[0]) #distance
        ydis = abs(self.target[1] - self.pos[1])
        if xdis < self.a:
            ac = self.a/2
            if xdis <= ac:
                self.xv = 0
                self.pos[0] = self.target[0]
        else:
            ac = self.a
        tx = abs(self.xv)/ac
        if xdis > abs(self.xv * tx):
            self.xv += ac
        elif  xdis < abs(self.xv * tx):
            self.xv -= ac
        if ydis < self.a:
            ac = self.a/2
            if ydis <= ac:
                self.yv = 0
                self.y = self.target[1]
        else:
            ac = self.a
        ty = abs(self.yv)/ac
        if ydis > abs(self.yv * ty):
            self.yv += ac
        elif ydis <abs(self.yv * ty):
            self.yv -= ac
        self.pos[0] += self.xv*xd
        self.pos[1] += self.yv*yd
"""
