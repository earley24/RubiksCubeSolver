#written by Cambrea Earley
#AndrewID: cne
#Section B

#################################################

import copy
from CubeClass import *

#################################################
#Cube solver class, Solves the cube and gets the list of moves to solve the cube
#################################################

class SolveCube(object):

    def __init__(self):
        #gets cube instace from RubiksCube class
        self.cube = RubiksCube()
        print('Inputted Cube\n',self.cube.cube)
        #index of edges and corners
        self.edges = [(0,1), (1,0), (1,2), (2,1)]
        self.corners = [(0,0),(0,2),(2,0),(2,2)]
        #the face colors and face order
        self.faceColor = ['w','y','r','o','b','g']
        self.faceOrder = ['f','b','r','l','u','d']
        #start solving if the cube isnt already solved
        if(self.cube.cube != self.cube.completedCube):   
            #go through steps to solve cube
            self.solveCross()
            self.solveWhiteCorners()
            #if middle layer not solved
            if(not self.middleLayerSolved()):
                self.middleLayer()
            #if yellow edges not solved
            if(not self.yellowEdgeSolved()):
                self.solveYellowEdge()
            self.solveYellowCorner()
            self.fixYellowCorners()            
        while(self.cube.cube != self.cube.completedCube):
            #if not already solved
            self.permuteYellowEdge()
        #print moves in console
        print('\nSolved Cube\n', self.cube.cube,'\n\n')
        print('Moves')
        self.displayMoves()
       
    def checkYellow(self, row, col):
        #check if white piece already in the way 
        for i in range(4):
            if(self.cube.cube[1][row][col] == 'w'):
                self.cube.rotate('b','c')
            else: break
        
    def correctDaisy(self):
        for e in range(len(self.edges)):
            #coords of edge piece 
            row = self.edges[e][0]
            col = self.edges[e][1]
            if(self.cube.cube[1][row][col] != 'w'):
                return False
        return True 
        
    def rightFaceWE(self):
        hasWhiteEdge = True
        edges = self.edges
        #For right face, red 
        while(hasWhiteEdge):
            hasWhiteEdge = False
            for e in range(len(edges)):
                #coords of edge piece
                row = edges[e][0]
                col = edges[e][1]
                if(self.cube.cube[2][row][col] == 'w'):
                    hasWhiteEdge = True
                    #different moves depending on position of white
                    if(e == 0):
                        self.checkYellow(row, col)
                        self.cube.rotate('u', 'cc')
                    if(e == 1):
                        self.cube.rotate('r','cc')
                        self.checkYellow(2, 1)
                        self.cube.rotate('d', 'c')
                        self.cube.rotate('r','c')
                    if(e == 2):
                        self.cube.rotate('r','c')
                        self.checkYellow(2, 1)
                        self.cube.rotate('d', 'c')
                    if(e == 3):
                        self.checkYellow(row, col)
                        self.cube.rotate('d', 'c')
        
    def leftFaceWE(self):
        hasWhiteEdge = True
        edges = self.edges
        #For left face, orange
        while(hasWhiteEdge):
            hasWhiteEdge = False
            for e in range(len(edges)):
                #coords of edge piece 
                row = edges[e][0]
                col = edges[e][1]
                if(self.cube.cube[3][row][col] == 'w'):
                    hasWhiteEdge = True
                    #different moives depending on position of white
                    if(e == 0):
                        self.checkYellow(row, col)
                        self.cube.rotate('u', 'c')
                    if(e == 1):
                        self.cube.rotate('l','c')
                        self.checkYellow(0, 1)
                        self.cube.rotate('u', 'c')
                    if(e == 2):
                        self.cube.rotate('l','cc')
                        self.checkYellow(0, 1)
                        self.cube.rotate('u', 'c')
                        self.cube.rotate('l', 'c')
                    if(e == 3):
                        self.checkYellow(row, col)
                        self.cube.rotate('d', 'cc')
                        
    def upFaceWE(self):
        hasWhiteEdge = True
        edges = self.edges
        #For up face, blue
        while(hasWhiteEdge):
            hasWhiteEdge = False
            for e in range(len(edges)):
                #coords of edge piece 
                row = edges[e][0]
                col = edges[e][1]
                if(self.cube.cube[4][row][col] == 'w'):
                    hasWhiteEdge = True
                    #different moives depending on position of white
                    if(e == 0):
                        self.cube.rotate('u','c')
                        self.checkYellow(1, 0)
                        self.cube.rotate('r', 'c')
                    if(e == 1):
                        self.checkYellow(1, 2)
                        self.cube.rotate('l', 'cc')
                    if(e == 2):
                        self.checkYellow(1, 0)
                        self.cube.rotate('r', 'c')
                    if(e == 3):
                        self.cube.rotate('u','cc')
                        self.checkYellow(1, 0)
                        self.cube.rotate('r', 'c')
                        self.cube.rotate('u','c')
    
    def downFaceWE(self):
        hasWhiteEdge = True
        edges = self.edges
        #For down face, green
        while(hasWhiteEdge):
            hasWhiteEdge = False
            for e in range(len(edges)):
                #coords of edge piece 
                row = edges[e][0]
                col = edges[e][1]
                if(self.cube.cube[5][row][col] == 'w'):
                    hasWhiteEdge = True
                    #different moives depending on position of white
                    if(e == 0):
                        self.cube.rotate('d','cc')
                        self.checkYellow(1, 2)
                        self.cube.rotate('l', 'c')
                        self.cube.rotate('d','c')
                    if(e == 1):
                        self.checkYellow(1, 2)
                        self.cube.rotate('l', 'c')
                    if(e == 2):
                        self.checkYellow(1, 0)
                        self.cube.rotate('r', 'cc')
                    if(e == 3):
                        self.cube.rotate('d','c')
                        self.checkYellow(1, 2)
                        self.cube.rotate('l', 'c')
        
    def frontFaceWE(self):
        hasWhiteEdge = True
        edges = self.edges
        #for front face, white
        for e in range(len(edges)):
            #coords of edge piece 
            row = edges[e][0]
            col = edges[e][1]
            #checks for white 
            if(self.cube.cube[0][row][col] == 'w'):
                if(e == 0):
                    self.checkYellow(row, col)
                    self.cube.rotate('u','c')
                    self.cube.rotate('u','c')
                if(e == 1):
                    self.checkYellow(row, 2)
                    self.cube.rotate('l','c')
                    self.cube.rotate('l','c')
                if(e == 2):
                    self.checkYellow(row, 0)
                    self.cube.rotate('r','c')
                    self.cube.rotate('r','c')
                if(e == 3):
                    self.checkYellow(row, col)
                    self.cube.rotate('d','c')
                    self.cube.rotate('d','c')
        
    def solveDaisy(self):
        #solve the daisy, white edges on yellow face
        self.rightFaceWE()
        self.leftFaceWE()
        self.upFaceWE()
        self.downFaceWE()
        self.frontFaceWE()
        #if not done, repeat
        if(not self.correctDaisy()):
           self.solveDaisy()
           
    def checkWhite(self):
        #returns false if white edge piece on yellow side
        for e in range(len(self.edges)):
            #coords of edge piece 
            row = self.edges[e][0]
            col = self.edges[e][1]
            if(self.cube.cube[1][row][col] == 'w'):
                return False
        return True
         
    def rotateToWhite(self):
        #rotates daisy, white edges to white face
        for e in range(len(self.edges)):
            #coords of edge piece 
            row = self.edges[e][0]
            col = self.edges[e][1]
            #make sure the colors on the middle layer are matches up before
            #the side is changed to the white face
            if(self.cube.cube[1][row][col] == 'w'):
                if(e == 0):
                    color = self.cube.cube[4][0][1]
                    if(color == 'r'):
                        self.cube.rotate('b','cc')
                    if(color == 'o'):
                        self.cube.rotate('b', 'c')
                    if(color == 'g'):
                        self.cube.rotate('b','c')
                        self.cube.rotate('b','c')
                if(e == 1):
                    color = self.cube.cube[2][1][2]
                    if(color == 'b'):
                        self.cube.rotate('b','c')
                        
                    if(color == 'o'):
                        self.cube.rotate('b', 'c')
                        self.cube.rotate('b', 'c')
                        
                    if(color == 'g'):
                        self.cube.rotate('b','cc')
                if(e == 2):
                    color = self.cube.cube[3][1][0]
                    if(color == 'b'):
                        self.cube.rotate('b','cc')
                    if(color == 'r'):
                        self.cube.rotate('b', 'c')
                        self.cube.rotate('b', 'c')
                    if(color == 'g'):
                        self.cube.rotate('b','c')
                if(e == 3):
                    color = self.cube.cube[5][2][1]
                    if(color == 'b'):
                        self.cube.rotate('b','c')
                        self.cube.rotate('b','c')                        
                    if(color == 'o'):
                        self.cube.rotate('b', 'cc')
                    if(color == 'r'):
                        self.cube.rotate('b','c')
                if(color == 'r'):
                    self.cube.rotate('r','c')
                    self.cube.rotate('r','c')
                if(color == 'b'):
                    self.cube.rotate('u','c')
                    self.cube.rotate('u','c')
                if(color == 'o'):
                    self.cube.rotate('l','c')
                    self.cube.rotate('l','c')
                if(color == 'g'):
                    self.cube.rotate('d','c')
                    self.cube.rotate('d','c')
        if(not self.checkWhite()):
            #repeat if not done
            self.rotateToWhite()
            
    def whiteCrossDone(self):
        #checks if white cross is finished
        for e in range(len(self.edges)):
            #coords of edge piece 
            row = self.edges[e][0]
            col = self.edges[e][1]
            if(self.cube.cube[0][row][col] != 'w'):
                return False
        return (self.cube.cube[2][1][0] == 'r') and (self.cube.cube[3][1][2] == 'o')\
        and (self.cube.cube[4][2][1] == 'b') and (self.cube.cube[5][0][1] == 'g')
    
    def solveCross(self):
        #solve daisy, then rotate to white
        if(not self.whiteCrossDone()):
            self.solveDaisy()
            self.rotateToWhite()

    def checkBackRight(self):
        isWhite = True
        #while there is a white face on the back left side layers
        while(isWhite == True):
            isWhite = False
            if(self.cube.cube[2][0][2] == 'w'):
             #right face right back
                isWhite = True
                #the color on the opposite face
                opColor = self.cube.cube[4][0][2]
                if(opColor == 'g'):
                    #moves white out of way
                    self.cube.rotate('b','c')
                if(opColor == 'b'):
                   #moves white out of the way t 
                    self.cube.rotate('b','cc')
                if(opColor == 'r'):
                    #moves white out of the way then places it 
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')
                
            if(self.cube.cube[3][2][0] == 'w'):
                #left face right back
                isWhite = True
                #the color on the opposite face
                opColor = self.cube.cube[5][2][0]
                if(opColor == 'g'):
                    #moves white out of way
                    self.cube.rotate('b','cc')
                if(opColor == 'b'):
                   #moves white out of the way t 
                    self.cube.rotate('b','c')
                if(opColor == 'o'):
                    #moves white out of the way then places it 
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')
            
            if(self.cube.cube[4][0][0] == 'w'):
                #up face right back
                isWhite = True
                #the color on the opposite face
                opColor = self.cube.cube[3][0][0]
                if(opColor == 'r'):
                    #moves white out of way
                    self.cube.rotate('b','c')
                if(opColor == 'o'):
                   #moves white out of the way t 
                    self.cube.rotate('b','cc')
                if(opColor == 'b'):
                    #moves white out of the way then places it 
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')
                
            if(self.cube.cube[5][2][2] == 'w'):
                #down face right back
                isWhite = True
                #the color on the opposite face
                opColor = self.cube.cube[2][2][2]
                if(opColor == 'r'):
                    #moves white out of way
                    self.cube.rotate('b','cc')
                if(opColor == 'o'):
                   #moves white out of the way t 
                    self.cube.rotate('b','c')
                if(opColor == 'g'):
                    #moves white out of the way then places it 
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')
                
            if(isWhite == True):
                #rotate to correct face, depending on the opposite color
                if(opColor == 'g'):
                    self.cube.rotate('d', 'cc')
                    self.cube.rotate('b','c')
                    self.cube.rotate('d','c')
        
                if(opColor == 'b'):
                    self.cube.rotate('u','cc')
                    self.cube.rotate('b', 'c')
                    self.cube.rotate('u','c')
                    
                if(opColor == 'r'):
                    self.cube.rotate('r','cc')
                    self.cube.rotate('b','c')
                    self.cube.rotate('r','c')
                
                if(opColor == 'o'):
                    self.cube.rotate('l','cc')
                    self.cube.rotate('b','c')
                    self.cube.rotate('l','c')
    
    def checkBackLeft(self):
        isWhite = True
        #while there is a white face on the back left side layers
        while(isWhite):
            isWhite = False
            if(self.cube.cube[2][2][2] == 'w'):
                #right face left back
                isWhite = True
                #the color on the opposite face
                opColor = self.cube.cube[5][2][2]
                if(opColor == 'g'):
                    #moves white out of way
                    self.cube.rotate('b','c')
                if(opColor == 'b'):
                   #moves white out of the way t 
                    self.cube.rotate('b','cc')
                if(opColor == 'r'):
                    #moves white out of the way then places it 
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')

            if(self.cube.cube[3][0][0] == 'w'):
                #left face left back
                isWhite = True
                #the color on the opposite face
                opColor = self.cube.cube[4][0][0]
                if(opColor == 'g'):
                    #moves white out of way
                    self.cube.rotate('b','cc')
                if(opColor == 'b'):
                   #moves white out of the way 
                    self.cube.rotate('b','c')
                if(opColor == 'o'):
                    #moves white out of the way
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')

            if(self.cube.cube[4][0][2] == 'w'):
                #up face left back
                isWhite = True
                #the color on the opposite face
                opColor = self.cube.cube[2][0][2]
                if(opColor == 'o'):
                    #moves white out of way
                    self.cube.rotate('b','cc')
                if(opColor == 'b'):
                   #moves white out of the way 
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')
                if(opColor == 'r'):
                    #moves white out of the 
                    self.cube.rotate('b','c')

            if(self.cube.cube[5][2][0] == 'w'):
                #down face left back
                isWhite = True
                #the color on the opposite face
                opColor = self.cube.cube[3][2][0]
                if(opColor == 'o'):
                    #moves white out of way
                    self.cube.rotate('b','c')
                if(opColor == 'g'):
                   #moves white out of the way 
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')
                if(opColor == 'r'):
                    #moves white out of the 
                    self.cube.rotate('b','cc')
                    
            #finish Rotation based on opposite color
            if(isWhite == True):
                if(opColor == 'g'):
                    self.cube.rotate('d', 'c')
                    self.cube.rotate('b','cc')
                    self.cube.rotate('d','cc')
        
                if(opColor == 'b'):
                    self.cube.rotate('u','c')
                    self.cube.rotate('b', 'cc')
                    self.cube.rotate('u','cc')
                    
                if(opColor == 'r'):
                    self.cube.rotate('r','c')
                    self.cube.rotate('b','cc')
                    self.cube.rotate('r','cc')
                
                if(opColor == 'o'):
                    self.cube.rotate('l','c')
                    self.cube.rotate('b','cc')
                    self.cube.rotate('l','cc')
            
    def backWhiteCorner(self):
        #checks if there is a white corner still on the yellow side 
        if(self.cube.cube[1][0][0] == 'w'): return True
        if(self.cube.cube[1][0][2] == 'w'): return True
        if(self.cube.cube[1][2][0] == 'w'): return True
        if(self.cube.cube[1][2][2] == 'w'): return True
        return False
        
    def topLeftCorner(self):
        if(self.cube.cube[1][0][0] == 'w'):
            #in the top left corner
            opColor1 = self.cube.cube[4][0][2]
            opColor2 = self.cube.cube[2][0][2]
            if(opColor1 == 'o' and opColor2 == 'g'):
                self.cube.rotate('r','c')
                self.cube.rotate('b','c')
                self.cube.rotate('b', 'c') 
                self.cube.rotate('r','cc')
            if(opColor1 == 'g' and opColor2 == 'r'):
                self.cube.rotate('b','cc')
                self.cube.rotate('d','c')
                self.cube.rotate('b', 'c') 
                self.cube.rotate('b','c')
                self.cube.rotate('d','cc')
            if(opColor1 == 'b' and opColor2 == 'o'):
                self.cube.rotate('b','c')
                self.cube.rotate('l','cc')
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('l','c')
            if(opColor1 == 'r' and opColor2 == 'b'):
                self.cube.rotate('r','c')
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('r','cc')
        
        
    def topRightCorner(self):
        if(self.cube.cube[1][0][2] == 'w'):
            #in the top right corner
            opColor1 = self.cube.cube[4][0][0]
            opColor2 = self.cube.cube[3][0][0]
            if(opColor1 == 'r' and opColor2 == 'g'):
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('d', 'c') 
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('d','cc')
            if(opColor1 == 'b' and opColor2 == 'r'):
                self.cube.rotate('b','cc')
                self.cube.rotate('r','c')
                self.cube.rotate('b', 'c') 
                self.cube.rotate('b','c')
                self.cube.rotate('r','cc')
            if(opColor1 == 'o' and opColor2 == 'b'):
                self.cube.rotate('l','cc')
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('l','c')
            if(opColor1 == 'g' and opColor2 == 'o'):
                self.cube.rotate('b','c')
                self.cube.rotate('l','c')
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('l','cc')
                
    def bottomLeftCorner(self):
        if(self.cube.cube[1][2][0] == 'w'):
            #in the bottom left corner
            opColor1 = self.cube.cube[2][2][2]
            opColor2 = self.cube.cube[5][2][2]
            if(opColor1 == 'r' and opColor2 == 'b'):
               self.cube.rotate('b','c')
               self.cube.rotate('r','c')
               self.cube.rotate('b','c')
               self.cube.rotate('b','c')
               self.cube.rotate('r','cc')
            if(opColor1 == 'b' and opColor2 == 'o'):
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('l','cc')
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('l','c')
            if(opColor1 == 'o' and opColor2 == 'g'):
                self.cube.rotate('b','cc')
                self.cube.rotate('l','c')
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('l','cc')
            if(opColor1 == 'g' and opColor2 == 'r'):
                self.cube.rotate('d', 'c') 
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('d','cc')
            
    def bottomRightCorner(self):
        if(self.cube.cube[1][2][2] == 'w'):
            #in the bottom right corner
            opColor1 = self.cube.cube[3][2][0]
            opColor2 = self.cube.cube[5][2][0]
            if(opColor1 == 'b' and opColor2 == 'r'):
               self.cube.rotate('b','c')
               self.cube.rotate('b','c')
               self.cube.rotate('r','c')
               self.cube.rotate('b','c')
               self.cube.rotate('b','c')
               self.cube.rotate('r','cc')
            if(opColor1 == 'o' and opColor2 == 'b'):
                self.cube.rotate('b','cc')
                self.cube.rotate('l','cc')
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('l','c')
            if(opColor1 == 'g' and opColor2 == 'o'):
                self.cube.rotate('l','c')
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('l','cc')
            if(opColor1 == 'r' and opColor2 == 'g'):
                self.cube.rotate('b', 'c') 
                self.cube.rotate('r','cc')
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.cube.rotate('r','c')
        
    def checkBackLayer(self):
        #checks yellow face for a white corner
        self.topLeftCorner()
        self.topRightCorner()
        self.bottomLeftCorner()
        self.bottomRightCorner()
        #if not completed repeat
        if(self.backWhiteCorner()):
            self.checkBackLayer()
    
    def rightSide(self):
        if(self.cube.cube[2][0][0] == 'w'):
            #right top
            self.cube.rotate('u','cc')
            self.cube.rotate('b','c')
            self.cube.rotate('u','c')
        if(self.cube.cube[2][2][0] == 'w'):
            #right bottom
            self.cube.rotate('d','c')
            self.cube.rotate('b','c')
            self.cube.rotate('d','cc')
        
    def leftSide(self):
        if(self.cube.cube[3][0][2] == 'w'):
            #left top 
            self.cube.rotate('u','c')
            self.cube.rotate('b','c')
            self.cube.rotate('u','cc')
        if(self.cube.cube[3][2][2] == 'w'):
            #left bottom
            self.cube.rotate('d','cc')
            self.cube.rotate('b','c')
            self.cube.rotate('d','c')
        
    def upSide(self):
        if(self.cube.cube[4][2][0] == 'w'):
            #up left
            self.cube.rotate('l','cc')
            self.cube.rotate('b','c')
            self.cube.rotate('l','c')
        if(self.cube.cube[4][2][2] == 'w'):
            #up right  
            self.cube.rotate('r','c')
            self.cube.rotate('b','c')
            self.cube.rotate('r','cc')
        
    def downSide(self):
        if(self.cube.cube[5][0][2] == 'w'):
            #down right
            self.cube.rotate('r','cc')
            self.cube.rotate('b','c')
            self.cube.rotate('r','c')
        if(self.cube.cube[5][0][0] == 'w'):
            #down left  
            self.cube.rotate('l','c')
            self.cube.rotate('b','c')
            self.cube.rotate('l','cc')
    
    def checkFrontSides(self):
        #checks front layer for white corners
        self.rightSide()
        self.leftSide()
        self.upSide()
        self.downSide()
    
    def frontLayerSolved(self):
        #returns false if the front layer is not solved
        for row in range(3):
            for col in range(3):
                if(self.cube.cube[0][row][col] != 'w'):
                    return False
        return True
  
    def solveWhiteCorners(self):
        #solve the white corners
        #checks for white corner in each layer of the cube
        while(not self.backLayer()):
            self.checkBackLeft()
            self.checkBackRight() 
        self.checkBackLayer()
        self.checkFrontSides()
        if(not self.frontLayerSolved()):
            #if not sovled, repeat
            self.solveWhiteCorners()
        
    def backLayer(self):
        #checks if white on the back layer at all
        return (self.cube.cube[2][0][2] != 'w') and (self.cube.cube[2][2][2] != 'w')\
         and (self.cube.cube[3][0][0] != 'w') and (self.cube.cube[3][2][0] != 'w') \
         and(self.cube.cube[4][0][0] != 'w') and (self.cube.cube[4][0][2] != 'w')\
         and(self.cube.cube[5][2][0] != 'w') and (self.cube.cube[5][2][2] != 'w')
        
    def moveRed(self):
            #moves the red edge into place
            if(self.cube.cube[1][1][0] == 'b'):
                self.canMove = True
                self.leftMiddleLayer('b','u','r')
                
            if(self.cube.cube[2][1][2] == 'g'):
                self.canMove = True
                self.rightMiddleLayer('b','d','r')
                
    def moveOrange(self):
        #moves the orange edge into place
        if(self.cube.cube[1][1][2] == 'b'):
            self.canMove = True
            self.rightMiddleLayer('b','u','l') 
        if(self.cube.cube[1][1][2] == 'g'):
            self.canMove = True
            self.leftMiddleLayer('b','d','l')
            
    def moveBlue(self):
        #moves the blue edge into place
        if(self.cube.cube[1][0][1] == 'o'):
            self.canMove = True
            self.leftMiddleLayer('b','l','u')
        if(self.cube.cube[1][0][1] == 'r'):
            self.canMove = True
            self.rightMiddleLayer('b','r','u')
            
    def moveGreen(self):
        #moves the green edge into place
        if(self.cube.cube[1][2][1] == 'r'):
            self.canMove = True
            self.leftMiddleLayer('b','r','d')
        if(self.cube.cube[1][2][1] == 'o'):
            self.canMove = True
            self.rightMiddleLayer('b','l','d')
        
    def rightBackLayer(self):    
        if(self.cube.cube[1][1][0] != 'y'):
            #for the right face
            if(self.cube.cube[2][1][2] == 'r'):
                self.moveRed()
            if(self.cube.cube[2][1][2] == 'b'):
                self.cube.rotate('b','c')
                self.moveBlue()
            if(self.cube.cube[2][1][2] == 'o'):
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.moveOrange()
            if(self.cube.cube[2][1][2] == 'g'):
                self.cube.rotate('b','cc')
                self.moveGreen()
    
    def leftBackLayer(self):
        if(self.cube.cube[1][1][2] != 'y'):
            #for the left face
            if(self.cube.cube[3][1][0] == 'r'):
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.moveRed()
            if(self.cube.cube[3][1][0] == 'b'):
                self.cube.rotate('b', 'cc')
                self.moveBlue()                
            if(self.cube.cube[3][1][0] == 'o'):
                self.moveOrange()                
            if(self.cube.cube[3][1][0] == 'g'):
                self.cube.rotate('b','c')
                self.moveGreen()
        
    def upBackLayer(self):
        if(self.cube.cube[1][0][1] != 'y'):            
            #for the up face 
            if(self.cube.cube[4][0][1] == 'r'):
                self.cube.rotate('b','cc')
                self.moveRed()
            if(self.cube.cube[4][0][1] == 'b'):
                self.moveBlue()                
            if(self.cube.cube[4][0][1] == 'o'):
                self.cube.rotate('b','c')
                self.moveOrange()                
            if(self.cube.cube[4][0][1] == 'g'):
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
                self.moveGreen()
                
    def downBackLayer(self):
        if(self.cube.cube[1][2][1] != 'y'):
            #for the down face
            if(self.cube.cube[5][2][1] == 'r'):
                self.cube.rotate('b','c')
                self.moveRed()                
            if(self.cube.cube[5][2][1] == 'b'):
                self.cube.rotate('b', 'c')
                self.cube.rotate('b', 'c')
                self.moveBlue()                
            if(self.cube.cube[5][2][1] == 'o'):
                self.cube.rotate('b', 'cc')
                self.moveOrange()                
            if(self.cube.cube[5][2][1] == 'g'):
                self.moveGreen()
    
    def moveBackLayer(self):
        #places edges in the correct place
        self.rightBackLayer()
        self.leftBackLayer()
        self.upBackLayer()
        self.downBackLayer()

    def rightMiddleLayer(self, u, r, f):
        #move sequence to move an edge right, into the middle layer
        self.cube.rotate(u,'c')
        self.cube.rotate(r,'c')
        self.cube.rotate(u,'cc')
        self.cube.rotate(r,'cc')
        self.cube.rotate(u,'cc')
        self.cube.rotate(f,'cc')
        self.cube.rotate(u,'c')
        self.cube.rotate(f,'c')
    
    def leftMiddleLayer(self, u, l, f):
        #move sequence to move and edge piece left, into the middle layer
        self.cube.rotate(u,'cc')
        self.cube.rotate(l,'cc')
        self.cube.rotate(u,'c')
        self.cube.rotate(l,'c')
        self.cube.rotate(u,'c')
        self.cube.rotate(f,'c')
        self.cube.rotate(u,'cc')
        self.cube.rotate(f,'cc')
    
    def checkMiddleLayerEdge(self):
        #check for incorrectly placed blocks
        #right side uses left algoritm
        if(self.cube.cube[2][0][1] != 'r'):
            self.leftMiddleLayer('b','u','r')
        if(self.cube.cube[3][2][1] != 'o'):
            self.leftMiddleLayer('b','d','l')
        if(self.cube.cube[4][1][0] != 'b'):
            self.leftMiddleLayer('b','l','u')
        if(self.cube.cube[5][1][2] != 'g'):
            self.leftMiddleLayer('b','r','d')
            
        
        #left side uses right algorithm 
        if(self.cube.cube[2][2][1] != 'r'):
            self.rightMiddleLayer('b','d','r')
        if(self.cube.cube[3][0][1] != 'o'):
            self.rightMiddleLayer('b','u','l')
        if(self.cube.cube[4][1][2] != 'b'):
            self.rightMiddleLayer('b','r','u')
        if(self.cube.cube[5][1][0] != 'g'):
            self.rightMiddleLayer('b','l','d')
    
    def middleLayerSolved(self):
        #returns true if the middle layer is solved
        if(self.cube.cube[2][0][1] != 'r' or self.cube.cube[2][2][1] != 'r'):
            return False
        if(self.cube.cube[3][0][1] != 'o' or self.cube.cube[3][2][1] != 'o'):
            return False
        if(self.cube.cube[4][1][0] != 'b' or self.cube.cube[4][1][2] != 'b'):
            return False
        if(self.cube.cube[5][1][0] != 'g' or self.cube.cube[5][1][2] != 'g'):
            return False 
        return True
    
    def middleLayer(self):
        #solves the middle layer
        self.moveBackLayer()
        #check edge pieces if not solved
        if(not self.middleLayerSolved()):
            self.checkMiddleLayerEdge()
        #repeat if not solved
        if(not self.middleLayerSolved()):
            self.middleLayer()
    
    def yellowEdgeSeq(self):
        #sequence to solve for yellow egdes
        self.cube.rotate('r','c')
        self.cube.rotate('d','c')
        self.cube.rotate('b','c')
        self.cube.rotate('d','cc')
        self.cube.rotate('b','cc')
        self.cube.rotate('r','cc')
        
    def yellowEdgeSolved(self):
        #returns false if the yellow edge is not solved
        for e in range(len(self.edges)):
            row = self.edges[e][0]
            col = self.edges[e][1]
            if(self.cube.cube[1][row][col] != 'y'): return False
        return True
    
    def solveYellowEdge(self):
        #solve the yelow edges dont have to be in the correct orientation
        if(self.cube.cube[1][0][1] != 'y' and self.cube.cube[1][1][0] != 'y' and\
        self.cube.cube[1][1][2] != 'y' and self.cube.cube[1][2][1] != 'y'):
            self.yellowEdgeSeq()
            self.yellowEdgeSeq()
            self.cube.rotate('b','c')
            self.yellowEdgeSeq()
            return
            
        if(self.cube.cube[1][1][0] == 'y' and (self.cube.cube[1][0][1] == 'y' or self.cube.cube[1][2][1] == 'y')):
            if(self.cube.cube[1][0][1] == 'y'):
                self.cube.rotate('b','cc')
            self.yellowEdgeSeq()
            self.cube.rotate('b','c')
            self.yellowEdgeSeq()
            return
        
        if(self.cube.cube[1][1][0] == 'y' and self.cube.cube[1][1][2] == 'y'):
            self.cube.rotate('b','c')
            self.yellowEdgeSeq()
            return
            
        if(self.cube.cube[1][1][2] == 'y' and (self.cube.cube[1][0][1] == 'y' or self.cube.cube[1][2][1] == 'y')):
            if(self.cube.cube[1][0][1] == 'y'):
                self.cube.rotate('b','c')
                self.cube.rotate('b','c')
            elif(self.cube.cube[1][2][1] == 'y'):
                self.cube.rotate('b','c')
                
            self.yellowEdgeSeq()
            self.cube.rotate('b','c')
            self.yellowEdgeSeq()
            return
            
        if(self.cube.cube[1][0][1] == 'y' and self.cube.cube[1][2][1] == 'y'):
            self.yellowEdgeSeq()
            return
        
    def yellowCornersEmpty(self):
       #returns false if there is a yellow edge on the back face
        for c in range(len(self.corners)):
            row = self.edges[c][0]
            col = self.edges[c][1]
            if(self.cube.cube[1][row][col] == 'y'): return False
        return True
    
    def cornersSolved(self):
        #returns false if the yellow corners are not solved
        for c in range(len(self.corners)):
            row = self.corners[c][0]
            col = self.corners[c][1] 
            if(self.cube.cube[1][row][col] != 'y'):return False
        return True
        
    def yellowCornerSeq(self):
        #the sequenced used if the cube is in the correct orientation to change the corners
        self.cube.rotate('d','cc')
        self.cube.rotate('b','c')
        self.cube.rotate('b','c')
        self.cube.rotate('d','c')
        self.cube.rotate('b','c')
        self.cube.rotate('d','cc')
        self.cube.rotate('b','c')
        self.cube.rotate('d','c')
    
    def yellowCornerCase1(self):
        return (self.cube.cube[1][2][0] == 'y') and (self.cube.cube[3][0][0] == 'y')\
         and (self.cube.cube[4][0][2] == 'y') and  (self.cube.cube[5][2][0] == 'y')
     
    def yellowCornerCase2(self):
        return (self.cube.cube[1][2][0] == 'y') and (self.cube.cube[3][0][0] == 'y')\
         and (self.cube.cube[1][0][0] == 'y') and (self.cube.cube[3][2][0] == 'y') 
         
    def yellowCornerCase3(self):
        return (self.cube.cube[2][2][2] == 'y') and (self.cube.cube[3][0][0] == 'y') \
        and (self.cube.cube[2][0][2] == 'y') and (self.cube.cube[3][2][0] == 'y') 
    
    def yellowCornerCase4(self):
        return (self.cube.cube[2][2][2] == 'y') and (self.cube.cube[4][0][0] == 'y')\
         and (self.cube.cube[4][0][2] == 'y') and (self.cube.cube[3][2][0] == 'y') 
    
    def yellowCornerCase5(self):
        return (self.cube.cube[1][0][2] == 'y') and (self.cube.cube[1][2][2] == 'y')\
         and (self.cube.cube[4][0][2] == 'y') and (self.cube.cube[5][2][2] == 'y')
         
    def yellowCornerCase6(self):
        return (self.cube.cube[1][2][0] == 'y') and (self.cube.cube[2][0][2] =='y')\
        and (self.cube.cube[3][2][0] == 'y') and (self.cube.cube[4][0][0] == 'y')
        
    def yellowCornerCase7(self):
        return (self.cube.cube[1][0][0] == 'y') and (self.cube.cube[1][2][2] == 'y')\
        and (self.cube.cube[3][0][0] == 'y') and (self.cube.cube[5][2][2] == 'y')
    
    def checkCase1(self):
        #case 1
        #checks if the cube is in the case 1 orientation
        for i in range(4):
            #rotates back face checking each side for correct orientation 
            if(not self.yellowCornerCase1()):
                self.cube.rotate('b','c')
        #finish these moves to solve the cube
        if(self.yellowCornerCase1()):
            self.yellowCornerSeq()
            return
            
    def checkCase2(self):
        #case 2
        for i in range(4):
            #rotates back checking for case 2 orientation
            if(not self.yellowCornerCase2()):
                self.cube.rotate('b','c')
        if(self.yellowCornerCase2()):
           #finish these moves to solve the yellow corners
            self.cube.rotate('b', 'c')
            self.yellowCornerSeq()
            self.cube.rotate('b','cc')
            self.yellowCornerSeq()
            self.cube.rotate('b','c')
            self.cube.rotate('b','c')
            self.yellowCornerSeq()
            return
            
    def checkCase3(self):
        #case 3
        for i in range(4):
            #rotates back checking for case 3 orientation
            if(not self.yellowCornerCase3()):
                self.cube.rotate('b','c')
        #do these moves if in case 3 orientation
        if(self.yellowCornerCase3()):
            self.yellowCornerSeq()           
            self.yellowCornerSeq()
            return
        
    def checkCase4(self):
        #case 4 
        for i in range(4):
            if(not self.yellowCornerCase4()):
                self.cube.rotate('b','c')
        if(self.yellowCornerCase4()):
            self.yellowCornerSeq()
            self.cube.rotate('b','c')
            self.yellowCornerSeq()
            return
            
    def checkCase5(self):
        #case 5
        for i in range(4):
            if(not self.yellowCornerCase5()):
                self.cube.rotate('b','c')
        if(self.yellowCornerCase5()):
            self.yellowCornerSeq()
            self.cube.rotate('b','c')
            self.yellowCornerSeq()
            self.cube.rotate('b','c')
            self.cube.rotate('b','c')
            self.yellowCornerSeq()
            return
            
    def checkCase6(self):
        #case 6
        for i in range(4):
            if(not self.yellowCornerCase6()):
                self.cube.rotate('b','c')
        if(self.yellowCornerCase6()):
            self.yellowCornerSeq()
            self.cube.rotate('b','c')
            self.cube.rotate('b','c')
            self.yellowCornerSeq()
            return
            
    def checkCase7(self):
        #case 7
        for i in range(4):
            if(not self.yellowCornerCase7()):
                self.cube.rotate('b','c')
        if(self.yellowCornerCase7()):
            self.yellowCornerSeq()
            self.yellowCornerSeq()
            self.cube.rotate('b','c')
            self.cube.rotate('b','c')
            self.yellowCornerSeq()
           
    def solveYellowCorner(self):
        #checks the different cases for the yellow corners
        self.checkCase1()
        self.checkCase2()
        self.checkCase3()
        self.checkCase4()
        self.checkCase5()
        self.checkCase6()
        self.checkCase7()
        
    def fixYellowCornerSeq(self):
        #the sequence used to fix the yellow corners
        self.cube.rotate('d','cc')
        self.cube.rotate('r','c')
        self.cube.rotate('d','cc')
        self.cube.rotate('l','c')
        self.cube.rotate('l','c')
        self.cube.rotate('d','c')
        self.cube.rotate('r','cc')
        self.cube.rotate('d','cc')
        self.cube.rotate('l','c')
        self.cube.rotate('l','c')
        self.cube.rotate('d','c')
        self.cube.rotate('d','c')

    def correctBottomCorners(self):
        #returns true if the corners are correct
        if(self.cube.cube[2][0][2] == 'r' and self.cube.cube[2][2][2] == 'r'):
            return True
        return False
    
    def fixYellowCorners(self):
        #re oirents the yellow corners
        color = ['r','o','b','g']
        headLights = False
        #checks for 'headlights' on the cube, two corners with the same color
        for c in range(len(color)):
            for i in range(4):
                if(self.cube.cube[2][0][2] == color[c] and self.cube.cube[2][2][2] == color[c]):
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')
                    headLights = True
                self.cube.rotate('b','c')
        #if no headlights, do sequence
        if(headLights == False): self.fixYellowCornerSeq()
        #checks using each color
        for c in range(len(color)):
            for i in range(4):
                self.cube.rotate('b','c')
                if(self.cube.cube[2][0][2] == color[c] and self.cube.cube[2][2][2] == color[c]):
                    self.cube.rotate('b','c')
                    self.cube.rotate('b','c')
                    break
        #does sequence again
        self.fixYellowCornerSeq()
        for i in range(4):
            #puts cube in correct orientation
            if(not self.correctBottomCorners()):
                self.cube.rotate('b','c')
        if(not self.correctYellowCorner()):
            self.fixYellowCorners()
            
    def correctYellowCorner(self):
        return (self.cube.cube[2][0][2] == 'r') and (self.cube.cube[2][2][2] == 'r')\
         and (self.cube.cube[3][0][0] == 'o') and (self.cube.cube[3][2][0] == 'o') \
         and (self.cube.cube[4][0][0] == 'b') and (self.cube.cube[4][0][2] == 'b')\
         and (self.cube.cube[5][2][0] == 'g') and (self.cube.cube[5][2][2] == 'g')
                
    def permuteEdgeSeq(self, r = 'r', u = 'b'):
        #the sequence used to permute the edges of the cube
        self.cube.rotate(r, 'c')
        self.cube.rotate(u, 'cc')
        self.cube.rotate(r, 'c')
        self.cube.rotate(u, 'c')
        self.cube.rotate(r, 'c')
        self.cube.rotate(u, 'c')
        self.cube.rotate(r, 'c')
        self.cube.rotate(u, 'cc')
        self.cube.rotate(r, 'cc')
        self.cube.rotate(u, 'cc')
        self.cube.rotate(r, 'c')
        self.cube.rotate(r, 'c')
    
    def oneEdgeSolved(self):
        #if one edge is solved, return the color
        if(self.cube.cube[2][1][2] == 'r'):
            return 'r'
        if(self.cube.cube[4][0][1] == 'b'):
            return 'u'
        if(self.cube.cube[3][1][0] == 'o'):
            return 'l'
        if(self.cube.cube[5][2][1] == 'g'):
            return 'd'
        else: return None
            
    def permuteYellowEdge(self):
        
        #gets if there is a side solved already
        solvedSide = self.oneEdgeSolved()
        if(solvedSide == 'r'):
            while(self.cube.cube != self.cube.completedCube):
                self.permuteEdgeSeq('u','b')
        if(solvedSide == 'l'):
            while(self.cube.cube != self.cube.completedCube):
                self.permuteEdgeSeq('d','b')

        if(solvedSide == 'u'):
            while(self.cube.cube != self.cube.completedCube):
                self.permuteEdgeSeq('l','b')
        if(solvedSide == 'd'):
            while(self.cube.cube != self.cube.completedCube):
                self.permuteEdgeSeq('r','b')
                
        #if there isnt a side that is solved
        if(solvedSide == None):
            self.permuteEdgeSeq()
            self.permuteYellowEdge()
            
    def displayMoves(self):
        #checks for redundant moves and changes them
        stringMoves = ' '.join(self.cube.moveSeq)
        stringMoves += ' '
        badMoves = ["F F' ", "B B' ","R R' ", "L L' ", "U U' ", "D D' ",\
         "F' F ", "B' B ","R' R ", "L' L ", "U' U ", "D' D "]
        for move in range(len(self.cube.possibleMoves)):
            char = self.cube.possibleMoves[move]
            char += ' '
            redunMove = char*4
            doubleMove = char*2
            tripleMove = char*3
            if("'" in doubleMove):
                char =  char.replace("'",'')
            if(redunMove in stringMoves):
                stringMoves = stringMoves.replace(redunMove, '')                
            if(tripleMove in stringMoves):
                if(len(char) == 2):
                    char = char.replace(' ', "' ")                    
                elif(len(char) == 3):
                    char = char.replace("' ", ' ')
                stringMoves = stringMoves.replace(tripleMove, char)
            if(doubleMove in stringMoves):
                char = char.replace(' ','2 ')
                stringMoves = stringMoves.replace(doubleMove, char)
        for move in range(len(badMoves)):
            redunMove = badMoves[move]
            if(redunMove in stringMoves):
                stringMoves = stringMoves.replace(redunMove, '')

        self.cube.moveSeq = stringMoves.split(' ')
        self.cube.moveSeq.pop()
        print(stringMoves)
    
###########
#Main
###########

def main():
    runSolver = SolveCube()

if __name__ == '__main__':
    main()
