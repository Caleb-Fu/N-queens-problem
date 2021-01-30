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

#set up threatened value diagnolly.
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
        print("This position placed by another Queen!")
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

def printBoard(board): #print out the board with Queen position and each gird with its threatened value.
    size = range(len(board))
    for i in size:
        for j in size:
            if j == len(board)-1:
                if board[i][j].hasQ == True:
                    print("Q")
                else:
                    print(board[i][j].threatened)
            else:
                if board[i][j].hasQ == True:
                    print("Q", end=" | ")
                else:
                    print(board[i][j].threatened, end=" | ")



if __name__=="__main__":
    new = board(8)
    placeQ(1, 2, new)
    printBoard(new)
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

