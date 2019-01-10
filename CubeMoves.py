#written by Cambrea Earley
#AndrewID: cne
#Section B

#################################################

import tkinter
from tkinter import *
from solveCubeClass import *
from PIL import ImageTk, Image

####################################
# Displays the moves, allows the user to step between the  moves
####################################

def init(data):
    #load data.xyz as appropriate
    data.moveIndex = 0
    #getes cube from solve cube class
    cube = SolveCube()
    data.moves = cube.cube.moveSeq
    data.time = 0
    data.play = False
    #Dictionary mapping move, to the correct file, as a gif
    data.fileDict = {'U':'cubeUpC.gif',"U'":'cubeUpCC.gif',\
    'U2':'cubeUpC.gif',"U'2":'cubeUpC.gif','D':'cubeDownC.gif',\
    "D'":'cubeDownCC.gif','D2':'cubeDownC.gif',"D'2":'cubeDownC.gif', \
    'R':'cubeRightC.gif', "R'":'cubeRightCC.gif', 'R2':'cubeRightC.gif', \
    "R'2":'cubeRightC.gif', 'L':'cubeLeftC.gif', "L'":'cubeLeftCC.gif',\
    'L2':'cubeLeftC.gif',"L'2":'cubeLeftC.gif', 'F':'cubeFrontC.gif',\
    "F'":'cubeFrontCC.gif','F2':'cubeFrontC.gif',"F'2":'cubeFrontC.gif',\
    "B": 'cubeBackC.gif', "B'":'cubeBackCC.gif',"B2": 'cubeBackC.gif',"B'2":'cubeBackC.gif'}
    #dictionary mapping moves to the set of directions
    data.moveDir = {'U':'U: Move Up face Clockwise', "U'":"U': Move Up face Counter Clockwise"\
    ,'U2':'U2: Move Up face Clockwise 180 Degrees',"U'2":'U2: Move Up face Clockwise 180 Degrees'\
    ,'D':"D: Move Down face Clockwise","D'":"D': Move Down face Counter Clockwise"\
    ,'D2':"D2: Move Down face Clockwise 180 Degrees","D'2":"D2: Move Down face Clockwise 180 Degrees",\
    'R':"R: Move Right face Clockwise", "R'":"R': Move Right face Counter Clockwise",\
    "R2":"R2: Move Right face Clockwise 180 Degrees",'L':"L: Move Left face Clockwise",\
    "R'2":"R2: Move Right face Clockwise 180 Degrees","L'":"L': Move Left face Counter Clockwise",\
    'L2':"L2: Move Left face Clockwise 180 Degrees","L'2":"L2: Move Left face Clockwise 180 Degrees",\
    'F':"F: Move Front face Clockwise", "F'" :"F': Move Front face Counter Clockwise",\
    "F'2":"F2: Move Front face Clockwise 180 Degrees",'F2':"F2: Move Front face Clockwise 180 Degrees",\
    'B':"B: Move Back face Clockwise", "B'" :"B': Move Back face Counter Clockwise",\
    'B2':"B2: Move Back face Clockwise 180 Degrees","B'2":"B2: Move Back face Clockwise 180 Degrees"}

def withinBox(data,event, x0,y0, x1, y1):
    #checks if click is within box
    return (event.x > x0) and (event.x < x1) and (event.y > y0) and (event.y < y1)

def mousePressed(event, data):
    # use event.x and event.y
    #if the play button is clicked
    if(withinBox(data, event,data.width/2 - 40, data.height - 30,\
     data.width/2 + 40, data.height - 10) and not data.moveIndex == len(data.moves)):
        data.play = not data.play
        data.time = 0
    
    #if the next button is clicked
    if(withinBox(data, event, data.width - 98, data.height - 30, data.width - 30, data.height - 10)):
        data.moveIndex += 1
    #if the previous button is clicked
    if(withinBox(data,event,30, data.height - 30, 90, data.height - 10)):
        data.moveIndex -= 1
    #make sure the move index is in bounds
    if(data.moveIndex < 0):
        data.moveIndex = 0 
    if(data.moveIndex >= len(data.moves) + 1):
        data.moveIndex = len(data.moves) 
  
def keyPressed(event, data):
    # use event.char and event.keysym
    #works on key pressed also
    if (event.keysym in ["Up", "Right"]):
        data.moveIndex += 1
    if (event.keysym in ["Down", "Left"]):
        data.moveIndex -= 1
    #keeps move index inbounds
    if(data.moveIndex < 0):
        data.moveIndex = 0 
    if(data.moveIndex >= len(data.moves) + 1):
        data.moveIndex = len(data.moves) 

def timerFired(data):
    if(data.play and (not data.moveIndex == len(data.moves)) ):
        data.time += 1
        if(data.time % 30 == 0):
            data.moveIndex += 1
            #keeps move index inbounds
            if(data.moveIndex < 0):
                data.moveIndex = 0 
            if(data.moveIndex >= len(data.moves) + 1):
                data.moveIndex = len(data.moves) 
        
def displayMove(canvas, data):
    #if The moves are done and the user has solved the cube
    if(data.moveIndex == len(data.moves) ):
        canvas.create_text(data.width/2, data.height - 80, text = "Done!", font = ('arial',25))
        img = tkinter.PhotoImage(file = 'cube.gif')
        label = Label(image = img)
        label.image = img
        canvas.create_image(data.width/2, data.height/2, image = img)
    #while the user is moving between the moves
    else:
        #gets the move
        data.currMove = data.moves[data.moveIndex]
        #displays directions
        dir = data.moveDir[data.currMove]
        canvas.create_text(data.width/2, 60, text = dir, font = ('arial', 15))
        numMove = str(data.moveIndex + 1) + ' out of ' + str(len(data.moves)) 
        canvas.create_text(data.width/2, 90, text = numMove)
        #opens the image file
        img = tkinter.PhotoImage(file = data.fileDict[data.currMove])
        label = Label(image = img)
        label.image = img
        #display image
        canvas.create_image(data.width/2, data.height/2, image = img)

def redrawAll(canvas, data):
    #creates the next button
    canvas.create_text(data.width/2, 20, text = 'Moves', font = ('arial', 30))
    canvas.create_rectangle(data.width - 98, data.height - 30, data.width - 30, data.height - 10)
    canvas.create_text(data.width - 75, data.height - 28, text = "Next", anchor = 'nw')
    #creates the previous button
    canvas.create_rectangle(30, data.height - 30, 90, data.height - 10)
    canvas.create_text(36, data.height - 28, text = "Previous", anchor = 'nw')
    #creates play Button
    canvas.create_rectangle(data.width/2 - 40, data.height - 30, data.width/2 + 40, data.height - 10)
    if(not data.play):
        canvas.create_text(data.width/2, data.height - 20, text = 'Play Moves')
    if(data.play):
        canvas.create_text(data.width/2, data.height - 20, text = 'Pause Moves')
    #shows the moves
    displayMove(canvas,data)
    
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

run(400, 350)
    