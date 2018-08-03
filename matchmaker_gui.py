import string
import time
import random
import pygame
import sys
"""
RLBot Semi-Swiss matchmaker and gui

This program generates a modified Swiss tournament that includes elimination to help minimize the number of matches and minimize unfairness
also gui

Please spare me for my trash code I had to start writing this before I could plan it
"""


white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
grey = (150,150,150)
pygame.init()
window = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("TournamentRunner")
boxBgImage = pygame.image.load('logo/5.png')

def randomTarget():
    x = random.randint(-1200,2500)
    while x < 1920 and x >-900 :
        x = random.randint(-1200,2500)

    y = random.randint(-1200,2500)
    while y < 1080 and y >-100 :
        y = random.randint(-1200,2500)

    return [x,y]

def onScreen(target):
    if target[0] < 1920 and target[0] > 0:
        if target[1] > 0 and target[1] < 1080:
            return True
    return False
        

def s(x):
    if x <= 0:
        return -1
    else:
        return 1

class gui():
    def __init__(self):
        self.mode = 0 #0 = list, 1 = match
        self.scroll = 1

        self.RECT_SIZE = (900,70)#64
        self.FONT_HEIGHT = int(self.RECT_SIZE[1]*0.7)
        self.boxFont = pygame.font.SysFont("futuraextra",self.FONT_HEIGHT)
        self.boxBg = pygame.transform.scale(boxBgImage,self.RECT_SIZE)
        self.backBg = pygame.image.load('logo/1.jpg')

        self.tny = match()
        self.matches = self.tny.matchRound()
        self.finished = []
        
        self.run()

    def changeRECT(self,size):
        self.RECT_SIZE = size
        self.FONT_HEIGHT = int(size[1]*0.7)
        self.boxBg = pygame.transform.scale(boxBgImage,self.RECT_SIZE)
        self.boxFont = pygame.font.SysFont("futuraextra",self.FONT_HEIGHT)
        for item in self.tny.finish():
            item.RECT_SIZE = size
            item.FONT_HEIGHT = int(size[1]*0.7)
            item.boxBg = pygame.transform.scale(boxBgImage,self.RECT_SIZE)
            item.boxFont = pygame.font.SysFont("futuraextra",item.FONT_HEIGHT)
            
        
    def run(self):
        clock = pygame.time.Clock()
        time.sleep(1)
        while 1:
            clock.tick(40)
            window.fill(blue)
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
                    if event.key == 51:# and self.mode == 0:
                        self.mode = 3
                    elif event.key == 48:# and self.mode == 3:
                        self.mode = 0
                    elif event.key == 49:
                        self.mode = 1
                        

            if self.mode == 0:
                if self.RECT_SIZE[0] ==425:
                    self.scroll = 1
                    self.changeRECT((900,70))
                bgRect = pygame.Rect(0,0,1920,1080)
                window.blit(self.backBg,bgRect)
                string = "Current Ranks"
                rect = self.boxFont.render(string,True,white)
                y =self.RECT_SIZE[1] + int(self.RECT_SIZE[1] * 1.1) * self.scroll
                if self.scroll == 1:
                    window.blit(rect,(960- rect.get_width()/2,y/4))
                for item in self.tny.finish():
                    item.target = [960,y]
                    y += int(self.RECT_SIZE[1] * 1.1)

            elif self.mode == 1:
                if self.RECT_SIZE[0] ==900:
                    self.changeRECT((425,35))
                for item in self.tny.finish():
                    if onScreen(item.target):
                        item.target = randomTarget()
                y = self.RECT_SIZE[1] + int(self.RECT_SIZE[1] * 1.1)
                xa = 50 + self.RECT_SIZE[0]/2
                xb = 1870 - self.RECT_SIZE[0]/2
                self.matches[0].a.target = [xa,y]
                self.matches[0].b.target = [xb,y]

            
                    
            elif self.mode == 3:
                bgRect = pygame.Rect(0,0,1920,1080)
                window.blit(self.backBg,bgRect)
                if self.RECT_SIZE[0] ==900:
                    self.changeRECT((425,35))
                
                string = "Upcoming Matches"
                rect = self.boxFont.render(string,True,white)

                y =self.RECT_SIZE[1] + int(self.RECT_SIZE[1] * 1.1)*2
                window.blit(rect,(960- rect.get_width()/2,y/4))
                for x in range(len(self.matches)):
                    xa = int(960 - 25 - self.RECT_SIZE[0]/2)
                    xb = int(960 + 25 +self.RECT_SIZE[0]/2)
                    self.matches[x].a.target = [xa,y]
                    self.matches[x].b.target = [xb,y]
                    y += int(self.RECT_SIZE[1] * 1.1)*2
            
                    

                
            
            for item in self.tny.finish():
                item.tick()
                item.render()

            pygame.display.update()
        
