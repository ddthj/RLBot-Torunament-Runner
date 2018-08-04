
class Old_Player():
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
