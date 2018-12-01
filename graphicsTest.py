#import libraries
import sys
import random
from pynput import keyboard
from pynput.keyboard import Key, Listener
from graphics import *
from PIL import Image as img
import MDPReader as mdpr
import ValueIterationAgent as VIA

#global controller variables
numLanes = 5    #reccomended max: 7
numCars = 1     #max 2, min 1
numOil = 2      #max 2, min 1

myChoice = None
badCarCoords = []
numIter = 0
while(myChoice == None):
  print("Choose:")
  print("1. Value Iteration")
  print("2. Approximate Q-Learning")
  print("3. Policy Iteration")
  print("4. Q-Learning")
  myChoice = input()
  myChoice = int(myChoice)
  if not myChoice in [1,2,3,4]:
      myChoice = None
if myChoice == 1:
    numOil = 2
    badCarCoords = [(1,0),(1,1),(1,3),(3,3),(3,4),(5,0),(5,1),(5,2)]
    while numIter < 1:
        print("How many iterations?")
        numIter = int(input())
#set global variables
WIDTH, HEIGHT = 1200.0, 700.0       #window size (leave alone)
speed = 2.0                         #"car speed" (line speed)
acceleration = 0.01                 #"car acceleration" (line accel.)
win = GraphWin('Speedy Wheely Automobiley', WIDTH, HEIGHT)  #graphics window
points = 0              #points
p2Win = 3000            #points to win
done = False            #done flag
qp = False              #"q pressed" flag for grid toggle
drawn = False           #drawn flag for grid toggle
grid = []               #grid array (holds type line from graphics)
gridcoords = []         #array for grid line x-coordinates
MDP = []                #array for MDP
MDPchanged = False      #flag to tell if the MDP has changed
listener = None         #keyboard listener, to be created in main()
playCar = None          #player car object
carX = 0                #car X-coordinate
carY = 0                #car Y-coordinate
xcoords = []            #board x-coordinates
ycoords = []            #board y-coordinates
move = False            #player movement flag
oil, oilX, oilY = None, 0, 0
oil2, oil2X, oil2Y = None, 0, 0
badCar, bcarX, bcarY, bcarSp = None, 0, 0, 0
badCar2, bcar2X, bcar2Y, bcar2Sp = None, 0, 0, 0

