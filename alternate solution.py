'''
This program is going to use the iterative repair algorithm to solve the N-queens problem.
Editors: Zhiwei Fu (20111271)
            Tina Gu (20060423)
            Aimee Fu (20067949)
            Carolyn Moore (20103046)
Date: 2020-02-10
'''


import random


def initialState(board_size, flag):
    '''
    Set up the initial state. If the size of board equals to 6n+8, initial state will be [odd+even]
    if the size of board equals to 6n+9, initial state will be [board_size, odd+even]; else, [even+odd]
    Input:  - an integer representing size of board and number of queens in board.
                - an integer representing the status of initial state.
    Ouput: - a list containing the colume postions of queens.
    '''
    qLis = list(range(1, board_size+1)) #use 1, not 0, representing the first colume.
    if flag == 1:
        qLis = qLis[::2] + qLis[1::2] #[odd]+[even]
    elif flag == 2:
        qLis = [qLis[board_size-1]] + qLis[:board_size-1:2] + qLis[1:board_size-1:2]
    else:
         qLis = qLis[1::2] + qLis[::2]

    return qLis


def calcRowScore(qLis):
    '''
    Calculates the "score" of each row, which is the number of queens in that row.
    The score for each row is stored in a 1D list sized n.
    Input:   - a 1D list representing queens' positions.
    Output - a 1D list, where the index represents the row and the value is the number
                  of queens found in that row. Again, note that index 0 represents row 1.
    '''
    qSize = len(qLis)
    qRow = [0] * qSize #initializes list to zeroes
    for i in range(1, qSize+1): 
        position = qLis[i-1] - 1 #get value from each index of the list of queens positions (represents the row)
        qRow[position] += 1 #increases count of queens at the specified row
        
    return qRow


def calcDiag1Score(qLis):
    '''
    Calculates the "score" of each top-left to bottom-right diagonal, which is the number
    of queens in that diagonal. The score for each diagonal is stored in a 1D list sized (2n-1)
    Input:   - a 1D list representing queens' positions.
    Output: - a 1D list, where the index represents the diagonal (starting bottom left corner)
                  and the value is the number of queens found in that diagonal. Again, note that
                  index 0 represents row 1.
    '''
    qSize = len(qLis)
    qDiag1 = [0] * (2*qSize - 1) #2n-1 diagonals on a board
    for i in range(1, qSize+1):
        position = qSize - qLis[i-1] + i - 1 #get the diagonal position of the current queen
        qDiag1[position] += 1

    return qDiag1


def calcDiag2Score(qLis):
    '''
    Calculates the "score" of each bottom-left to top-right diagonal, which is the number
    of queens in that diagonal. The score for each diagonal is stored in a 1D list sized (2n-1)
    Input:   - a 1D list representing queens' positions.
    Ouput:  - a 1D list, where the index represents the diagonal (starting top-left corner)
              and the value is the number of queens found in that diagonal. Again, note that
              index 0 represents row 1.
    '''
    qSize = len(qLis)
    qDiag2 = [0] * (2*qSize - 1) 
    for i in range(1, qSize+1):
        position = qLis[i-1] + i - 2 #get the diagonal position of the current queen
        qDiag2[position] += 1

    return qDiag2


def calcThreatSum(qLis, qRow, qDiag1, qDiag2):
    '''
    Calculates the total number of threats for each queen on the board. Sums the threats in
    the row with the threats on the fist diagonal with the threats on the second diagonal.
    The total sum is stored in a 1D list sized n.
    Inputs:  - a 1D list representing number of queens on each colume.
                 - a 1D list representing number of queens on each row.
                 - a 1D list representing number of queens in the first diagonal.
                 - a 1D list representing number of queens on the second diagonal.
    Ouput:  - a 1D list, where the index represents the diagonal (starting top-left corner)
                   and the value is the number of queens found in that diagonal. Again, note that
                   index 0 represents row 1.
    '''
    qSize = len(qLis)
    qThreatSums = [0] * qSize
    for i in range(1, qSize+1):
        rowThreat = qRow[qLis[i-1]-1]
        diag1Threat = qDiag1[qSize - qLis[i-1] + i - 1]
        diag2Threat = qDiag2[qLis[i-1] + i - 2]

        #need to subtract 2 so the threat of the queen isn't duplicated
        qThreatSums[i-1] = rowThreat + diag1Threat + diag2Threat - 2 

    return qThreatSums


def findMostThreatened(qThreatSums):
    '''
    Iterates through the list of the threats against each queen and finds the most
    threatened (highest value). The index of the highest value is stored in a list.
    If there are multiple queens with the highest number of threats, one is seected
    randomly.
    Input:      - a 1D list representing total number of threats (on row, colume, and
                      diagonals) for each queen. 
    Output:   - int representing the index of the most threatened queen.
    '''
    qMax = 0
    qMaxTracker = []
    
    for i in range(1, len(qThreatSums)+1):
        if qThreatSums[i-1] > qMax:
            qMax = qThreatSums[i-1]
            qMaxTracker.clear() #clear old list since that was for a smaller number of threats
            qMaxTracker.append(i) #append index of the queen with the most threats
        elif qThreatSums[i-1] == qMax:
            qMaxTracker.append(i)
    qThreatenedIndex = random.choice(qMaxTracker)
            
    return qThreatenedIndex



