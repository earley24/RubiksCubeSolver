#written by Cambrea Earley
#AndrewID: cne
#Section B 

from tkinter import *
from isLegalCube import *
import random

####################################
# Program displays the start screen and the color selection screen
# after the user selects the colors, the cube is written to a file(add call to run, to run solo)
####################################

def init(data):
    # load data.xyz as appropriate
    data.cellSize = 20
    data.currColor = None
    data.currFaceIndex = None
    data.invCube = False
    #starts on 'start' mode 
    data.mode = 'start'
    data.colors = ['red','blue','green','white','yellow', 'orange']
    data.startColor = data.colors[0]
    data.cubeFaceX = random.randint(50, data.width - data.cellSize*2)
    data.cubeFaceY = random.randint(50, data.height -  data.cellSize*2)
    data.dy = -1
    data.dx = -1
    data.time = 0
    #the colors of the cube
    data.cube = [ #front face 
            [['w','w','w'],
            ['w','w','w'],
            ['w','w','w']],
            #back face
            [['w','w','w'],
            ['w','y','w'],
            ['w','w','w']],
            #right face
            [['w','w','w'],
            ['w','r','w'],
            ['w','w','w']],
            #left face
            [['w','w','w'],
            ['w','o','w'],
            ['w','w','w']],
            #up/top face
            [['w','w','w'],
            ['w','b','w'],
            ['w','w','w']],
            #down/bottom face
            [['w','w','w'],
            ['w','g','w'],
            ['w','w','w']],
                        ]
    #coordinates of the cube boxes
    data.coords = [ #front face 
            [[0,0,0],
            [0,0,0],
            [0,0,0]],
            #back face
            [[0,0,0],
            [0,0,0],
            [0,0,0]],
            #right face
            [[0,0,0],
            [0,0,0],
            [0,0,0]],
            #left face
            [[0,0,0],
            [0,0,0],
            [0,0,0]],
            #up/top face
            [[0,0,0],
            [0,0,0],
            [0,0,0]],
            #down/bottom face
            [[0,0,0],
            [0,0,0],
            [0,0,0]],
                        ]
                        
def withinBox(data,event, x0,y0, x1, y1):
    #checks if click is within box
    return (event.x > x0) and (event.x < x1) and (event.y > y0) and (event.y < y1)
    
def changeCurrColor(event, data):
    #if the users clicks on one of these boxes, the selected color changes
    #red
    if(withinBox(data,event,350,90, 410, 115)):
        data.currColor = 'Red'
    #orange
    if(withinBox(data,event,350,115, 410, 140)):
        data.currColor = 'Orange'
    #yellow
    if(withinBox(data,event,350,140, 410, 165)):
        data.currColor = 'Yellow'
    #green
    if(withinBox(data,event,350,165, 410, 190)):
        data.currColor = 'Green'
    #blue
    if(withinBox(data,event,350,190, 410, 215)):
        data.currColor = 'Blue'
    #white
    if(withinBox(data,event,350,215, 410, 230)):
        data.currColor = 'White'
    
def mousePressed(event, data):
    # use event.x and event.y
    if(data.mode == 'start'):
        #in start mode, can only click start
        if(withinBox(data,event,data.width/2 - 30, data.height - 70,data.width/2 + 30, data.height - 40)):
            data.mode = 'selectC'
    if(data.mode == 'selectC'):
        #in the color selction mode
        #select current color
        changeCurrColor(event,data)
        #changes colors on cube
        for face in range(6):
            for row in range(3):
                for col in range(3):
                    coord = data.coords[face][row][col]
                    x0 = coord[0]
                    y0 = coord[1]
                    x1 = coord[2]
                    y1 = coord[3]
                    
                    if(withinBox(data, event, x0,y0,x1,y1)):
                        if not (row == 1 and col == 1):
                            data.currFace = face
                            data.currRow = row
                            data.currCol = col
                            changeColor(data)
        #click on done
        if(withinBox(data,event, data.width-100, data.height-30, data.width-30, data.height-10)):
            #checks if the inputted cube is legal
            if(legalColor(data.cube)):
                data.invCube = False
                data.mode = 'Done'
                #writes the cube to the cube.txt file so it can be used by the cube solver
                cubeFile = open('cube.txt','w')
                for face in range(6):
                    for row in range(3):
                        for col in range(3):
                            c = data.cube[face][row][col]
                            cubeFile.write(c)
            else:
                #if invalid cube is entered
                data.invCube = True

def changeColor(data):
    #changes the color in the cube list
    if(data.currColor == 'Red'):
        data.cube[data.currFace][data.currRow][data.currCol] = 'r'
        
    if(data.currColor == 'Orange'):
        data.cube[data.currFace][data.currRow][data.currCol] = 'o'
        
    if(data.currColor == 'Yellow'):
        data.cube[data.currFace][data.currRow][data.currCol] = 'y'
    
    if(data.currColor == 'Green'):
        data.cube[data.currFace][data.currRow][data.currCol] = 'g'
    
    if(data.currColor == 'Blue'):
        data.cube[data.currFace][data.currRow][data.currCol] = 'b'
        
    if(data.currColor == 'White'):
        data.cube[data.currFace][data.currRow][data.currCol] = 'w'
    