def main():
    #grab global variables
    global myChoice
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
    global grid, gridcoords
    global MDP, MDPchanged
    global playCar, carX, carY
    global xcoords
    global ycoords
    global move
    global oil, oilX, oilY
    global badCar, bcarX, bcarY, bcarSp
    global numLanes
    global numCars, numOil
    if numCars > 1:
        global badCar2, bcar2X, bcar2Y, bcar2Sp
    if numOil > 1 or myChoice == 1:
        global oil2, oil2X, oil2Y

    mdpReader = mdpr.MDPReader()
    if myChoice == 1:
        startCalc = True
        global numIter

    #set background (dirt road)
    win.setBackground('burlywood')

    #draw grey road
    drawRoad(win, roadBuff)
    #create lines for grid, but don't draw them yet
    for i in range(8):
        line = Line(Point(int((i)*(WIDTH/7)), 0), Point((i)*(WIDTH/7), HEIGHT))
        grid.append(line)
        gridcoords.append(int((i)*(WIDTH/7)))
    print(gridcoords)
    #draw road lines, first parameter is how many to draw. 3 means 4 rows, and that scales in the same manner
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

    #draw point counter or end goal
    if myChoice != 1:
        pCounter = Text(Point(WIDTH/2, roadBuff/2), "Points: ")
        pCounter.setSize(24)
        pCounter.setStyle("bold")
        pCounter.draw(win)
    else:   #draw win space
        yr = make_rect((xcoords[6],ycoords[numLanes-1]),(xcoords[6]-xcoords[5], laneWidth))
        yrect = Rectangle(yr[0], yr[1])
        yrect.setOutline("black")
        yrect.setFill("green")
        yrect.draw(win)
        MDP[numLanes-1][6] = 'w'
    
    #resize player car to fit in lane
    image = img.open("car.png")
    newHeight = int(laneWidth*0.7)
    hpercent = (newHeight / float(image.size[1]))
    wsize = int((float(image.size[0])*float(hpercent)))
    image = image.resize((wsize, newHeight), img.ANTIALIAS)
    image.save('car.png')
    
    #draw car in the middle lane
    if myChoice != 1:
        carX = 3
        carY = int(numLanes/2)
    else:
        carX = 0
        carY = 0
    MDP[carY][carX] = 'p'
    playCar = Image(Point(xcoords[carX], ycoords[carY]), "car.png")
    playCar.draw(win)

    #resize oil slick to fit in line
    image = img.open("oilSlick.png")
    newHeight = int(laneWidth*0.7)
    hpercent = (newHeight / float(image.size[1]))
    wsize = int((float(image.size[0])*float(hpercent)))
    image = image.resize((wsize, newHeight), img.ANTIALIAS)
    image.save('oilSlick.png')

    #draw oil in the middle lane
    if myChoice != 1:
        oilX = 6
        oilY = int(numLanes/2)
    #else:
    #    oilX = 5
    #    oilY = int(numLanes/2)+1
        MDP[oilY][oilX] = 'o'
        oil = Image(Point(xcoords[oilX], ycoords[oilY]), "oilSlick.png")
        oil.draw(win)
        if numOil > 1:
            oil2X = 3
            oil2Y = 1
            MDP[oil2Y][oil2X] = 'o'
            oil2 = Image(Point(xcoords[oil2X], ycoords[oil2Y]), "oilSlick.png")
            oil2.draw(win)

    #resize enemy car to fit in lane
    image = img.open("badCar.png")
    newHeight = int(laneWidth*0.7)
    hpercent = (newHeight / float(image.size[1]))
    wsize = int((float(image.size[0])*float(hpercent)))
    image = image.resize((wsize, newHeight), img.ANTIALIAS)
    image.save('badCar.png')

    #draw enemy car in the middle lane
    bcarSp = 5
    if myChoice != 1:
        bcarX = 0
    else:
        bcarX = 3
    if myChoice != 1:
        bcarY = int(numLanes/2)+1
        MDP[bcarY][bcarX] = 'b'
        badCar = Image(Point(xcoords[bcarX], ycoords[bcarY]), "badCar.png")
        badCar.draw(win)
        if numCars > 1:
            bcar2Sp = bcarSp+2
            bcar2X = 0
            bcar2Y = numLanes-1
            MDP[bcar2Y][bcar2X] = 'b'
            badCar2 = Image(Point(xcoords[bcar2X], ycoords[bcar2Y]), "badCar.png")
            badCar2.draw(win)
    else:
        xdistance = xcoords[1] - xcoords[0]
        badCars = []
        #badCars.append(badCar)
        for bc in badCarCoords:
            badCar = Image(Point(xcoords[bc[0]], ycoords[bc[1]]), "badCar.png")
            badCar.draw(win)
            badCars.append(badCar)
            MDP[bc[1]][bc[0]] = 'b'

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
        if startCalc:
            #do calculations
            vIteration = VIA.ValueIterationAgent(MDP, numIter)
            vIteration.dothing()
            #mdpReader.getTransitionStatesAndProbs(MDP, mdpReader.getAgentCoordinates(MDP),"left")
            startCalc = False
        if move:
            x = playCar.getAnchor().getX()
            y = playCar.getAnchor().getY()
            div = 5
            if x < xcoords[carX]:
                if myChoice != 1: xmov = (xcoords[carX]-xcoords[carX-1])/div
                else: xmov = 1
                playCar.move(xmov,0)
            if x > xcoords[carX]:
                if myChoice != 1: xmov = (xcoords[carX+1]-xcoords[carX])/div
                else: xmov = 1
                playCar.move(-xmov,0)
            if y < ycoords[carY]:
                if myChoice != 1: ymov = (ycoords[carY]-ycoords[carY-1])/div
                else: ymov = 1
                playCar.move(0,ymov)
            if y > ycoords[carY]:
                if myChoice != 1: ymov = (ycoords[carY+1]-ycoords[carY])/div
                else: ymov = 1
                playCar.move(0,-ymov)
            if x == xcoords[carX] and y == ycoords[carY]:
                move = False
        #calculate obstacle edges
        if myChoice != 1:
            moveObst(speed)
            if bcarY == carY:
                badCarR = badCar.getAnchor().getX()+(badCar.getWidth()/2)
                badCarL = badCar.getAnchor().getX()-(badCar.getWidth()/2)
                cx = playCar.getAnchor().getX()
                cxr = cx + (playCar.getWidth()/2)
                cxl = cx - (playCar.getWidth()/2)
                collision = (cxr >= badCarL) and (cxl <= badCarR)
                if collision:
                    print("you lose")
                    end_game()
            if numCars > 1 and bcar2Y == carY:
                badCarR = badCar2.getAnchor().getX()+(badCar2.getWidth()/2)
                badCarL = badCar2.getAnchor().getX()-(badCar2.getWidth()/2)
                cx = playCar.getAnchor().getX()
                cxr = cx + (playCar.getWidth()/2)
                cxl = cx - (playCar.getWidth()/2)
                collision = (cxr >= badCarL) and (cxl <= badCarR)
                if collision:
                    print("you lose")
                    end_game()
        else:
            if (carX, carY) in badCarCoords:
                points -= p2Win
                print("You lose")
                end_game()
        if myChoice != 1:
            if oilY == carY:
                oilR = oil.getAnchor().getX()+(oil.getWidth()/2)
                oilL = oil.getAnchor().getX()-(oil.getWidth()/2)
                cx = playCar.getAnchor().getX()
                cxr = cx + (playCar.getWidth()/2)
                cxl = cx - (playCar.getWidth()/2)
                collision = (cxr >= oilL) and (cxl <= oilR)
                if collision:
                    coin = random.randint(1, 2)
                    if coin == 1:
                        moveCar("down")
                    else:
                        moveCar("up")
        """elif oilX == carX and oilY == carY:
            x = playCar.getAnchor().getX()
            y = playCar.getAnchor().getY()
            if x < xcoords[carX]:
                moveCar("right")
            if x > xcoords[carX]:
                moveCar("left")
            if y < ycoords[carY]:
                moveCar("down")
            if y > ycoords[carY]:
                moveCar("up")"""
        if myChoice != 1:
            if numOil > 1 and oil2Y == carY:
                oilR = oil2.getAnchor().getX()+(oil2.getWidth()/2)
                oilL = oil2.getAnchor().getX()-(oil2.getWidth()/2)
                cx = playCar.getAnchor().getX()
                cxr = cx + (playCar.getWidth()/2)
                cxl = cx - (playCar.getWidth()/2)
                collision = (cxr >= oilL) and (cxl <= oilR)
                if collision:
                    coin = random.randint(1, 2)
                    if coin == 1:
                        moveCar("down")
                    else:
                        moveCar("up")
        """elif numOil > 1 and oil2X == carX and oil2Y == carY:
            x = playCar.getAnchor().getX()
            y = playCar.getAnchor().getY()
            if x < xcoords[carX]:
                moveCar("right")
            if x > xcoords[carX]:
                moveCar("left")
            if y < ycoords[carY]:
                moveCar("down")
            if y > ycoords[carY]:
                moveCar("up")"""
        #move the road lines
        if myChoice != 1:
          for i in rlines:
              rmove(i, -speed, 0)
        #increase speed by acceleration
        speed += acceleration

        #increase points, plan to scale with speed later
        if myChoice != 1:
            points += 1
            pCounter.setText("Points: " + str(points))
        else: #xcoords[6],ycoords[numLanes-1]
            if carX == 6 and carY == numLanes-1:
                cx = playCar.getAnchor().getX()
                cy = playCar.getAnchor().getY()
                if cx == xcoords[6] and cy == ycoords[numLanes-1]:
                    points = p2Win
        #if you get enough points, you win
        if points >= p2Win:
            done = True
            print("you win!")
        #print(points)
            
        if MDPchanged:
            #this is where you will call your algorithm to decide
            #what move to make, by calling moveCar("up"), moveCar("down"),
            #moveCar("left"), or moveCar("right")
            #print()
            #print(mdpReader.getAgentCoordinates(MDP))
            #print()
            #print(mdpReader.getTransitionStatesAndProbs(MDP,mdpReader.getAgentCoordinates(MDP),"down"))

            #printMDP()
            MDPchanged = False
    end_game()

