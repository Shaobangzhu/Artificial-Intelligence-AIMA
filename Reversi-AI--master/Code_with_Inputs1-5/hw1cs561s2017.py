# CSCI-561 2017S Homework1
# Student Name: Chaoran Lu
# Student ID: 6524-2400-52
# Email: luchaora@usc.edu
# References:
# 1. InventWithPython Chapter 15 Reversi
#   URL:https://inventwithpython.com/chapter15.html
# 2. Python + Pygame published 2012:
#   Ideas of three functions come from this example:
#           "def isOnBoard(x, y):",
#           "def isValidMove(board, tile, xstart, ystart):"
#           "def getValidMoves(board, tile):"
#   URL:http://blog.csdn.net/guzhou_diaoke/article/details/8201542

import os

# This global variable is used to store the data of "Positional Weights" for Evaluation Function
posW = [
        [99, -8, 8, 6, 6, 8, -8, 99],
        [-8, -24, -4, -3, -3, -4, -24, -8],
        [8, -4, 7, 4, 4, 7, -4, 8],
        [6, -3, 4, 0, 0, 4, -3, 6],
        [6, -3, 4, 0, 0, 4, -3, 6],
        [8, -4, 7, 4, 4, 7, -4, 8],
        [-8, -24, -4, -3, -3, -4, -24, -8],
        [99, -8, 8, 6, 6, 8, -8, 99],
]

# This global variable is used to record the alpha-beta pruning process
myRecord = []

# This global variable is to record current root value
curRootVal = float("-infinity")

# This global variable is to record the next move position
nextMove = ''


# function ALPHA-BETA-SEARCH(state)
def lcrPlay(curplayer, depth, initMatrix):
    # variables of current state
    alphaInit = float("-infinity")
    betaInit = float("infinity")
    totalDepth = depth
    tile = curplayer

    lcrResult = alphaBetaMax('root', tile, initMatrix, 0, alphaInit, betaInit, totalDepth, 0)
#    print('root', 0, lcrResult[0], lcrResult[1], lcrResult[2])


# function MAX-VALUE(state, a, b) returns a utility value
def alphaBetaMax(node, tile, curMatrix, curDepth, a, b, totalDepth, passCount):
    global curRootVal
    global nextMove
#    printB(curMatrix)
    vlcr = float("-infinity")
    originalA = a

    if tile == "X":
        othertile = "O"
    else:
        othertile = "X"

    # Get a list of valid position from the current board
    branch = getValidMoves(curMatrix, tile)
    # Terminal Test 1
    if len(branch) == 0 and curDepth != totalDepth:
        lcrResult = [vlcr, a, b]
        if passCount == 2:
#            print getWeights(curMatrix)
            lcrResult = [getWeights(curMatrix), a, b]
#            print([node, curDepth, lcrResult[0], a, b])
            myRecord.append([node, curDepth, lcrResult[0], a, b])
            return lcrResult
        passCount = passCount + 1
        myRecord.append([node, curDepth, lcrResult[0], a, b])
#        print([node, curDepth, lcrResult[0], a, b])
        curBoard1 = boardClone(curMatrix)
        tmpTerminal = alphaBetaMin('pass', othertile, curBoard1, curDepth + 1, a, b, totalDepth, passCount)
        vlcr = max(vlcr, tmpTerminal[0])
        a = max(a, vlcr)
        if a < b:
            originalA = a
        if b <= a:
            a = originalA
        myRecord.append([node, curDepth, vlcr, a, b])
#        print([node, curDepth, vlcr, a, b])
        return tmpTerminal

    # Terminal Test 2 (Base case)
    if curDepth == totalDepth:
#        print getWeights(curMatrix)
        lcrResult = [getWeights(curMatrix), a, b]
#        print([node, curDepth, lcrResult[0], a, b])
        myRecord.append([node, curDepth, lcrResult[0], a, b])
        return lcrResult

    # Recursive rule
    for num in range(0, len(branch)):
        curBoard1 = boardClone(curMatrix)
        if (curDepth != totalDepth):
#            print([node, curDepth, vlcr, a, b])
            myRecord.append([node, curDepth, vlcr, a, b])
        cordinateX = branch[num][0]
        cordinateY = branch[num][1]
        curBoard2 = flipTiles(curBoard1, tile, cordinateX, cordinateY)
        # printB(curBoard)
        childNode = getNodeIndex(cordinateX, cordinateY)
        tmp1 = alphaBetaMin(childNode, othertile, curBoard2, curDepth + 1, a, b, totalDepth, passCount)
        vlcr = max(vlcr, tmp1[0])
        # print([node, curDepth, vlcr, a, b])
        a = max(a, vlcr)
        if node == 'root':
            if curRootVal != vlcr:
                curRootVal = vlcr
                nextMove = childNode
                # print(nextMove[0])
        if a < b:
            originalA = a
        if b <= a:
            break

    if b <= a:
        a =originalA
