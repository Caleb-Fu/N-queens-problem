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
        return -1
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

'''
sets up board to have all queens in their own row but share the column.
This was better than the greedy start because it forces errors early and prevents
getting stuck on a local maximum
'''
def initialState1(board_size):

    new = board(board_size)
    for row in range(board_size):
        placeQ(row, 0, new)

    return new
        

def initialState2(board_size):

    new = board(board_size)
    rowLis = list(range(0, board_size))
    colLis = list(range(0, board_size))
    random.shuffle(rowLis)
    random.shuffle(colLis)
    for i in range(board_size):
        placeQ(rowLis[i], colLis[i], new)

    return new
    

def iterativeRepair(board):
    step = 0
    size = len(board)
    while True:
        maxConflict = 0 #this keeps track of the maximum number of "threats"
        minConflict = size #this keeps track of the minimum number of threats

        dictMax = {} #stores the row and column of the space with the most number of threats, requires multiple entries if there is a tie
        for row in range(size):
            for col in range(size):
                if board[row][col].hasQ and board[row][col].threatened > maxConflict:
                    maxConflict = board[row][col].threatened
                    dictMax.clear() #resets dictionary since it is outdated
                    dictMax[row] = col #puts updated row and column information for space with most conflicts
                elif board[row][col].hasQ and board[row][col].threatened == maxConflict:
                    dictMax[row] = col

        if maxConflict == 1: #this means the algorithm is complete
            print("Step:", step)
            return board

        lisMin = [] #stores the column containing the space with the least number of threats, in the row with the most number of threats
        maxConflictRow = random.choice(list(dictMax)) #according to the algorithm, need to randomly choose the row if there is a tie
        for col in range(size):
            if board[maxConflictRow][col].threatened < minConflict: #finds the column containing the space with the min number of threats
                minConflict = board[maxConflictRow][col].threatened
                minConflictCol = col
                lisMin.clear()
                lisMin.append(col)
            elif board[maxConflictRow][col].threatened == minConflict:
                lisMin.append(col)
                
        removeQ(maxConflictRow, dictMax[maxConflictRow], board) #removes queen from threatened postion
        placeQ(maxConflictRow, random.choice(lisMin), board) #puts queen in least threatened position, randomly selects colomn if there is a tie
        step += 1

    
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


# Implement a solver that returns a list of queen's locations
#  - Make sure the list is the right length, and uses the numbers from 0 .. BOARD_SIZE-1
def solve(board_size):
    
    board = initialState1(board_size)
    solvedBoard = iterativeRepair(board)
    #printBoard(solvedBoard)

    answer = []
    for row in range(board_size):
        for col in range(board_size):
            if solvedBoard[row][col].hasQ:
                answer.append(col+1)
    return answer

if __name__=="__main__":
    print(solve(8))