#stop game method
def end_game():
    global listener, win, points
    print("points:" + str(points))
    listener.stop()
    win.close()
    sys.exit()

def printMDP():
    global MDP
    for row in MDP:
        print(row)
    print()

def moveObst(speed):
    global WIDTH, xcoords, ycoords
    global numCars, numOil
    global badCar, bcarX, bcarY, bcarSp
    global badCar2, bcar2X, bcar2Y, bcar2Sp
    global oil, oilX, oilY
    global oil2, oil2X, oil2Y
    global gridcoords
    global MDP, MDPchanged
    
    oilR = oil.getAnchor().getX()+(oil.getWidth()/2)
    if oilR <= 0:
        MDP[oilY][oilX] = 'e'
        oilY = random.randint(0,numLanes-1)
        ydiff = ycoords[oilY]-oil.getAnchor().getY()
        oil.move(WIDTH+oil.getWidth(), ydiff)
        oilX = 6
        MDP[oilY][oilX] = 'o'
        MDPchanged = True
        #printMDP()
    else:
        oil.move(-speed, 0)
        if oilX != 0 and oil.getAnchor().getX() < gridcoords[oilX]:
            MDP[oilY][oilX] = 'e'
            oilX -= 1
            MDP[oilY][oilX] = 'o'
            MDPchanged = True
            #printMDP()

    if numOil > 1:
        oilR = oil2.getAnchor().getX()+(oil2.getWidth()/2)
        if oilR <= 0:
            MDP[oil2Y][oil2X] = 'e'
            oil2Y = random.randint(0,numLanes-1)
            ydiff = ycoords[oil2Y]-oil2.getAnchor().getY()
            oil2.move(WIDTH+oil2.getWidth(), ydiff)
            oil2X = 6
            MDP[oil2Y][oil2X] = 'o'
            MDPChanged = True
            #printMDP()
        else:
            oil2.move(-speed, 0)
            if oil2X != 0 and oil2.getAnchor().getX() < gridcoords[oil2X]:
                MDP[oil2Y][oil2X] = 'e'
                oil2X -= 1
                MDP[oil2Y][oil2X] = 'o'
                MDPchanged = True
                #printMDP()
            
    badCarL = badCar.getAnchor().getX()-(badCar.getWidth()/2)
    if badCarL >= WIDTH:
        MDP[bcarY][bcarX] = 'e'
        bcarY = random.randint(0,numLanes-1)
        ydiff = ycoords[bcarY]-badCar.getAnchor().getY()
        badCar.move(-WIDTH-badCar.getWidth(), ydiff)
        bcarX = 0
        MDP[bcarY][bcarX] = 'b'
        bcarSp += 1
        MDPchanged = True
        #printMDP()
    else:
        badCar.move(bcarSp, 0)
        if bcarX != 6 and badCar.getAnchor().getX() > gridcoords[bcarX]:
            MDP[bcarY][bcarX] = 'e'
            bcarX += 1
            MDP[bcarY][bcarX] = 'b'
            MDPchanged = True
            #printMDP()

    if numCars > 1:
        badCarL = badCar2.getAnchor().getX()-(badCar2.getWidth()/2)
        if badCarL >= WIDTH:
            MDP[bcar2Y][bcar2X] = 'e'
            bcar2Y = random.randint(0,numLanes-1)
            if bcar2Y == bcarY and bcarY != 0:
                if bcarY != 0:
                    bcar2Y = bcarY-1
                else:
                    bcar2Y = bcarY+1
            ydiff = ycoords[bcar2Y]-badCar2.getAnchor().getY()
            badCar2.move(-WIDTH-badCar2.getWidth(), ydiff)
            bcar2X = 0
            MDP[bcar2Y][bcar2X] = 'b'
            bcar2Sp += 1
            MDPchanged = True
            #printMDP()
        else:
            badCar2.move(bcar2Sp, 0)
            if bcar2X != 6 and badCar2.getAnchor().getX() > gridcoords[bcar2X]:
                MDP[bcar2Y][bcar2X] = 'e'
                bcar2X += 1
                MDP[bcar2Y][bcar2X] = 'b'
                MDPchanged = True
                #printMDP()

