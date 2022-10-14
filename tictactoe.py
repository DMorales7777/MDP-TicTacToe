# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 16:37:56 2022

Name:  Daniel Morales
EUID:  dm0698
Class: CSCE 4201.001

Pits Markov Desicion Process AI with Human Level Reflex Agent
"""

'''
00 01 02 03
10 11 12 13
20 21 22 23
30 31 32 33

X    Y    X->Y
0    0     
0    1     
1    0    
1    1
'''
import random as rand
import copy
from itertools import chain

# Draws Board
def draw_board(board):
    for row in board:
        for space in row:
            if (space != None):
                print(space, end=" ")
            else:
                print("-", end=" ")
        print()

# Checks for win, returns winning charl, None if none
def check_win(board):
    # Rows
    for row in board:
        if len(set(row)) == 1 and row[0] != None:
            return row[0]
    
    # Columns 
    for col in range(0,4):
        check_list = []
        for row in  range(0,4):
            check_list.append(board[row][col])
        if len(set(check_list)) == 1 and check_list[0] != None:
            return check_list[0]
        
    # Diagonal
    if board[0][0] == board[1][1] == board[2][2] == board[3][3] and board[0][0] != None:
        return board[0][0]
    
    # Reverse Diagonal
    if board[0][3] == board[1][2] == board[2][1] == board[3][0] and board[0][3] != None:
        return board[0][3]
    
    return None

# Adds one to merit score (Helper Function)
def update_merit(val, m_O, m_X):
    if val == "X":
        m_X += 1
    if val == "O":
        m_O += 1
    return (m_O, m_X)

# Returns Merits score of both X and O
def check_merit(board):
    m_O = 0
    m_X = 0
    
    # Rows
    for i in range(0,2):
        for row in board:
            check_list = row[0+i:3+i]
            if len(set(check_list)) == 1 and check_list[0] != None:
                m_O, m_X = update_merit(check_list[0], m_O, m_X)
    
    # Columns
    for i in range(0,2):
        for col in range(0,4):
            check_list = []
            for row in range(0,3):
                check_list.append(board[row+i][col])
            if len(set(check_list)) == 1 and check_list[0] != None:
                m_O, m_X = update_merit(check_list[0], m_O, m_X)
    
    # Diagonals
    for rOS in range(0,2):
        for cOS in range(0,2):
            check_list = []
            for row in range(0,3):
                check_list.append(board[row+rOS][row+cOS])
            if len(set(check_list)) == 1 and check_list[0] != None:
                m_O, m_X = update_merit(check_list[0], m_O, m_X)
    
    # Reverse Diagonals
    for rOS in range(0,2):
        for cOS in range(0,2):
            check_list = []
            for row in range(0,3):
                check_list.append(board[row+rOS][-(row+cOS+1)])
            if len(set(check_list)) == 1 and check_list[0] != None:
                m_O, m_X = update_merit(check_list[0], m_O, m_X)
    
    return (m_O, m_X)

# First reward function, strict
def reward_1(board, i, j):
    # Base Reward if not None
    rew = 10
    
    # More Readable Chars
    assigned_icon = "X"
    opponent_icon = "O"
    
    # Creates copy of board
    simulated_board = copy.deepcopy(board)
    simulated_board[i][j] = assigned_icon
    
    # Win
    ver = check_win(simulated_board)
    if ver == assigned_icon:
        rew += 1000000
    
    # Merit
    oldMerit = check_merit(board)[1]
    newMerit = check_merit(simulated_board)[1]
    if oldMerit < newMerit:
        rew += 100000
    
    # Enemy Win
    simulated_board[i][j] = opponent_icon
    ver = check_win(simulated_board)
    if ver == opponent_icon:
        rew += 500000
    
    # Enemy Merit
    oldMerit = check_merit(board)[0]
    newMerit = check_merit(simulated_board)[0]
    if oldMerit < newMerit:
        rew += 50000
    
    return rew

# Second reward function, leniant
def reward_2(board, i, j):
    # Base Reward if not None
    rew = 10
    
    # More Readable Chars
    assigned_icon = "X"
    opponent_icon = "O"
    
    # Creates copy of board
    simulated_board = copy.deepcopy(board)
    simulated_board[i][j] = assigned_icon
    
    # Win
    ver = check_win(simulated_board)
    if ver == assigned_icon:
        rew += 100   
    
    # Merit
    oldMerit = check_merit(board)[1]
    newMerit = check_merit(simulated_board)[1]
    if oldMerit < newMerit:
        rew += 70
    
    # Enemy Win
    simulated_board[i][j] = opponent_icon
    ver = check_win(simulated_board)
    if ver == opponent_icon:
        rew += 85
    
    # Enemy Merit
    oldMerit = check_merit(board)[0]
    newMerit = check_merit(simulated_board)[0]
    if oldMerit < newMerit:
        rew += 35
    
    return rew

# MDP Based AI
def player1(board, rewardVersion):
    # Bellman Equation: V(s) = max_a( R(s,a) + gamma( V(s) ) )
    
    # Reward Map
    rewardMap = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    
    # Based on reward version
    if rewardVersion == 1: # Strong
        for i, row in enumerate(board):
            for j, slot in enumerate(row):
                if slot == None:
                    rewardMap[i][j] = reward_1(board, i, j)
    else: # Leniant
        for i, row in enumerate(board):
            for j, slot in enumerate(row):
                if slot == None:
                    rewardMap[i][j] = reward_2(board, i, j)
    '''
    print()
    draw_board(rewardMap)
    print()
    draw_board(board)
    print()
    '''
    
    # Returns Random based on value
    rewardMap_1D = list(chain.from_iterable(rewardMap))
    randomNumberList = rand.choices(rewardMap_1D, k=1, weights=rewardMap_1D)
    for i in range(0,4):
        for j in range(0,4):
            if randomNumberList[0] == rewardMap[i][j]:
                return (i, j)
    
    # Fail Safe (Gets Max Val)
    maxVal = 0
    maxRow = 0
    maxCol = 0
    for i in range(0,4):
        for j in range(0,4):
            if rewardMap[i][j] > maxVal:
                maxVal = rewardMap[i][j]
                maxRow = i
                maxCol = j
    
    return (maxRow, maxCol)

# Human AI
def player2(board):
    assigned_icon = "O"
    opponent_icon = "X"
    
    # Next Move is a Win
    for i in range(0,4):
        for j in range(0,4):
            simulated_board = copy.deepcopy(board)
            
            if simulated_board[i][j] == None:
                simulated_board[i][j] = assigned_icon
                ver = check_win(simulated_board)
                if ver == assigned_icon:
                    #print("Calculated Victory")
                    return (i,j)            
    
    # Block Opponent Win
    for i in range(0,4):
        for j in range(0,4):
            simulated_board = copy.deepcopy(board)
            
            if simulated_board[i][j] == None:
                simulated_board[i][j] = opponent_icon
                ver = check_win(simulated_board)
                if ver == opponent_icon:
                    #print("Goal Line Stand")
                    return (i,j) 
    
    # Make a merit move
    for i in range(0,4):
        for j in range(0,4):
            simulated_board = copy.deepcopy(board)
            
            if simulated_board[i][j] == None:
                simulated_board[i][j] = assigned_icon
                oldMerit = check_merit(board)[0]
                newMerit = check_merit(simulated_board)[0]
                if oldMerit < newMerit:
                    #print("Oh yeah, merit move")
                    return (i,j)  

    # Block a merit move
    for i in range(0,4):
        for j in range(0,4):
            simulated_board = copy.deepcopy(board)
            
            if simulated_board[i][j] == None:
                simulated_board[i][j] = opponent_icon
                oldMerit = check_merit(board)[1]
                newMerit = check_merit(simulated_board)[1]
                if oldMerit < newMerit:
                    #print("Yoink")
                    return (i,j)
    
    # Randomly place
    #print("No Good Move Found, Making Random Choice...")
    row = rand.randint(0,3)
    col = rand.randint(0,3)
    while (board[row][col] != None):
        #print("Reshuffle")
        row = rand.randint(0,3)
        col = rand.randint(0,3)
    #print("Player 2:", row, col)
    return (row, col)

# TicTacToe Game
def tictactoe(start, rewardVersion):
    winner = None
    meritWin = False
    
    displayBoard = 0
    
    X = "X"
    O = "O"
    
    board = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    
    plays=0

    while plays < 16 and winner == None:
        
        openSpot = False
        for row in board:
            for spot in row:
                if spot == None:
                    openSpot = True
        
        if not openSpot:
            break
        
        if (plays+start)%2 == 0:
            #print("Player 1 (X) Turn")
            row, col = player1(board, rewardVersion)
            board[row][col] = "X"
        else:
            #print("Player 2 (O) Turn")
            row, col = player2(board)
            board[row][col] = "O"       
        winner = check_win(board)
        plays += 1
        
        if displayBoard:
            draw_board(board)
            print()

    #winner = check_win(board)
    meritScoreO, meritScoreX = check_merit(board)
    if winner == None:
        if meritScoreO == meritScoreX:
            winner = "D"
        elif meritScoreO > meritScoreX:
            meritWin = True
            winner = "O"
        elif meritScoreO < meritScoreX:
            meritWin = True
            winner = "X"
        else:
            winner = "ERR"
    
    '''
    if displayBoard:
        print("Final Outcome:")
    draw_board(board)
    
    
    if winner != "D" and not meritWin:
        print("Win:", winner)
    elif meritWin:
        print("Merit Win:", winner)
    else:
        print(winner)
    '''
    #print("Merit Score X:", meritScoreX)
    #print("Merit Score O:", meritScoreO)
    
    return (winner, meritWin)

# Task 2
def task2():
    print("Workin on Task 2... Stronger Rewards")
    rewardFunction = 1
    p1_wins = 0
    p1_meritWins = 0
    p1_loss = 0
    
    p2_wins = 0
    p2_meritWins = 0
    p2_loss = 0
    
    games = 100
    gamesPlayed = 0
    winner = None
    while gamesPlayed < games:
        print("\rGame", gamesPlayed+1, end=" ")
        # Run game
        winner, merit = tictactoe(gamesPlayed, rewardFunction)
        
        # Add points
        if winner != "D":
            if winner == "X":
                p2_loss += 1
                if merit:
                    p1_meritWins += 1
                else:
                    p1_wins += 1
            elif winner == "O":
                p1_loss += 1
                if merit:
                    p2_meritWins += 1
                else:
                    p2_wins += 1
        # Restart
        gamesPlayed+=1
        #print()
    
    print()
    print()
    print("Task 2 Results:")
    print("--Player 1--")
    print("Ouright Wins:", p1_wins)
    print("Merit Wins:", p1_meritWins)
    print("Losses:", p1_loss)
    print(f"Win/Merit/Loss: {p1_wins}/{p1_meritWins}/{p1_loss}")
    try:
        print("WML Ratio:", round(((p1_wins + (p1_meritWins)) / p1_loss), 3))
    except ZeroDivisionError:
        print("WML Ratio:", round(((p1_wins + (p1_meritWins))), 3))
    print("------------")
    print()
    print("--Player 2--")
    print("Ouright Wins:", p2_wins)
    print("Merit Wins:", p2_meritWins)
    print("Losses:", p2_loss)
    print(f"Win/Merit/Loss: {p2_wins}/{p2_meritWins}/{p2_loss}")
    try:
        print("WML Ratio:", round(((p2_wins + (p2_meritWins)) / p2_loss), 3))
    except:
        print("WML Ratio:", round(((p2_wins + (p2_meritWins))), 3))
    print("------------")
    print()

# Task 3
def task3():
    print("Workin on Task 3... Weak Rewards")
    rewardFunction = 2
    
    p1_wins = 0
    p1_meritWins = 0
    p1_loss = 0
    
    p2_wins = 0
    p2_meritWins = 0
    p2_loss = 0
    
    games = 100
    gamesPlayed = 0
    winner = None
    while gamesPlayed < games:
        print("\rGame", gamesPlayed+1, end=" ")
        # Run game
        winner, merit = tictactoe(gamesPlayed, rewardFunction)
        
        # Add points
        if winner != "D":
            if winner == "X":
                p2_loss += 1
                if merit:
                    p1_meritWins += 1
                else:
                    p1_wins += 1
            elif winner == "O":
                p1_loss += 1
                if merit:
                    p2_meritWins += 1
                else:
                    p2_wins += 1
        # Restart
        gamesPlayed+=1
        #print()
    
    print()
    print()
    print("Task 3 Results:")
    print("--Player 1--")
    print("Ouright Wins:", p1_wins)
    print("Merit Wins:", p1_meritWins)
    print("Losses:", p1_loss)
    print(f"Win/Merit/Loss: {p1_wins}/{p1_meritWins}/{p1_loss}")
    try:
        print("WML Ratio:", round(((p1_wins + (p1_meritWins)) / p1_loss), 3))
    except ZeroDivisionError:
        print("WML Ratio:", round(((p1_wins + (p1_meritWins))), 3))
    print("------------")
    print()
    print("--Player 2--")
    print("Ouright Wins:", p2_wins)
    print("Merit Wins:", p2_meritWins)
    print("Losses:", p2_loss)
    print(f"Win/Merit/Loss: {p2_wins}/{p2_meritWins}/{p2_loss}")
    try:
        print("WML Ratio:", round(((p2_wins + (p2_meritWins)) / p2_loss), 3))
    except:
        print("WML Ratio:", round(((p2_wins + (p2_meritWins))), 3))
    print("------------")
    print()

# Task 4
def task4():
    print("Task 4: Before a winning move (Using Stronger Rewards)")
    print("Align reward values with respective indexes")
    print()
    X = "X"
    O = "O"
    
    rewardVersion = 1
    board = [
        [None, O, O, None],
        [X, O, O, None],
        [X, None, O, None],
        [X, None, None, X]
    ]
    
    draw_board(board)
    print()
    
    rewardMap = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    if rewardVersion == 1:
        for i, row in enumerate(board):
            for j, slot in enumerate(row):
                if slot == None:
                    rewardMap[i][j] = reward_1(board, i, j)
    else:
        for i, row in enumerate(board):
            for j, slot in enumerate(row):
                if slot == None:
                    rewardMap[i][j] = reward_2(board, i, j)
    draw_board(rewardMap)

def main():
    
    print("Task 1 implemented as Player 1 and related functions\n")
    task2()
    task3()
    task4()
 
    return 0
    
if __name__ == "__main__":
    main()