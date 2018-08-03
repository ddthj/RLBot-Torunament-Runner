import string
import random
"""
Matchmaker Test v1 by GooseFairy/ddthj

This program generates a modified Swiss tournament that includes elimination to help minimize the number of matches and minimize unfairness
"""

class player():
    def __init__(self,name,a,b,c):
        self.name = name
        self.a = a #how good a bot is at doing A
        self.b = b #how good B
        self.c = c #how good C
        self.points = 0 #points it has won
        self.opponents = [] #opponents it has faced
        self.taken = False #if it has played a match in the current round
        
    def ts(self): #to string
        dif = int((abs(self.a - self.b) + abs(self.a - self.c) + abs(self.c - self.b))/3)
        
        total = str(self.name)
        total += (" a: %s b: %s c: %s Total: %s Bad: %s Points: %s" % (str(self.a),str(self.b),str(self.c),str(self.a + self.b + self.c), str(dif),str(self.points)))
        return total

class match():
    def __init__(self):
        self.loud = True #spam the console with match info, don't use if running more than 1 tournament
        self.stages = 3 #number of stages in the tournament (qualifying, playoffs, finals)
        self.firstRounds = 2 #number of matches each bot will play in the first round
        self.normalRounds = 1 #number of matches each bot will play in the playoffs/finals
        self.firstcutoff = 0.5 #how many bots to cut after the first stage
        self.cutoff = 0.5 #how many bots to cut after additional stages
        self.start_seeded = False #seed the bots

        self.nameid = 1
        self.matches = 0
        self.un = 0
        self.hu = 0

        self.numPlayers = 22 #number of players

        self.activePlayers = []
        self.cutPlayers = []

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
        return self.rateFairness()
            


z = match()
z.runTournament(1)
