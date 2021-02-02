
import random
import numpy as np


'''
Sets up the "board" so every queen is placed in its own row and column.
The "rows" are shuffled to be in random order of a 1D array. Note that
index 0 of the list will represent column 1, index 1 represents column 2, etc.
Returned: 1D list, where the index represents the column, and the
          value at each index represents the row the queen is in.
          i.e. [3, 1, 4, 2] has queens in: column 1, row 3
                                           column 2, row 1
                                           column 3, row 4
                                           column 4, row 2
'''
def initialState(board_size):
    qLis = np.arange(board_size)
    qLis += 1
    qLis = qLis.tolist()
    qLis = qLis[1::2] + qLis[::2]
    #qLis = list(range(1, board_size+1))
    #random.shuffle(qLis)

    return qLis
'''
Calculates the "score" of each row, which is the number of queens in that row.
The score for each row is stored in a 1D list sized n.
Returned: 1D list, where the index represents the row and the value is the number
          of queens found in that row. Again, note that index 0 represents row 1.
'''
def calcRowScore(qLis):
    qSize = len(qLis)
    qRow = [0] * qSize #initializes list to zeroes
    for i in range(1, qSize+1): 
        position = qLis[i-1] - 1 #get value from each index of the list of queens positions (represents the row)
        qRow[position] += 1 #increases count of queens at the specified row
        
    return qRow

'''
Calculates the "score" of each top-left to bottom-right diagonal, which is the number
of queens in that diagonal. The score for each diagonal is stored in a 1D list sized (2n-1)
Returned: 1D list, where the index represents the diagonal (starting bottom left corner)
          and the value is the number of queens found in that diagonal. Again, note that
          index 0 represents row 1.
'''
def calcDiag1Score(qLis):
    qSize = len(qLis)
    qDiag1 = [0] * (2*qSize - 1) #2n-1 diagonals on a board
    for i in range(1, qSize+1):
        position = qSize - qLis[i-1] + i - 1 #get the diagonal position of the current queen
        qDiag1[position] += 1

    return qDiag1

'''
Calculates the "score" of each bottom-left to top-right diagonal, which is the number
of queens in that diagonal. The score for each diagonal is stored in a 1D list sized (2n-1)
Returned: 1D list, where the index represents the diagonal (starting top-left corner)
          and the value is the number of queens found in that diagonal. Again, note that
          index 0 represents row 1.
'''
def calcDiag2Score(qLis):
    qSize = len(qLis)
    qDiag2 = [0] * (2*qSize - 1) 
    for i in range(1, qSize+1):
        position = qLis[i-1] + i - 2 #get the diagonal position of the current queen
        qDiag2[position] += 1

    return qDiag2

'''
Calculates the total number of threats for each queen on the board. Sums the threats in
the row with the threats on the fist diagonal with the threats on the second diagonal.
The total sum is stored in a 1D list sized n.
Returned: 1D list, where the index represents the diagonal (starting top-left corner)
          and the value is the number of queens found in that diagonal. Again, note that
          index 0 represents row 1.
'''
def calcThreatSum(qLis, qRow, qDiag1, qDiag2):
    qSize = len(qLis)
    qThreatSums = [0] * qSize
    for i in range(1, qSize+1):
        rowThreat = qRow[qLis[i-1]-1]
        diag1Threat = qDiag1[qSize - qLis[i-1] + i - 1]
        diag2Threat = qDiag2[qLis[i-1] + i - 2]

        #need to subtract 2 so the threat of the queen isn't duplicated
        qThreatSums[i-1] = rowThreat + diag1Threat + diag2Threat - 2 

    return qThreatSums
'''
Iterates through the list of the threats against each queen and finds the most
threatened (highest value). The index of the highest value is stored in a list.
If there are multiple queens with the highest number of threats, one is seected
randomly.
Returned Value: int representing the index of the most threatened queen.
'''
def findMostThreatened(qThreatSums):
    
    qMaxTracker = np.argwhere(qThreatSums == np.amax(qThreatSums))
    qMaxTracker += 1
    qMaxTracker = qMaxTracker.flatten().tolist()
    qThreatenedIndex = random.choice(qMaxTracker) #randomly choose the most threatened queen
    
    return qThreatenedIndex

'''
Calculates the number of threats for each space in the column containing the
queen with the most threats. The number of threats is stored in a 1D array of
size n.
Returned Value: 1D list, where the index represents a row in the column,
                and the value is the number of threats found in that space.
                Again, note that index 0 represents row 1.
'''
def calcColScore(qThreatenedIndex, qThreatSums, qLis, qRow, qDiag1, qDiag2):
    qSize = len(qThreatSums)
    qCol = [0] * qSize
    for i in range(1, qSize+1):
        if i == qLis[qThreatenedIndex-1]:
            qCol[i-1] = qThreatSums[qThreatenedIndex-1] #this is for the row containing the queen
        else:
            qCol[i-1] = 1 + qRow[i-1] + qDiag1[qSize + qThreatenedIndex - i - 1] + qDiag2[qThreatenedIndex + i - 2]
                            
    return qCol

'''
Iterates through the list of the threats against each space in a column, and finds
the least threatened (lowest value). The index of the lowest value is stored in a list.
If there are multiple spaces with the lowest number of threats, one is seected
randomly.
Returned Value: int representing the index of the least threatened space.
'''
def findLeastThreatened(qCol):
    
    qMinTracker = np.argwhere(qCol == np.amin(qCol))
    qMinTracker += 1
    qMinTracker = qMinTracker.flatten().tolist()
    qMinimumIndex = random.choice(qMinTracker) #randomly choose the least threatened space
    
    return qMinimumIndex

'''
This is the main driver of the program. It makes all other function calls, including
initializing the lists that track threats in each row, diagonal, and the most threatened
column. It also updates these values when a queen is moved from one row in a column to
another. This function has a while loop that will execute either until the board is soved
(when the number of threats equals 1 - meaning it only has 1 queen, so no conflict) or
until the number of iterations (moves) exceeds the max number of iterations allowed.
Returned: 1D list of updated queens positions (solution to n-queens problem)
'''
def solve(board_size):
    qLis = initialState(board_size)
    step = 0
    maxIterations = board_size // 2 #maximum number of steps/moves allowed

    #initializes scores in the row and two diagonals based on initial board configuration
    qRow = calcRowScore(qLis)
    qDiag1 = calcDiag1Score(qLis)
    qDiag2 = calcDiag2Score(qLis)

    while step <= maxIterations:
        qThreatSums = calcThreatSum(qLis, qRow, qDiag1, qDiag2)
        qThreatenedIndex = findMostThreatened(qThreatSums)

        if qThreatSums[qThreatenedIndex-1] == 1: #executes if current board is a solution
            answer = qLis
            print("Step: ", step)
            print(answer)
            
            return answer
        
        qCol = calcColScore(qThreatenedIndex, qThreatSums, qLis, qRow, qDiag1, qDiag2)
        qLisOld = qLis[:] #make a copy of the old list before a queen is moved
        
        qMinimumIndex = findLeastThreatened(qCol)
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
        solve(987654)

        