def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    if(data.mode == 'start'):
        data.time += 1
        
        if(data.time % 10 == 0):
            r = random.randint(0,5)
            data.startColor = data.colors[r]

def startScreen(canvas,data):
    #random starting location of cube Face
    draw3X3(canvas,data, data.cubeFaceX,data.cubeFaceY,None,data.startColor)
    
    #check if the target is hitting the side of the screen
    #if it is hitting the side, change the direction
    if(data.cubeFaceX   < 0):
        data.dx = -data.dx
        data.cubeFaceX = 1
    if(data.cubeFaceY  < 0):
        data.dy = -data.dy
        data.cubeFaceY = 1
        
    if((data.cubeFaceX + data.cellSize*3) > data.width):
        data.dx = -data.dx
        data.cubeFaceX = data.width - data.cellSize*3
        
    if((data.cubeFaceY + data.cellSize*3) > data.height):
        data.dy = -data.dy
        data.cubeFaceY = data.height - data.cellSize*3
    #moves the target
    data.cubeFaceY += data.dy
    data.cubeFaceX += data.dx
    
    #start mode labels and start button
    canvas.create_text(data.width/2, 30, text = "Rubik's Cube Solver!", font = ('arial', 30))
    canvas.create_text(data.width/2, 70, text = "Click Start to begin")
    canvas.create_rectangle(data.width/2 - 30, data.height - 70,data.width/2 + 30, data.height - 40, fill = 'white')
    canvas.create_text(data.width/2, data.height - 65, text = 'Start', anchor = 'n', font = ('arial', 15))

def redrawAll(canvas, data):
    # draw in canvas
    if(data.mode == 'start'):
      startScreen(canvas,data)

    if(data.mode == 'selectC'):
        #select mode labels 
        canvas.create_text(data.width/2, 20, text = 'Fill in Your Cube', font = ('arial', 20))
        #draws the color selection boxes
        drawColorBoxes(canvas,data)
        #draws the grid of the cube with colors filled in
        draw2dCube(canvas,data)
        #the done button
        canvas.create_rectangle(data.width - 100, data.height - 30, data.width - 30, data.height - 10)
        canvas.create_text(data.width - 80, data.height - 28, text = "Done", anchor = 'nw')
        #if the cube is invalid display text
        if(data.invCube):
            canvas.create_text(data.width/2, 40, text = 'Cube is Invalid', fill = 'red')
        
def drawColorBoxes(canvas,data):
    width = 60
    height = 15
    #creates the color selection boxes
    canvas.create_text(380,70,text = 'Select a Color')
    canvas.create_rectangle(350, 90, 350 + width, 90 + height, fill = 'red')
    canvas.create_rectangle(350, 115, 350 + width, 115 + height, fill = 'orange')
    canvas.create_rectangle(350, 140, 350 + width, 140 + height, fill = 'yellow')
    canvas.create_rectangle(350, 165, 350 + width, 165 + height, fill = 'green')
    canvas.create_rectangle(350, 190, 350 + width, 190 + height, fill = 'blue')
    canvas.create_rectangle(350, 215, 350 + width, 215 + height, fill = 'white')
    #if a color is selected, display text 
    if(data.currColor != None):
        string = 'Color Selected: ' + data.currColor
        canvas.create_text(380,250, text = string)
        
def getColor(c):
    #changes letter into word, to diplay correct color
    if(c == 'r'):
        return 'red'
    if(c == 'o'):
        return 'orange'
    if(c == 'y'):
        return 'yellow'
    if(c == 'g'):
        return 'green'
    if(c == 'b'):
        return 'blue'
    if(c == 'w'):
        return 'white'
        
def draw3X3(canvas,data, x,y, face, cStart = None):
    #draw the cube grid, draws a 3x3 grid
    for row in range(3):
        for col in range(3):
            if(data.mode == 'start'):
                color = cStart
                data.cellSize = 40
            else:
                data.cellSize = 20
            #gets coord of grid
            x0 = x + col*data.cellSize
            x1 = x0 + data.cellSize
            y0 = y + row*data.cellSize
            y1 = y0 + data.cellSize
            #gets color for each square, using cube list
            if(data.mode == 'start'):
                color = cStart
                
            if(data.mode == 'selectC'):
                c = data.cube[face][row][col]
                color = getColor(c)
                #adds coords of each cube to list
                data.coords[face][row][col] = (x0,y0,x1,y1)
                    
            canvas.create_rectangle(x0,y0,x1,y1, fill = color)
           
def draw2dCube(canvas,data):    
    #draws each 3x3 grid in correct location on canvas
    draw3X3(canvas, data,80, 150, 0)
    draw3X3(canvas,data, 220,150, 1)
    draw3X3(canvas,data,150, 150, 2)
    draw3X3(canvas,data,10, 150, 3)
    draw3X3(canvas,data,80,80, 4)
    draw3X3(canvas,data,80,220, 5)
  
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")