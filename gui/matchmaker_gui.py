import pygame
import time

import sys

from match_making.match import Match
from gui.utils import blue, white, onScreen, randomTarget, RANKS, DURING_MATCH, UPCOMING_MATCHES


class Gui:
    def __init__(self, globals):
        self.mode = 0  #0 = list, 1 = match
        self.scroll = 1

        self.RECT_SIZE = (900,70)#64
        self.FONT_HEIGHT = int(self.RECT_SIZE[1]*0.7)
        self.boxFont = pygame.font.SysFont("futuraextra",self.FONT_HEIGHT)
        self.boxBg = pygame.transform.scale(globals.boxBgImage, self.RECT_SIZE)
        self.backBg = pygame.image.load('logo/1.jpg')

        self.tny = Match(globals)
        self.matches = self.tny.matchRound()
        self.finished = []
        self.boxBgImage = globals.boxBgImage
        self.globals = globals
        self.window = globals.window
        
        self.popMatch = False
        self.run()

    def changeRECT(self,size):
        self.RECT_SIZE = size
        self.FONT_HEIGHT = int(size[1]*0.7)
        self.boxBg = pygame.transform.scale(self.boxBgImage,self.RECT_SIZE)
        self.boxFont = pygame.font.SysFont("futuraextra",self.FONT_HEIGHT)
        for item in self.tny.finish():
            item.RECT_SIZE = size
            item.FONT_HEIGHT = int(size[1]*0.7)
            item.boxBg = pygame.transform.scale(self.boxBgImage,self.RECT_SIZE)
            item.boxFont = pygame.font.SysFont("futuraextra",item.FONT_HEIGHT)


    def run(self):
        clock = pygame.time.Clock()
        time.sleep(1)
        while 1:   
            clock.tick(40)
            self.window.fill(blue)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and self.scroll <= 0:
                        self.scroll += 1
                    elif event.button == 5:
                        self.scroll -=1
                elif event.type == pygame.KEYDOWN:
                    if event.key == 50: # and self.mode == 0:
                        self.mode = UPCOMING_MATCHES
                    elif event.key == 49: # and self.mode == 3:
                        self.mode = RANKS
                    elif event.key == 51:
                        self.mode = DURING_MATCH
                    elif event.key == 97 and self.mode == DURING_MATCH: #A Wins
                        self.matches[0].a.win += 1
                        self.matches[0].a.points += 2
                        self.matches[0].a.opponents.append(self.matches[0].b)

                        self.matches[0].b.opponents.append(self.matches[0].a)
                        self.matches[0].b.loss += 1
                         
                        self.popMatch = True
                    elif event.key == 115 and self.mode == DURING_MATCH: #A Wins Close Game
                        self.matches[0].a.win += 1
                        self.matches[0].a.points += 2
                        self.matches[0].a.opponents.append(self.matches[0].b)

                        self.matches[0].b.opponents.append(self.matches[0].a)
                        self.matches[0].b.points += 1
                        self.matches[0].b.loss += 1
                        
                        self.popMatch = True
                    elif event.key == 100 and self.mode == DURING_MATCH:#B Wins Close Game
                        self.matches[0].a.loss += 1
                        self.matches[0].a.points += 1
                        self.matches[0].a.opponents.append(self.matches[0].b)

                        self.matches[0].b.opponents.append(self.matches[0].a)
                        self.matches[0].b.points +=2
                        self.matches[0].b.win += 1
                         
                        self.popMatch = True
                    elif event.key == 102 and self.mode == DURING_MATCH: #B Wins
                        self.matches[0].a.loss += 1
                        self.matches[0].a.opponents.append(self.matches[0].b)

                        self.matches[0].b.opponents.append(self.matches[0].a)
                        self.matches[0].b.points += 2
                        self.matches[0].b.win += 1
                         
                        self.popMatch = True

            if self.mode == RANKS:
                if self.popMatch == True:
                    self.popMatch = False
                    self.matches.pop(0)
                self.show_ranks()
            elif self.mode == DURING_MATCH:
                self.start_match()
            elif self.mode == UPCOMING_MATCHES:
                self.show_upcoming_matches()

            for item in self.tny.finish():
                item.tick()
                item.render()

            if len(self.matches) < 1:
                if self.tny.firstRounds > 1:
                    self.tny.sortPlayers(False)
                    self.tny.firstRounds -= 1
                    self.matches = self.tny.matchRound()
                else:
                    self.tny.sortPlayers(False)
                    self.tny.cut(0)
                    self.matches  = self.tny.matchRound()

            pygame.display.update()

    def start_match(self):
        if self.RECT_SIZE[0] != 640:
            self.changeRECT((640,50))
        for item in self.tny.finish():
            if onScreen(item.target):
                item.target = randomTarget()
        y = self.RECT_SIZE[1] 
        xa = 50 + self.RECT_SIZE[0]/2
        xb = 1870 - self.RECT_SIZE[0]/2
        self.matches[0].a.target = [xa,y]
        self.matches[0].b.target = [xb,y]

    def show_ranks(self):
        if self.RECT_SIZE[0] !=900:
            self.scroll = 1
            self.changeRECT((900,70))
        bgRect = pygame.Rect(0,0,1920,1080)
        self.window.blit(self.backBg,bgRect)
        string = "Current Ranks"
        rect = self.boxFont.render(string,True,white)
        y =self.RECT_SIZE[1] + int(self.RECT_SIZE[1] * 1.1) * self.scroll
        if self.scroll == 1:
            self.window.blit(rect,(960- rect.get_width()/2,y/4))
        for item in self.tny.finish():
            item.target = [960,y]
            y += int(self.RECT_SIZE[1] * 1.1)

    def show_upcoming_matches(self):
        bgRect = pygame.Rect(0,0,1920,1080)
        self.window.blit(self.backBg,bgRect)
        if self.RECT_SIZE[0] !=425:
            self.changeRECT((425,35))
        for item in self.tny.finish():
            if onScreen(item.target):
                item.target = randomTarget()
        string = "Upcoming Matches"
        rect = self.boxFont.render(string,True,white)

        vs = "VS"
        vsRect = self.boxFont.render(vs,True,white)

        y =self.RECT_SIZE[1] + int(self.RECT_SIZE[1] * 1.1)*2
        self.window.blit(rect,(960- rect.get_width()/2,y/4))
        for x in range(len(self.matches)):
            xa = int(960 - 25 - self.RECT_SIZE[0]/2)
            xb = int(960 + 25 +self.RECT_SIZE[0]/2)
            self.matches[x].a.target = [xa,y]
            self.matches[x].b.target = [xb,y]
            self.window.blit(vsRect,(960- vsRect.get_width()/2,y-int(0.2*self.RECT_SIZE[1])))
            y += int(self.RECT_SIZE[1] * 1.1)*2
            
