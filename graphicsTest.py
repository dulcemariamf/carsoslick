from graphics import *

WIDTH, HEIGHT = 1200.0, 700.0

#grab speed & accel from outside file

speed = 2.0
acceleration = 0.005

points = 0
p2Win = 100000

lines = []

def main():
    roadBuff = 50.0
    global speed
    win = GraphWin('Speedy Wheely Automobiley', WIDTH, HEIGHT)
    win.setBackground('burlywood')

    drawRoad(win, roadBuff)
    for i in range(7):
        line = Line(Point(i*(WIDTH/7), 0), Point(i*(WIDTH/7), HEIGHT))
        line.draw(win)

    done = False
    lines = drawLines(2, win, roadBuff)
    global points
    while not done:
        for i in lines:
            rmove(i, -speed, 0)
        done = win.checkMouse()
        #speed += acceleration
        points += 1
        if points >= p2Win:
            done = True
            print("you win!")
        print(points)

    win.close()

def rmove(rect, xm, ym):
    rWidth = rect.getP2().getX() - rect.getP1().getX()
    rCenter = rect.getP1().getX() + rWidth
    if(rect.getP2().getX() <= -rWidth):
        rect.move(WIDTH+(rWidth*2), ym)
    else:
        rect.move(xm, ym)

def make_rect(center,size):
    return (Point(center[0]-(size[0]/2), center[1]-(size[1]/2)),Point(center[0]+(size[0]/2), center[1]+(size[1]/2)))

def drawRoad(win, roadBuff):
    upEdge = roadBuff
    downEdge = HEIGHT - roadBuff
    
    road = Rectangle(Point(WIDTH,downEdge), Point(-1,upEdge))
    road.setOutline("black")
    road.setFill("grey")
    road.draw(win)
    sepHeight = HEIGHT/10

def drawLines(numLines, win, buff):
    line = []
    numTix = int((WIDTH / 2)/buff)
    
    roadWidBuff = HEIGHT/(numLines+1)

    for k in range(numLines):
        for i in range(numTix+1):
            yr = make_rect((i*(buff*2)+(buff), (k+1)*roadWidBuff),(buff, buff/(2*numLines)))
            yrect = Rectangle(yr[0], yr[1])
            yrect.setOutline("black")
            yrect.setFill("yellow")
            line.append(yrect)

    for i in line:
        i.draw(win)
    return line

main()
