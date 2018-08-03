import pygame

from gui.utils import s, white


class Player:
    def __init__(self, globals, name, a, b, c):
        self.name = name
        self.a = a #how good a bot is at doing A
        self.b = b #how good B
        self.c = c #how good C

        self.points = 0 #points it has won
        self.win = 0
        self.loss = 0
        self.close = 0
        self.matches = 0
        self.opponents = [] #opponents it has faced
        self.taken = False #if it has played a match in the current round
        self.rank = 0

        #gui stuff
        self.pos = [-800,540]
        self.xv = 0
        self.yv = 0
        self.target = [960,540]
        self.a = 2
        self.colorFlag = 0 #none
        self.window = globals.window

        self.RECT_SIZE = (900,70)#64
        self.FONT_HEIGHT = int(self.RECT_SIZE[1]*0.7)
        self.boxFont = pygame.font.SysFont("futuraextra",self.FONT_HEIGHT)
        self.boxBg = pygame.transform.scale(globals.boxBgImage,self.RECT_SIZE)

    def render(self):
        #box
        x = self.pos[0] - self.RECT_SIZE[0]/2
        y = self.pos[1] - self.RECT_SIZE[1]/2
        #pygame.draw.rect(window,grey,(x,y,RECT_SIZE[0],RECT_SIZE[1]))
        RECT = pygame.Rect(x,y,self.RECT_SIZE[0],self.RECT_SIZE[1])
        self.window.blit(self.boxBg,RECT)
        #text
        string = "#" + str(self.rank) +" " + str(self.name)#+ str(self.points)
        string2 = str(self.points)
        textRECT = self.boxFont.render(string,True,white)
        textRECT2 = self.boxFont.render(string2,True,white)
        self.window.blit(textRECT,(x + self.FONT_HEIGHT/4, y + self.FONT_HEIGHT/4 ))
        self.window.blit(textRECT2,(self.RECT_SIZE[0] + x - self.FONT_HEIGHT/4 - textRECT2.get_width(), y + self.FONT_HEIGHT/4 ))

    def tick(self):
        xd = s(self.target[0] - self.pos[0]) #direction
        yd = s(self.target[1] - self.pos[1])
        xdis = abs(self.target[0] - self.pos[0]) #distance
        ydis = abs(self.target[1] - self.pos[1])

        ac = self.a
        tx = abs(self.xv)/ac
        if xdis > abs(self.xv * tx):
            self.xv += ac
        elif  xdis < abs(self.xv * tx):
            self.xv -= ac
        if xdis < ac or xdis < self.xv:
            self.pos[0] = self.target[0]
            self.xv = 0

        ty = abs(self.yv)/ac
        if ydis > abs(self.yv * ty):
            self.yv += ac
        elif ydis  < abs(self.yv * ty):
            self.yv -= ac
        if ydis < ac or ydis < self.yv:
            self.pos[1] = self.target[1]
            self.yv = 0

        self.pos[0] += self.xv*xd
        self.pos[1] += self.yv*yd

    def ts(self): #to string
        dif = int((abs(self.a - self.b) + abs(self.a - self.c) + abs(self.c - self.b))/3)

        total = str(self.name)
        total += (" a: %s b: %s c: %s Total: %s Bad: %s Points: %s" % (str(self.a),str(self.b),str(self.c),str(self.a + self.b + self.c), str(dif),str(self.points)))
        return total
