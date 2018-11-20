#import libraries
import sys
from pynput import keyboard
from pynput.keyboard import Key, Listener
from graphics import *
from PIL import Image as img

#set global variables
WIDTH, HEIGHT = 1200.0, 700.0       #window size (leave alone)
speed = 2.0                         #"car speed" (line speed)
acceleration = 0.01                 #"car acceleration" (line accel.)
win = GraphWin('Speedy Wheely Automobiley', WIDTH, HEIGHT)  #graphics window
points = 0              #points
p2Win = 100000          #points to win
done = False            #done flag
qp = False              #"q pressed" flag for grid toggle
drawn = False           #drawn flag for grid toggle
grid = []               #grid array (holds type line from graphics)
MDP = []                #array for MDP
listener = None         #keyboard listener, to be created in main()
playCar = None          #player car object
carX = 0                #car X-coordinate
carY = 0                #car Y-coordinate
xcoords = []            #board x-coordinates
ycoords = []            #board y-coordinates
move = False            #player movement flag

def main():
    #grab global variables
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
    global MDP
    global playCar
    global carX
    global carY
    global xcoords
    global ycoords
    global move

    #set background (dirt road)
    win.setBackground('burlywood')

    #draw grey road
    drawRoad(win, roadBuff)
    #create lines for grid, but don't draw them yet
    for i in range(6):
        line = Line(Point((i+1)*(WIDTH/7), 0), Point((i+1)*(WIDTH/7), HEIGHT))
        grid.append(line)
    #draw road lines, first parameter is how many to draw. 3 means 4 rows, and that scales in the same manner
    numLanes = 5
    rLinesNumber = numLanes-1
    rlines = drawLines(rLinesNumber, win, roadBuff)
    
    #create a 2D array that acts as our MDP with rLinesNumber+1 rows 
    columns = 7
    MDP = [['e' for x in range(columns)] for y in range (numLanes)] 
    #print (MDP)

    #calculate lane width
    laneWidth = rlines[0].getCenter().getY() - roadBuff

    #create Arrays to hold coordinates for car locations
    xcoords = []
    for i in range(7):
        x = int(((i*2)+1)*(WIDTH/14))
        xcoords.append(x-(x%5))
    xmov = (xcoords[1] - xcoords[0])/10
    ycoords = []
    for i in range(numLanes):
        y = int((roadBuff+(laneWidth/2))+(i*laneWidth))
        ycoords.append(y-(y%5))
    ymov = (ycoords[1] - ycoords[0])/10
    
    #resize player car to fit in lane
    image = img.open("car.png")
    newHeight = int(laneWidth*0.7)
    hpercent = (newHeight / float(image.size[1]))
    wsize = int((float(image.size[0])*float(hpercent)))
    image = image.resize((wsize, newHeight), img.ANTIALIAS)
    image.save('car.png')
    
    #draw car in the center of the screen
    carX = 3
    carY = int(numLanes/2)
    MDP[carY][carX] = 'p'
    playCar = Image(Point(xcoords[carX], ycoords[carY]), "car.png")
    playCar.draw(win)
    printMDP()

    #loop until done
    while not done:
        #if q was pressed, toggle the grid drawing
        if qp:
            if not drawn:
                for g in grid:
                    g.draw(win)
            else:
                for g in grid:
                    g.undraw()
            qp = False
            drawn = not drawn
        if move:
            x = playCar.getAnchor().getX()
            y = playCar.getAnchor().getY()
            if x < xcoords[carX]:
                xmov = (xcoords[carX]-xcoords[carX-1])/5
                playCar.move(xmov,0)
            if x > xcoords[carX]:
                xmov = (xcoords[carX+1]-xcoords[carX])/5
                playCar.move(-xmov,0)
            if y < ycoords[carY]:
                ymov = (ycoords[carY]-ycoords[carY-1])/5
                playCar.move(0,ymov)
            if y > ycoords[carY]:
                ymov = (ycoords[carY+1]-ycoords[carY])/5
                playCar.move(0,-ymov)
            if x == xcoords[carX] and y == ycoords[carY]:
                move = False
        #move the road lines
        for i in rlines:
            rmove(i, -speed, 0)
        #increase speed by acceleration
        speed += acceleration
        #increase points, plan to scale with speed later
        points += 1
        #if you get enough points, you win
        if points >= p2Win:
            done = True
            print("you win!")
        #print(points)
    end_game()

#stop game method
def end_game():
    global listener, win
    listener.stop()
    win.close()
    sys.exit()

def printMDP():
    global MDP
    for row in MDP:
        print(row)
    print()

def moveCar(drxn):
    global playCar, carX, carY, MDP, move
    MDP[carY][carX] = 'e'
    if drxn == "down" and carY < (len(MDP)-1):
        carY += 1
        move = True
    elif drxn == "up" and carY > 0:
        carY -= 1
        move = True
    elif drxn == "left" and carX > 0:
        carX -= 1
        move = True
    elif drxn == "right" and carX < (len(MDP[0])-1):
        carX += 1
        move = True
    MDP[carY][carX] = 'p'
    printMDP()

#keyboard listener method
def on_press(key):
    global done, drawn, qp, MDP
    if key == Key.esc:  #press esc to quit
        done = True
    elif key.char == 'q': #press q to toggle the grid
        qp = True
    elif key.char == 's':
        moveCar("down")
    elif key.char == 'w':
        moveCar("up")
    elif key.char == 'a':
        moveCar("left")
    elif key.char == 'd':
        moveCar("right")

#road line movement method
#Parameters: Rectangle graphics object, int, int
def rmove(rect, xm, ym):
    if(rect.getP2().getX() <= -50):
        rect.move(WIDTH+100, ym)
    else:
        rect.move(xm, ym)

#create rectangle method
#Parameters: tuple (x,y), tuple (width,height)
def make_rect(center,size):
    return (Point(center[0]-(size[0]/2), center[1]-(size[1]/2)),Point(center[0]+(size[0]/2), center[1]+(size[1]/2)))

#draw road method
#Parameters: graphics window, int
def drawRoad(win, roadBuff):
    upEdge = roadBuff
    downEdge = HEIGHT - roadBuff
    
    road = Rectangle(Point(WIDTH,downEdge), Point(-1,upEdge))
    road.setOutline("black")
    road.setFill("grey")
    road.draw(win)
    sepHeight = HEIGHT/10

#draw road lines method
#Parameters: int, graphics window, int
def drawLines(numLines, win, buff):
    line = []
    numTix = int((WIDTH/2)/50.0)
    
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
