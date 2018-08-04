import random

white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
grey = (150,150,150)

RANKS = 0
UPCOMING_MATCHES = 1
DURING_MATCH = 2


def randomTarget(): #makes target offscreen
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


class Globals:
    def __init__(self, window, boxBgImage):
        self.boxBgImage = boxBgImage
        self.window = window
