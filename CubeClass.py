#written by Cambrea Earley
#AndrewID: cne
#Section B

#################################################

import copy
from colorSelection import *

#################################################
#cube class, allows for rotations of all faces in all direction of the rubiks cube
#gets colors for cube from the cube.txt file
#################################################

class RubiksCube(object):
    #cube face color mapped to index of face
    cubeFaces = {'f':0, 'b':1, 'r':2, 'l':3, 'u':4, 'd':5}
    
    def __init__(self, cube = None):
        
        #faces are front, back, right, left, up, down
        self.faces = ['f','b','r','l','u','d']
        self.possibleMoves = ["F","F'","B","B'","R","R'","L","L'","U","U'","D","D'"]
        #all moves to solve cube
        self.moveSeq = []
        if(cube == None):
            #gets cube from file
            cube = currCube()
        self.cube = cube
        self.completedCube= [ 
                #front face 
                [['w','w','w'],
                ['w','w','w'],
                ['w','w','w']],
                #back face
                [['y','y','y'],
                ['y','y','y'],
                ['y','y','y']],
                #right face
                [['r','r','r'],
                ['r','r','r'],
                ['r','r','r']],
                #left face
                [['o','o','o'],
                ['o','o','o'],
                ['o','o','o']],
                #up/top face
                [['b','b','b'],
                ['b','b','b'],
                ['b','b','b']],
                #down/bottom face
                [['g','g','g'],
                ['g','g','g'],
                ['g','g','g']]
                            ]
                        
    def eq(self, other):
        return (self.cube == other.cube) and (isinstance(other, RubiksCube))
   
    def rotate(self, side, dir):
        #transposes any face 90 degrees
        #gets the right index
        self.faceIndex = self.faces.index(side)
        faceIndex = self.faceIndex
        faceCopy = copy.deepcopy(self.cube[faceIndex])
        #transpose face
        #code(just the next nested for loop) taken from 
        #https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
        for i in range(len(faceCopy)):
            for j in range(i+1, len(faceCopy)):
                temp=faceCopy[i][j]  
                faceCopy[i][j]=faceCopy[j][i]  
                faceCopy[j][i]=temp
        if(dir == 'c'):
            #switches columns about the y axis if rotating clockwise
            for row in range(len(faceCopy)):
                for col in range(len(faceCopy)):
                    val = faceCopy[row][col]
                    if(col == 2):col = 0
                    elif(col == 0):col = 2
                    self.cube[faceIndex][row][col] = val
        if(dir == 'cc'):
           #switches face about the x axis if rotating counter clockwise
            temp = copy.copy(faceCopy[0])
            faceCopy[0] = []
            faceCopy[0] = copy.copy(faceCopy[2])
            faceCopy[2] = []
            faceCopy[2] = temp
            #copy to cube
            self.cube[faceIndex] = []
            self.cube[faceIndex] = copy.deepcopy(faceCopy)
            
        self.callRotation(side,dir)
        
    def callRotation(self, side, dir):
        #calls correct rotation function and appends the rotation to the self.moveSeq list
        if(side == 'f'):
            if(dir == 'c'):self.moveSeq.append(self.possibleMoves[0])
            if(dir == 'cc'):self.moveSeq.append(self.possibleMoves[1])
            self.finishFrontRotation(dir)
        if(side == 'b'):
            if(dir == 'c'):self.moveSeq.append(self.possibleMoves[2])
            if(dir == 'cc'):self.moveSeq.append(self.possibleMoves[3])
            self.finishBackRotation(dir)
        if(side == 'r'):
            if(dir == 'c'):self.moveSeq.append(self.possibleMoves[4])
            if(dir == 'cc'):self.moveSeq.append(self.possibleMoves[5])
            self.finishRightRotation(dir)
        if(side == 'l'):
            if(dir == 'c'):self.moveSeq.append(self.possibleMoves[6])
            if(dir == 'cc'):self.moveSeq.append(self.possibleMoves[7])
            self.finishLeftRotation(dir)
        if(side == 'u'):
            if(dir == 'c'):self.moveSeq.append(self.possibleMoves[8])
            if(dir == 'cc'):self.moveSeq.append(self.possibleMoves[9])
            self.finishUpRotation(dir)
        if(side == 'd'):
            if(dir == 'c'):self.moveSeq.append(self.possibleMoves[10])
            if(dir == 'cc'):self.moveSeq.append(self.possibleMoves[11])
            self.finishDownRotation(dir)
    
    def getSidesToChange(self):
        faceIndex = self.faceIndex
        sides = []
        temp = []
        #gets the sides that will be changed based on the face that is rotated
        if(faceIndex % 2 == 0): temp = self.faces[:faceIndex] + self.faces[faceIndex+2:]
        else: temp = self.faces[:faceIndex-1] + self.faces[faceIndex + 1:]
        sides.extend(temp)
        #puts the sides in order going around the cube
        temp = []
        temp.extend([sides[i] for i in range(len(sides)) if i%2 == 0])
        temp.extend([sides[i] for i in range(len(sides)) if i%2 == 1])
        return temp
          
    def changeCol(self, face, col, vals):
        #changes the values of a column        
        faceC = copy.deepcopy(self.cube[face])
        for row in range(len(faceC)):
            for c in range(len(faceC)):
                if(col == c):
                    faceC[row][col] = vals.pop(0)
        self.cube[face] = [[]]
        self.cube[face] = copy.deepcopy(faceC)
        
    def getCol(self, face, col):
        #gets the values of a certain column on a face(2d list)
        result = []
        for row in range(len(face)):
            for c in range(len(face)):
                if( c == col):
                    result.append(face[row][col])
        #returns the values in a list 
        return result
        
    #start, end, and step depend on the direction of the rotation
    def start(self,i, dir):
        #the start of the for loop 
        if(dir == 'p'):return i+1
        if(dir == 'n'):return i-1
            
    def end(self, i, dir):
        #the end of the loop 
        if(dir == 'p'):return i+2
        if(dir == 'n'):return i-2
            
    def step(self, dir):
        #the step of the for loop 
        if(dir == 'p'): return 1
        if(dir == 'n'):return -1
    
    def finishFrontRotation(self, direction):
        if(direction == 'c'): dir = 'p'
        if(direction == 'cc'): dir = 'n'
        #change the surrounding side faces, the first row moves to left one
        cDict = RubiksCube.cubeFaces
        sides = self.getSidesToChange()
        #uses a temp variable, c to find colors
        c = copy.deepcopy(self.cube)
        for i in range(len(sides)):
            for j in range(self.start(i,dir) , self.end(i, dir), self.step(dir)):
                #wraps around to beginning 
                if(j == len(sides)): j = 0
                vals = []
                #if using u or d side
                if(sides[j] == 'u'): vals.extend(c[cDict['u']][2])
                if(sides[j] == 'd'):vals.extend(c[cDict['d']][0])
                if(sides[j] == 'r'): 
                    vals.extend(self.getCol(c[cDict['r']], 0))
                if(sides[j] == 'l'): 
                    vals.extend(self.getCol(c[cDict['l']], 2))
                #Changing the values on the cube
                if(sides[i] == 'r'):
                    if(direction == 'cc'): vals = vals[::-1]
                    self.changeCol(cDict[sides[i]], 0, vals)
                if(sides[i] == 'l'):
                    if(direction == 'cc'): vals = vals[::-1]
                    self.changeCol(cDict[sides[i]], 2, vals)
                if(sides[i] == 'u'):
                    if(direction == 'c'): vals = vals[::-1]
                    self.cube[cDict['u']][2] = []
                    self.cube[cDict['u']][2].extend(vals)
                if(sides[i] == 'd'):
                    if(direction == 'c'): vals = vals[::-1]
                    self.cube[cDict['d']][0] = []
                    self.cube[cDict['d']][0].extend(vals)
         
    def finishBackRotation(self, direction):
        if(direction == 'cc'): dir = 'p'
        if(direction == 'c'): dir = 'n'
        #change the surrounding side faces, the first row moves to left one
        cDict = RubiksCube.cubeFaces
        sides = self.getSidesToChange()
        #uses a temp variable, c to find colors
        c = copy.deepcopy(self.cube)
        for i in range(len(sides)):
            for j in range(self.start(i,dir), self.end(i, dir), self.step(dir)):
                #wraps around to beginning 
                if(j == len(sides)): j = 0
                vals = []
                #if using u or d side
                if(sides[j] == 'u'): vals.extend(c[cDict['u']][0])
                if(sides[j] == 'd'):vals.extend(c[cDict['d']][2])
                if(sides[j] == 'r'): 
                    vals.extend(self.getCol(c[cDict['r']], 2))
                if(sides[j] == 'l'): 
                    vals.extend(self.getCol(c[cDict['l']], 0))
                #Changing the values on the cube
                if(sides[i] == 'r'):
                    if(direction == 'c'): vals = vals[::-1]
                    self.changeCol(cDict[sides[i]], 2, vals)
                if(sides[i] == 'l'):
                    if(direction == 'c'): vals = vals[::-1]
                    self.changeCol(cDict[sides[i]], 0, vals)
                if(sides[i] == 'u'):
                    if(direction == 'cc'): vals = vals[::-1]
                    self.cube[cDict['u']][0] = []
                    self.cube[cDict['u']][0].extend(vals)
                if(sides[i] == 'd'):
                    if(direction == 'cc'): vals = vals[::-1]
                    self.cube[cDict['d']][2] = []
                    self.cube[cDict['d']][2].extend(vals)

    def finishRightRotation(self, direction):
        if(direction == 'cc'): dir = 'p'
        if(direction == 'c'): dir = 'n'
        #change the surrounding side faces, the first row moves to left one
        cDict = RubiksCube.cubeFaces
        sides = self.getSidesToChange()
        #uses a temp variable, c to find colors
        c = copy.deepcopy(self.cube)
        for i in range(len(sides)):
            for j in range(self.start(i,dir), self.end(i, dir), self.step(dir)):
                #wraps around to beginning 
                if(j == len(sides)): j = 0
                #gets values
                vals = []
                if(sides[j] == 'b'):vals.extend(self.getCol(c[cDict['b']], 0))
                else:
                    vals.extend(self.getCol(c[cDict[sides[j]]], 2))
                #Changing the values on the cube, make sure to copy down cirrect values
                if(sides[i] == 'b'): 
                    vals = vals[::-1]
                    self.changeCol(cDict['b'], 0, vals)
                else:
                    if(sides[i] == 'd'and direction == 'c'): vals = vals[::-1]
                    if(sides[i] == 'u' and direction == 'cc'): vals = vals[::-1]
                    self.changeCol(cDict[sides[i]], 2, vals)
        
    def finishLeftRotation(self, direction):
        if(direction == 'c'): dir = 'p'
        if(direction == 'cc'): dir = 'n'
        #change the surrounding side faces, the first row moves to left one
        cDict = RubiksCube.cubeFaces
        sides = self.getSidesToChange()
        #uses a temp variable, c to find colors
        c = copy.deepcopy(self.cube)
        for i in range(len(sides)):
            for j in range(self.start(i,dir), self.end(i, dir), self.step(dir)):
                #wraps around to beginning 
                if(j == len(sides)): j = 0
                #gets values
                vals = []
                if(sides[j] == 'b'):vals.extend(self.getCol(c[cDict['b']], 2))
                else:
                    vals.extend(self.getCol(c[cDict[sides[j]]], 0))
                #Changing the values on the cube
                if(sides[i] == 'b'):
                    vals = vals[::-1]
                    self.changeCol(cDict['b'], 2, vals)
                else:
                    if(sides[i] == 'u' and direction == 'c'): vals = vals[::-1]
                    if(sides[i] == 'd' and direction == 'cc'):vals = vals[::-1]
                    self.changeCol(cDict[sides[i]], 0, vals)
        
    def finishUpRotation(self, direction):
        if(direction == 'c'): dir = 'p'
        if(direction == 'cc'): dir = 'n'
        #change the surrounding side faces, the first row moves to left one
        cDict = RubiksCube.cubeFaces
        sides = self.getSidesToChange()
        #uses a temp variable, c to find colors
        c = copy.deepcopy(self.cube)
        for i in range(len(sides)):
            for j in range(self.start(i,dir), self.end(i, dir), self.step(dir)):
                #wraps around to beginning 
                if(j == len(sides)): j = 0
                #empties first row
                self.cube[cDict[sides[i]]][0] = []
                #fills in with new color 
                self.cube[cDict[sides[i]]][0].extend(c[cDict[sides[j]]][0])
        
    def finishDownRotation(self, direction):
        if(direction == 'cc'): dir = 'p'
        if(direction == 'c'): dir = 'n'
        #change the surrounding side faces, the first row moves to left one
        cDict = RubiksCube.cubeFaces
        sides = self.getSidesToChange()
        #uses a temp variable, c to find colors
        c = copy.deepcopy(self.cube)
        for i in range(len(sides)):
            for j in range(self.start(i,dir), self.end(i, dir), self.step(dir)):
                #wraps around to beginning 
                if(j == len(sides)): j = 0
                #empties first row
                self.cube[cDict[sides[i]]][2] = []
                #fills in with new color 
                self.cube[cDict[sides[i]]][2].extend(c[cDict[sides[j]]][2])
            