class game():
    def __init__(self,a,b):
        self.a = a
        self.b = b
        
class player():
    def __init__(self,name,a,b,c):
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

        self.RECT_SIZE = (900,70)#64
        self.FONT_HEIGHT = int(self.RECT_SIZE[1]*0.7)
        self.boxFont = pygame.font.SysFont("futuraextra",self.FONT_HEIGHT)
        self.boxBg = pygame.transform.scale(boxBgImage,self.RECT_SIZE)
        
    def render(self):
        #box
        x = self.pos[0] - self.RECT_SIZE[0]/2
        y = self.pos[1] - self.RECT_SIZE[1]/2
        #pygame.draw.rect(window,grey,(x,y,RECT_SIZE[0],RECT_SIZE[1]))
        RECT = pygame.Rect(x,y,self.RECT_SIZE[0],self.RECT_SIZE[1])
        window.blit(self.boxBg,RECT)
        #text
        string = "#" + str(self.rank) +" " + str(self.name)#+ str(self.points)
        string2 = str(self.points)
        textRECT = self.boxFont.render(string,True,white)
        textRECT2 = self.boxFont.render(string2,True,white)
        window.blit(textRECT,(x + self.FONT_HEIGHT/4, y + self.FONT_HEIGHT/4 ))
        window.blit(textRECT2,(self.RECT_SIZE[0] + x - self.FONT_HEIGHT/4 - textRECT2.get_width(), y + self.FONT_HEIGHT/4 ))
        
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