def moveCar(drxn):
    global playCar, carX, carY, MDP, MDPchanged, move, badCarCoords, myChoice
    MDP[carY][carX] = 'e'
    #if drxn == "down" and carY < (len(MDP)-1) and ((myChoice == 1) <= (not (carX, carY+1) in badCarCoords)):
    if drxn == "down" and carY < (len(MDP)-1):
        carY += 1
        move = True
    #elif drxn == "up" and carY > 0 and ((myChoice == 1) <= (not (carX, carY-1) in badCarCoords)):
    elif drxn == "up" and carY > 0:
        carY -= 1
        move = True
    #elif drxn == "left" and carX > 0 and ((myChoice == 1) <= (not (carX-1, carY) in badCarCoords)):
    elif drxn == "left" and carX > 0:
        carX -= 1
        move = True
    #elif drxn == "right" and carX < (len(MDP[0])-1) and ((myChoice == 1) <= (not (carX+1, carY) in badCarCoords)):
    elif drxn == "right" and carX < (len(MDP[0])-1):
        carX += 1
        move = True
    MDP[carY][carX] = 'p'
    MDPchanged = True
    #printMDP()

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
            yr = make_rect((i*(100.0)+(50.0), buff+(k+1)*roadWidBuff),(50.0, 50.0/(2*numLines)))
            yrect = Rectangle(yr[0], yr[1])
            yrect.setOutline("black")
            yrect.setFill("yellow")
            line.append(yrect)

    for i in line:
        i.draw(win)
    return line

main()