#    print([node, curDepth, vlcr, a, b])
    myRecord.append([node, curDepth, vlcr, a, b])
    lcrResult = [vlcr, a, b]
    return lcrResult


# function MIN-VALUE(state, a, b) returns a utility value
def alphaBetaMin(node, tile, curMatrix, curDepth, a, b, totalDepth, passCount):
    global curRootVal
    global nextMove
#    printB(curMatrix)
    vlcr = float("infinity")
    originalB = b

    if tile == "X":
        othertile = "O"
    else:
        othertile = "X"

    # Get a list of valid position from the current board
    branch = getValidMoves(curMatrix, tile)

    # Terminal Test 1
    if len(branch) == 0 and curDepth != totalDepth:
        lcrResult = [vlcr, a, b]
        if passCount == 2:
#            print getWeights(curMatrix)
            lcrResult = [getWeights(curMatrix), a, b]
#            print([node, curDepth, lcrResult[0], a, b])
            myRecord.append([node, curDepth, lcrResult[0], a, b])
            return lcrResult
        passCount = passCount + 1
        myRecord.append([node, curDepth, lcrResult[0], a, b])
#        print([node, curDepth, lcrResult[0], a, b])
        curBoard1 = boardClone(curMatrix)
        tmpTerminal = alphaBetaMax('pass', othertile, curBoard1, curDepth + 1, a, b, totalDepth, passCount)
        vlcr = min(vlcr, tmpTerminal[0])
        b = min(b, vlcr)
        if a < b:
            originalB = b
        if a >= b:
            b = originalB
        myRecord.append([node, curDepth, vlcr, a, b])
#        print([node, curDepth, vlcr, a, b])
        return tmpTerminal

    # Terminal Test 2
    if curDepth == totalDepth:
#        print getWeights(curMatrix)
        lcrResult = [getWeights(curMatrix), a, b]
#        print([node, curDepth, lcrResult[0], a, b])
        myRecord.append([node, curDepth, lcrResult[0], a, b])
        return lcrResult

    # Recursive rule
    for num in range(0, len(branch)):
        curBoard1 = boardClone(curMatrix)
        if (curDepth != totalDepth):
#            print([node, curDepth, vlcr, a, b])
            myRecord.append([node, curDepth, vlcr, a, b])
        cordinateX = branch[num][0]
        cordinateY = branch[num][1]
        curBoard3 = flipTiles(curBoard1, tile, cordinateX, cordinateY)
        # printB(curBoard)
        childNode = getNodeIndex(cordinateX, cordinateY)
        tmp2 = alphaBetaMax(childNode, othertile, curBoard3, curDepth + 1, a, b, totalDepth, passCount)
        vlcr = min(vlcr, tmp2[0])
        b = min(b, vlcr)
        if node == 'root':
            if curRootVal != vlcr:
                curRootVal = vlcr
                nextMove = childNode
        if a < b:
            originalB = b
        if b <= a:
            break

    if b <= a:
        b = originalB
#    print([node, curDepth, vlcr, a, b])
    myRecord.append([node, curDepth, vlcr, a, b])
    lcrResult = [vlcr, a, b]
    return lcrResult

# Determine if the tile is within the reversi board
def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <= 7