def calcColScore(qThreatenedIndex, qThreatSums, qLis, qRow, qDiag1, qDiag2):
    '''
    Calculates the number of threats for each space in the column containing the
    queen with the most threats. The number of threats is stored in a 1D array of
    size n.
    Input:    - an int representing the position of the queen having highest threats.
                  - a 1D list containing total number of threats for each queen.
                  - a 1D list representing number of threats on row.
                  - a 1D list representing number of threats on colume.
                  - a 1D list representing number of threats on the first diagonal.
                  - a 1D list representing number of threats on the second diagonal.
    Output:  - a 1D list, where the index represents a row in the column,
                    and the value is the number of threats found in that space.
                    Again, note that index 0 represents row 1.
    '''
    qSize = len(qThreatSums)
    qCol = [0] * qSize
    for i in range(1, qSize+1):
        if i == qLis[qThreatenedIndex-1]:
            qCol[i-1] = qThreatSums[qThreatenedIndex-1] #this is for the row containing the queen
        else:
            qCol[i-1] = 1 + qRow[i-1] + qDiag1[qSize + qThreatenedIndex - i - 1] + qDiag2[qThreatenedIndex + i - 2]
                            
    return qCol



def findLeastThreatened(qCol,qOrigin):
    '''
    Iterates through the list of the threats against each space in a column, and finds
    the least threatened (lowest value). The index of the lowest value is stored in a list.
    If there are multiple spaces with the lowest number of threats, one is seected
    randomly.
    Input:  - a 1D list representing number of threats on colume.
                - a 1D list representing oringial positions of queens.
    Output:  - an int representing the index of the least threatened space.
    '''
    qMin = len(qCol)
    qMinTracker = []

    for i in range(1, len(qCol)+1):
        if qCol[i-1] < qMin and qCol[i-1] != qOrigin:
            qMin = qCol[i-1]
            qMinTracker.clear() #clear old list since that was for a larger number of threats
            qMinTracker.append(i) #append index of the space with the least threats
        elif qCol[i-1] == qMin and qCol[i-1] != qOrigin:
            qMinTracker.append(i)
 
    qMinimumIndex = random.choice(qMinTracker) #randomly choose the least threatened space
    

    return qMinimumIndex


def solve(board_size):
    '''
    This is the main driver of the program. It makes all other function calls, including
    initializing the lists that track threats in each row, diagonal, and the most threatened
    column. It also updates these values when a queen is moved from one row in a column to
    another. This function has a while loop that will execute either until the board is soved
    (when the number of threats equals 1 - meaning it only has 1 queen, so no conflict) or
    until the number of iterations (moves) exceeds the max number of iterations allowed.
    Input:  - an int representing size of board and number of queens.
    Output:  - a 1D list of updated queens positions (solution to n-queens problem)
    '''
    if (board_size-8) % 6 == 0:
        qLis = initialState(board_size, 1)
    elif (board_size-9) % 6 == 0:
        qLis = initialState(board_size, 2)
    else:
        qLis = initialState(board_size, 0)
    step = 0
    maxIterations = 60 #// 2 #maximum number of steps/moves allowed

    #initializes scores in the row and two diagonals based on initial board configuration
    qRow = calcRowScore(qLis)
    qDiag1 = calcDiag1Score(qLis)
    qDiag2 = calcDiag2Score(qLis)

    while step <= maxIterations:
        
        qThreatSums = calcThreatSum(qLis, qRow, qDiag1, qDiag2)
        qThreatenedIndex = findMostThreatened(qThreatSums)

        if qThreatSums[qThreatenedIndex-1] == 1: #executes if current board is a solution
            answer = qLis
            print('boardsize: ',board_size)
            print("Step: ", step)
            
            return answer
        
        qCol = calcColScore(qThreatenedIndex, qThreatSums, qLis, qRow, qDiag1, qDiag2)
        qLisOld = qLis[:] #make a copy of the old list before a queen is moved
        
        qMinimumIndex = findLeastThreatened(qCol, qLis[qThreatenedIndex-1])
        qLis[qThreatenedIndex-1] = qMinimumIndex

        #updates values in the tracking lists of row and diagonal scores
        if qLisOld != qLis:
            qRow[qLisOld[qThreatenedIndex-1]-1] -= 1
            qRow[qMinimumIndex-1] += 1
            
            qDiag1[board_size - qLisOld[qThreatenedIndex-1] + qThreatenedIndex - 1] -= 1
            qDiag1[board_size - qMinimumIndex + qThreatenedIndex - 1] += 1

            qDiag2[qLisOld[qThreatenedIndex-1] + qThreatenedIndex - 2] -= 1
            qDiag2[qMinimumIndex + qThreatenedIndex - 2] += 1
            
            step += 1 #only updates if the new board is a different configuration from the old one
           
            
    return solve(board_size)


if __name__=="__main__":
    print(solve(1000004))
