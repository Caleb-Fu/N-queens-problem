class gird(object):
    def __init__(self):
        self.hasQ = False
        self.threatened = 0

def board(size):
    board=[]
    for i in range(size):
        row=[]
        for j in range(size):
            row.append(gird())
        board.append(row)
    return board

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

def placeQ(row, col, board):
    pos = board[row][col]
    if pos.hasQ == True:
        print("This position placed by another Queen!")
    else:
        pos.hasQ = True
        for g in board[row]:
            g.threatened += 1
        for i in range(len(board)):
            board[i][col].threatened += 1
        setLeftUp(row, col, board)
        setLeftDown(row, col, board)
        setRightUp(row, col, board)
        setRightDown(row, col, board)
        pos.threatened -= 1

def printBoard(board):
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
    placeQ(6,6,new)
    printBoard(new)

