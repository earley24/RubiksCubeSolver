#written by Cambrea Earley
#AndrewID: cne
#Section B

#################################################
#program checks legality of entered cube
#################################################

# w = white
# y = yellow
# r = red
# o = orange
# b = blue 
# g = green 

def legalColor(cube):
    #makes sure that the user inputs a cube that is a legal color scheme
    colorD = {'w':0, 'y':0, 'r':0, 'o':0, 'b':0, 'g':0}
    #counts number of each color on cube
    for face in range(len(cube)):
        for row in range(len(cube[0])):
            for col in range(len(cube[0])):
                c = cube[face][row][col] 
                colorD[c] += 1
    #all color counts should be 9
    for val in colorD:
        if(colorD[val] != 9):
            return False
            
    return True
            
###########
#Test Cases
###########
def validCube():
    cube = [ #front face 
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
            #top face
            [['b','b','b'],
            ['b','b','b'],
            ['b','b','b']],
            #bottom/down face
            [['g','g','g'],
            ['g','g','g'],
            ['g','g','g']]
                        ]
    return cube
    
def invalidCube():
    cube = [ #front face 
            [['w','w','w'],
            ['w','w','w'],
            ['w','w','w']],
            #back face
            [['y','y','y'],
            ['y','y','y'],
            ['y','y','y']],
            #right face
            [['w','w','r'],
            ['r','r','r'],
            ['r','r','r']],
            #left face
            [['o','o','o'],
            ['o','o','o'],
            ['o','o','o']],
            #top face
            [['b','b','b'],
            ['b','b','b'],
            ['b','b','y']],
            #bottom/down face
            [['g','g','g'],
            ['g','g','g'],
            ['g','g','g']]
                        ]
    return cube
    
def testLegalColor():
    print('testing legalColor()...')
    c = validCube()
    assert(legalColor(c) == True)
    c = invalidCube()
    assert(legalColor(c) == False)
    
    print('passed')
    
###########
#testAll and Main
###########

def testAll():
   testLegalColor()

def main():
    testAll()

if __name__ == '__main__':
    main()