def currCube():
    #runs the colorSelection file, the start screen and color selection screen
    run(500, 300)
    #opens cube file
    with open('cube.txt','r') as myFile:
        data = myFile.read()
    #separates the colors of the faces
    fFace = data[:9]
    bFace = data[9:18]
    rFace = data[18:27]
    lFace = data[27:36]
    uFace = data[36:45]
    dFace = data[45:54]
    #an empty cube
    cube= [ #front face 
            [[0,0,0],[0,0,0],[0,0,0]],
            #back face
            [[0,0,0],[0,0,0],[0,0,0]],
            #right face
            [[0,0,0],[0,0,0],[0,0,0]],
            #left face
            [[0,0,0],[0,0,0],[0,0,0]],
            #up/top face
            [[0,0,0],[0,0,0],[0,0,0]],
            #down/bottom face
            [[0,0,0],[0,0,0],[0,0,0]],]
    for face in range(6):    
        i = 0
        for row in range(3):
            for col in range(3):
               #adds the values to the empty cube
                if(face == 0):
                    val = fFace[i]                
                if(face == 1):
                    val = bFace[i]                    
                if(face == 2):
                    val = rFace[i]                
                if(face == 3):
                    val = lFace[i]
                if(face == 4):
                    val = uFace[i]
                if(face == 5):
                    val = dFace[i]
                cube[face][row][col] = val
                i += 1
    #returns the cube filled in with the users data
    return cube
