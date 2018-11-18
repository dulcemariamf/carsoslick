from pynput import keyboard
from pynput.keyboard import Key, Listener
from graphics import *

WIDTH, HEIGHT = 1200.0, 700.0

#grab speed & accel from outside file

speed = 2.0
acceleration = 0.01
win = GraphWin('Speedy Wheely Automobiley', WIDTH, HEIGHT)
points = 0
p2Win = 100000
done = False
qp = False
drawn = False

grid = []
listener = None

def main():
    global listener
    listener = Listener(
            on_press=on_press)
    listener.start()
    roadBuff = 75.0
    global speed
    global lines
    global done
    global points
    global win
    global qp
    global drawn
    win.setBackground('burlywood')

    drawRoad(win, roadBuff)
    for i in range(6):
        line = Line(Point((i+1)*(WIDTH/7), 0), Point((i+1)*(WIDTH/7), HEIGHT))
        grid.append(line)
        #line.draw(win)
    lines = drawLines(4, win, roadBuff)
    
    while not done:
        if qp:
            if not drawn:
                for g in grid:
                    g.draw(win)
            else:
                for g in grid:
                    g.undraw()
            qp = False
            drawn = not drawn
        for i in lines:
            rmove(i, -speed, 0)
        speed += acceleration
        points += 1
        if points >= p2Win:
            done = True
            print("you win!")
        #print(points)

    end_game()

def end_game():
    global listener
    global win
    listener.stop()
    win.close()

def on_press(key):
    global done
    global drawn
    global qp
    if key == Key.esc:
        done = True
    if key.char == 'q': #press q to quit the game
        qp = True
    #print(type(key))

def rmove(rect, xm, ym):
    if(rect.getP2().getX() <= -50):
        rect.move(WIDTH+100, ym)
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
    #numTix = int((WIDTH / 2)/buff)
    numTix = int((WIDTH/2)/50.0)
    
    #roadWidBuff = (HEIGHT-(buff*2))/(numLines+1)
    roadWidBuff = (HEIGHT-(buff*2))/(numLines+1)

    for k in range(numLines):
        for i in range(numTix+1):
            #yr = make_rect((i*(buff*2)+(buff), buff+(k+1)*roadWidBuff),(buff, buff/(2*numLines)))
            yr = make_rect((i*(100.0)+(50.0), buff+(k+1)*roadWidBuff),(50.0, 50.0/(2*numLines)))
            yrect = Rectangle(yr[0], yr[1])
            yrect.setOutline("black")
            yrect.setFill("yellow")
            line.append(yrect)

    for i in line:
        i.draw(win)
    return line

main()
