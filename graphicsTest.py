#import libraries
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
listener = None         #keyboard listener, to be created in main()

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

    #set background (dirt road)
    win.setBackground('burlywood')

    #draw grey road
    drawRoad(win, roadBuff)
    #create lines for grid, but don't draw them yet
    for i in range(6):
        line = Line(Point((i+1)*(WIDTH/7), 0), Point((i+1)*(WIDTH/7), HEIGHT))
        grid.append(line)
    #draw road lines, first parameter is how many to draw
    rlines = drawLines(6, win, roadBuff)

    #calculate lane width
    laneWidth = rlines[0].getCenter().getY() - roadBuff

    #resize player car to fit in lane
    image = img.open("car.png")
    newHeight = int(laneWidth*0.8)
    hpercent = (newHeight / float(image.size[1]))
    wsize = int((float(image.size[0])*float(hpercent)))
    image = image.resize((wsize, newHeight), img.ANTIALIAS)
    image.save('car.png')
    
    #draw car in the center of the screen
    playCar = Image(Point(WIDTH/2,HEIGHT/2), "car.png")
    playCar.draw(win)

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
    global listener
    global win
    listener.stop()
    win.close()

#keyboard listener method
def on_press(key):
    global done
    global drawn
    global qp
    if key == Key.esc:  #press esc to quit
        done = True
    if key.char == 'q': #press q to toggle the grid
        qp = True

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