class match():
    def __init__(self):
        self.auto = False
        self.loud = False #spam the console with match info, don't use if running more than 1 tournament
        self.stages = 3 #number of stages in the tournament (qualifying, playoffs, finals)
        self.firstRounds = 3 #number of matches each bot will play in the first round
        self.normalRounds = 1 #number of matches each bot will play in the playoffs/finals
        self.firstcutoff = 0.45 #how many bots to cut after the first stage
        self.cutoff = 0.3 #how many bots to cut after additional stages
        self.start_seeded = False #seed the bots

        self.nameid = 1
        self.matches = 0
        self.un = 0
        self.hu = 0

        self.numPlayers = 0 #number of players
        self.activePlayers = []
        file = "1v1Bots.txt"
        self.loadPlayers(file)
        self.cutPlayers = []
        
    def loadPlayers(self,file):
        try:
            f= open(file,"rb")
            for line in f:
                if len(line) > 1:
                    self.activePlayers.append(player(line.decode("UTF-8"),0,0,0))
                    self.numPlayers += 1
        except:
            print("couldn't load players")

    
    def matchRound(self):
        matches = []
        uncaught = []
        for a in self.activePlayers:
            if a.taken == False:
                flag = True
                for b in self.activePlayers:
                    if b.taken == False and b != a and b not in a.opponents:
                        a.taken = True
                        b.taken = True
                        matches.append(game(a,b))
                        flag = False
                        a.opponents.append(b)
                        b.opponents.append(a)
                        break
                if flag:
                    uncaught.append(a) #if every bot has seen every other bot, there are uncaught match pairings
        uncaught.sort(key=lambda bot: bot.points,reverse = True)
        for a in uncaught: #uncaught pairings are dealt with as fairly as possible
            if a.taken == False:
                flag = True
                for b in uncaught:
                    if b.taken == False and b != a:
                        a.taken = True
                        b.taken = True
                        matches.append(game(a,b))
                        flag = False
                        break
        for bot in self.activePlayers: #flag in all bots is reset
            bot.taken = False
        return matches
        
        
    
    def runTournament(self, sample = 1):
        print("Running %s Tournament(s)" % (str(sample)))
        print("Stages: %s\nNumber of firstRounds: %s\nNumber of normalRounds: %s\nCutoff Percent(for normal rounds): %s\nSeeded: %s\nNumber of Players: %s\n" % (str(self.stages),str(self.firstRounds),str(self.normalRounds),str(self.cutoff),str(self.start_seeded),str(self.numPlayers),))
        totalUnfair = 0

        for x in range(sample):
            self.activePlayers = []
            self.cutPlayers = []
            self.nameid = 1
            self.makePlayers()
            if self.loud:
                print("Current Unfairness: %s" % (str(self.rateFairness())))
                print("\n\nCompetitors:")
                for item in self.activePlayers:
                    print(item.ts())
                print("\nRunning FirstRounds")
            for y in range(self.firstRounds):
                if self.loud:
                    print("Current Unfairness: %s" % (str(self.rateFairness())))
                    print("\nRunning Round %s"%(str(y)))
                self.playRound(False)
                self.sortPlayers(False)
                if self.loud:
                    for item in self.activePlayers:
                        print(item.ts())
            self.cut(0)
            for z in range(self.stages-1):
                if self.loud:
                    print("\nRunning Stage %s"%(str(z)))
                for y in range(self.normalRounds):
                    if self.loud:
                        print("Current Unfairness: %s" % (str(self.rateFairness())))
                        print("\nRunning Round %s"%(str(y)))
                    self.playRound(False)
                    self.sortPlayers(False)
                    if self.loud:
                        for item in self.activePlayers:
                            print(item.ts())
                self.cut(1)
            totalUnfair += self.finish()
        print("Matches Per Tournament: %s\n" % str(self.matches/sample))
            
        print("Total Matches: %s" % str(self.matches))
        print("Average Unfairness: " + str(totalUnfair/sample))
        print("Uncaught match pairing issues: " +str(self.un))
        print("Repeat matches: " +str(self.hu))
        print("% of unwanted matches: " +str((self.hu/self.matches)*100)[:5])
            
    
    def abc(self,total): #generates skill level of A,B,C for a given bot, where the sum of A,B,C = total
        a = random.randint(0,total-1)
        b = random.randint(0,total-a-1)
        c = total - a - b
        return a,b,c

    def whoWins(self,a,b):
        #This compares the stats of 2 players to see who would win
        #The stats are kinda like tic-tac-toe, each one beats one other
        #a = a
        #a = b/1.5
        #a = c*1.5
        als = [a.a,a.b,a.c]
        bls = [b.a,b.b,b.c]
        ap = 0
        bp = 0     
        for i in range(3):
            if als[i] > bls[i]:
                ap += 1
            elif als[i] < bls[i]:
                bp += 1
            if als[i] > bls[(i+1)%3] /1.5:
                ap += 1
            elif als[i] < bls[(i+1)%3] /1.5:
                bp += 1
            if als[i] > bls[(i+2)%3] *1.5:
                ap += 1
            elif als[i] < bls[(i+2)%3] *1.5:
                bp += 1
        if ap >= bp+1:
            return 2
        elif abs(ap - bp)<=1 and ap > bp:
            return 1
        elif abs(ap-bp) <=1 and bp > ap:
            return 0
        else:
            return -1

    def makePlayers(self): #generates the players, each one having less total skill than the previous
        scale = int(100/self.numPlayers)
        total = 100
        for i in range(self.numPlayers):
            a,b,c = self.abc(total)
            self.activePlayers.append(player(str(self.nameid),a,b,c))
            self.nameid += 1
            total -= scale
        if self.start_seeded == False:
            random.shuffle(self.activePlayers)

    def playRound(self, simple = True): #plays a round, ignore the 'simple' version it's stupid
        if simple ==True:
            i=0
            while i < len(self.activePlayers) -1:
                if self.whoWins(self.activePlayers[i],self.activePlayers[i+1]) == 2:
                    self.activePlayers[i].points += 2
                elif self.whoWins(self.activePlayers[i],self.activePlayers[i+1]) == 1:
                    self.activePlayers[i].points += 2
                    self.activePlayers[i+1].points += 1
                elif self.whoWins(self.activePlayers[i],self.activePlayers[i+1]) == 0:
                    self.activePlayers[i].points += 1
                    self.activePlayers[i+1].points += 2
                else:
                    self.activePlayers[i+1].points += 2
                i+=2
                self.matches+=1
        else:
            #plays bots against eachother, ensuring similar point levels are matched and bots play against new opponents
            uncaught = []
            for a in self.activePlayers:
                if a.taken == False:
                    flag = True
                    for b in self.activePlayers:
                        if b.taken == False and b != a and b not in a.opponents:
                            self.matches+=1
                            a.taken = True
                            b.taken = True
                            flag = False
                            a.opponents.append(b)
                            b.opponents.append(a)
                            if self.whoWins(a,b) == 2:
                                a.points += 2
                            elif self.whoWins(a,b) == 1: #uses the close game system
                                a.points += 2
                                b.points += 1
                            elif self.whoWins(a,b) == 0:
                                a.points += 1
                                b.points += 2
                            else:
                                b.points += 2
                            break
                    if flag:
                        self.un += 1
                        uncaught.append(a) #if every bot has seen every other bot, there are uncaught match pairings
                        if self.loud:
                            print("Could not find match!!!!!")
            uncaught.sort(key=lambda bot: bot.points,reverse = True)
            for a in uncaught: #uncaught pairings are dealt with as fairly as possible
                if a.taken == False:
                    flag = True
                    for b in uncaught:
                        if b.taken == False and b != a:
                            self.matches+=1
                            a.taken = True
                            b.taken = True
                            flag = False
                            if self.whoWins(a,b) == 2:
                                a.points += 2
                            elif self.whoWins(a,b) == 1:
                                a.points += 2
                                b.points += 1
                            elif self.whoWins(a,b) == 0:
                                a.points += 1
                                b.points += 2
                            else:
                                b.points += 2
                            break
                    if flag:
                        self.un += 1
                        if self.loud:
                            print("Could not find match!!!!!")
                    else:
                        self.un -= 2
                        self.hu +=1
            for bot in self.activePlayers: #flag in all bots is reset
                bot.taken = False

    def sortPlayers(self,debug = True): #sorts bots by their points
        self.activePlayers.sort(key=lambda bot: bot.points,reverse = True)
        if debug and self.loud:
            for item in self.activePlayers:
                print(item.ts())

    def cut(self,t): #cuts from active bots by percentage
        if t == 0:
            temp = self.firstcutoff
        else:
            temp = self.cutoff
        toCut = int(len(self.activePlayers) * temp)
        if toCut % 2 > 0:
            toCut += 1
        for i in range(toCut):
            self.cutPlayers.append(self.activePlayers.pop())
            
    def rateFairness(self): #determines how far away bots are from where they should be by comparing their final standing with their total skill points
        final = []
        for item in self.activePlayers:
            final.append(item)
        for item in self.cutPlayers:
            final.append(item)
        final.sort(key=lambda bot: bot.points,reverse = True)
        totalError = 0
        maxError = (self.numPlayers * (self.numPlayers + 1))/2
        for i in range(0,len(final)):
            #print(str(self.activePlayers[i].name)+" "+ str(abs((i+1) - int(self.activePlayers[i].name))))
            totalError += (abs((i+1) - int(final[i].name))) * ((self.numPlayers-int(final[i].name))*2/self.numPlayers)
        return int((totalError/maxError)*100)

    def finish(self): #combines active and cut players and sorts by points
        counter = 1
        final = []
        for item in self.activePlayers:
            final.append(item)
        for item in self.cutPlayers:
            final.append(item)
        final.sort(key=lambda bot: bot.points,reverse = True)
        if self.loud:
            print("\n\nFinal Results:")
            for item in final:
                print(item.ts())
            print("Unfairness: %s" % (str(self.rateFairness())))
            print("Matches Played: %s"%(self.matches))
        for item in final:
            item.rank = counter
            counter += 1
        return final
            
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