# Determine if this is a valid move
def isValidMove(board, tile, xstart, ystart):

    # If there has been a tile in this position, return false
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != '*':
        return False

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    # Tiles to be flipped
    tilesToFlip = []

    # Checking Each of the Eight Directions
    for xdirection, ydirection in [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection

        if not isOnBoard(x, y):
            continue
        if board[x][y] == '*':
            continue
        # Keep moving until out of board or reached a position that is not the other tile
        while board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                break
        # If out of bound, then no tile needs to be flipped
        if not isOnBoard(x, y):
            continue
        if board[x][y] == '*':
            continue
        # If the tile is the same kind
        if board[x][y] == tile:
            while True:
                x -= xdirection
                y -= ydirection
                # break when we reached the starting point
                if x == xstart and y == ystart:
                    break
                # Add the valid move
                tilesToFlip.append([x, y])

    # If there were no tile to be flipped, return false
    if len(tilesToFlip) == 0:
        return False

    return True

# Acquire the valid positions
def getValidMoves(board, tile):
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

# Flip all the opposite tiles in between
def flipTiles(board, tile, xstart, ystart):
    # Put the tile onto this designated position
    board[xstart][ystart] = tile

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    # Checking Each of the Eight Directions
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if not isOnBoard(x, y):
            continue
        if board[x][y] == '*':
            continue
        # Keep moving until out of board or reached a position that is not the other tile
        while board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                break
        # If out of bound, then no tile needs to be flipped
        if not isOnBoard(x, y):
            continue
        if board[x][y] == '*':
            continue
        # If the tile is the same kind
        if board[x][y] == tile:
            while True:
                x -= xdirection
                y -= ydirection
                board[x][y] = tile
                # break when we reached the starting point
                if x == xstart and y == ystart:
                    break
    return board

# Determine the weight of the leaf nodes by counting the tiles.
def getWeights(matrix):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if matrix[x][y] == 'X':
                xscore += posW[x][y]
            if matrix[x][y] == 'O':
                oscore += posW[x][y]
    weight = xscore - oscore
    return weight

# Print current board for Debug usage
def printB(matrix):
    for i in range(8):
        print matrix[i]\

# Get the index: letter-number of each position
def getNodeIndex(x, y):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    nodeIndex = letters[y] + '%d'%(x + 1)
    return nodeIndex

# Clone a board to make another copy
def boardClone(board):
    tmp = [
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
    ]
    for x in range(8):
        for y in range(8):
                tmp[x][y] = board[x][y]
    return tmp

# Get the coordiates from a given node index
def getCoord(node):
    myDict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    coord = [0, 0]
    coord[0] = int(node[1]) - 1
    coord[1] = myDict[node[0]]
    return coord


def main():

    # 2D Array to record the game progress
    matrix = [
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
    ]

    originalBoard = [
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
    ]

    # for i in range(100):
    # This line of code is used to read the input.txt
    infile = open('input.txt', 'r')

    # read the input file and put it into a list, each element is a string
    tmp = infile.readlines()
    curplayer = tmp[0][0]
    depth = int(tmp[1])

    for i in range(2, 10):
        lcrStr = tmp[i]
        for j in range(0, 8):
            matrix[i - 2][j] = lcrStr[j]
            originalBoard[i - 2][j] = lcrStr[j]

    lcrPlay(curplayer, depth, matrix)

#    print('')
#    print('')
#    print('-------------------------------------')
    tmpBoard = originalBoard
    if nextMove == '':
        tmpBoard = originalBoard
#       printB(tmpBoard)
    else:
        coord1 = getCoord(nextMove)
        xMove = coord1[0]
        yMove = coord1[1]
        tmpBoard = flipTiles(originalBoard, curplayer, xMove, yMove)
#        printB(tmpBoard)

#    print(['Node', 'Depth', 'Value', 'Alpha', 'Beta'])
#    for k in range(0, len(myRecord)):
#        print myRecord[k]\

    finalResult = ''
    # Transfer the content of tmpBoard and myRecord to a string variable
    for i1 in range(0, 8):
        for j1 in range(0, 8):
            if finalResult == '':
                finalResult = tmpBoard[i1][j1]
            else:
                finalResult = finalResult + tmpBoard[i1][j1]
        finalResult = finalResult + '\n'

    finalResult = finalResult + 'Node,Depth,Value,Alpha,Beta' + '\n'
    for i2 in range(0, len(myRecord)):
        varlcr = str(myRecord[i2][2])
        if varlcr == 'inf':
            varlcr = 'Infinity'
        if varlcr == '-inf':
            varlcr = '-Infinity'
        alphalcr = str(myRecord[i2][3])
        if alphalcr == 'inf':
            alphalcr = 'Infinity'
        if alphalcr == '-inf':
            alphalcr = '-Infinity'
        betalcr = str(myRecord[i2][4])
        if betalcr == 'inf':
            betalcr = 'Infinity'
        if betalcr == '-inf':
            betalcr = '-Infinity'

        strRecord = str(myRecord[i2][0]) + ',' + str(myRecord[i2][1]) + ',' + varlcr + ',' + alphalcr + ',' + betalcr
        finalResult = finalResult + strRecord + '\n'
    # This line of code is used to create the output.txt
    outfile = open('output.txt', 'w')
    outfile.write(finalResult)
    # for i in range(100):
    #     print i
    #     os.popen('cp input%s.txt input.txt' % i)
    #     os.popen('python h.py')
    #     os.popen('mv input.txt input%s.txt' % i)
    #     os.popen('mv output.txt output%s.txt' % i)

    # for i in range(100):
    #     print("--Test Case #{0}--".format(i))
    #     os.system('cp ./input{0}.txt input.txt'.format(i))
    #     os.system('time ./hw1cs561s2017.py')
    #     print("")
    #     os.system('diff ./output.txt output{0}.txt'.format(i))
    #
    # os.system('rm input.txt output.txt')

if __name__ == "__main__": main()