import random

class grid(object): #initialize each grid
    def __init__(self):
        self.hasQ = False # whether Queen is on this grid.
        self.threatened = 0 # threatened value.
        
def board(size): #create a new board and accept input representing length (AxA)
    board=[]
    for i in range(size):
        row=[]
        for j in range(size):
            row.append(grid()) #each grid has two attributes.
        board.append(row)
    return board

#set up threatened value diagonally.
def setLeftUp(row, col, board):
    if (row-1 >= 0)and (col-1 >= 0):
        board[row-1][col-1].threatened += 1
        setLeftUp(row-1, col-1, board)
        
def setLeftDown(row, col, board):
    if (row+1 <= len(board)-1) and (col-1 >= 0):
        board[row+1][col-1].threatened += 1
        setLeftDown(row+1, col-1, board)
        
def setRightUp(row, col, board):
     if (row-1 >= 0) and (col+1 <= len(board)-1):
        board[row-1][col+1].threatened += 1
        setRightUp(row-1, col+1, board)

def setRightDown(row, col, board):
    if (row+1 <= len(board)-1) and (col+1 <= len(board)-1):
        board[row+1][col+1].threatened += 1
        setRightDown(row+1, col+1, board)

def placeQ(row, col, board): #place Queen on the board by given specific row and column.
    pos = board[row][col]
    if pos.hasQ == True: # already take placed by another Queen.
        print("This position already has a Queen!")
    else:
        pos.hasQ = True
        for g in board[row]: #set threatened value for whole row.
            g.threatened += 1
        for i in range(len(board)): #threatened value for whole column.
            board[i][col].threatened += 1
        #set diagnolly.
        setLeftUp(row, col, board)
        setLeftDown(row, col, board)
        setRightUp(row, col, board)
        setRightDown(row, col, board)
        pos.threatened -= 1 #minus the extra threaten value.

#remove threatened value diagonally.
def removeLeftUp(row, col, board):
    if (row-1 >= 0)and (col-1 >= 0):
        board[row-1][col-1].threatened -= 1
        removeLeftUp(row-1, col-1, board)
        
def removeLeftDown(row, col, board):
    if (row+1 <= len(board)-1) and (col-1 >= 0):
        board[row+1][col-1].threatened -= 1
        removeLeftDown(row+1, col-1, board)
        
def removeRightUp(row, col, board):
     if (row-1 >= 0) and (col+1 <= len(board)-1):
        board[row-1][col+1].threatened -= 1
        removeRightUp(row-1, col+1, board)

def removeRightDown(row, col, board):
    if (row+1 <= len(board)-1) and (col+1 <= len(board)-1):
        board[row+1][col+1].threatened -= 1
        removeRightDown(row+1, col+1, board)
        
def removeQ(row, col, board):#remove Queen on the board by given specific row and column.
    pos = board[row][col]
    if pos.hasQ == False:
        print("This position doesn't have a Queen to remove!")
    else:
        pos.hasQ = False
        for g in board[row]: #set threatened value for whole row.
            g.threatened -= 1
        for i in range(len(board)): #threatened value for whole column.
            board[i][col].threatened -=1

        #set diagnolly.
        removeLeftUp(row, col, board)
        removeLeftDown(row, col, board)
        removeRightUp(row, col, board)
        removeRightDown(row, col, board)
        pos.threatened += 1 #add the extra threatened value. 

#sets up board to have all queens in their own row, greedy start attempts to produce least number of conflicts
def greedyStart(board_size):
    new = board(board_size)

    size = range(len(new))
    for i in size:
        minConflict = board_size
        minIndex = board_size
        for j in size:
            if new[i][j].threatened < minConflict:
                minConflict = new[i][j].threatened
                minIndex = j
        
        placeQ(i, minIndex, new)

    solvedBoard = iterativeRepair(new)
    printBoard(solvedBoard)
    
def iterativeRepair(board):
    return board        
    
def printBoard(board): #print out the board with Queen position and each gird with its threatened value.
    size = range(len(board))
    for i in size:
        for j in size:
            if j == len(board)-1:
                if board[i][j].hasQ == True:
                    print(['Q', board[i][j].threatened])
                else:
                    print("   ", board[i][j].threatened)
            else:
                if board[i][j].hasQ == True:
                    print(['Q', board[i][j].threatened], end="|")
                else:
                    print("   ", board[i][j].threatened, end="   |")


if __name__=="__main__":
    greedyStart(10)
    '''
    1 | 1 | 1 | 1 | 0 | 0 | 1 | 0
    1 | 2 | Q | 1 | 1 | 1 | 2 | 1
    0 | 1 | 2 | 1 | 0 | 0 | 1 | 0
    1 | 0 | 1 | 1 | 1 | 0 | 1 | 0
    0 | 0 | 1 | 0 | 1 | 1 | 1 | 0
    0 | 0 | 1 | 0 | 0 | 1 | 2 | 1
    1 | 1 | 2 | 1 | 1 | 1 | Q | 2
    0 | 0 | 1 | 0 | 0 | 1 | 1 | 1
    '''

