# Philip Le

"""
ToDo: 
1. How to improve the performance 
    a. Either with parallel computing with multi-core
    b. Or use the restriction on the number of computation for minmax alg
2. Split the file into multiple modules and add a conf file
3. Add the input options with Pygame viz instead.     
    """



import pygame
import sys
import time
import os
import math
import copy
import random
import numpy as np
import pandas as pd
# from joblib import Parallel, delayed
# from numba import njit, prange


os.chdir('/home/philip/Learning/Computer_Science/CS50_Python/Projects/tictactoe')

pygame.init()

# define the game size

def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))  
       assert userInput < 10
    except ValueError:
       print("Not an integer! Try again.")
       continue
    except AssertionError:
       print("Enter a number less than 10! Try again.")
       continue
    else:
       return userInput 
       break


global bs; global nt; global AIlevel
bs = inputNumber("Input the size of ttt-game board (less than 10): ")    
nt = inputNumber("Input the number of continuous length to win: ") 
nt <= bs, 'Length to win must be less than or equal to board size'
AIlevel = inputNumber("Level of your AI (1 random - 7 complex): ") 

X = "X"
O = "O"
EMPTY = None

size = width, height = 50 + 160*bs, 100 + 160*bs

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)





def initial_state(bs):
    """
    Returns starting state of the board.
    """
    return [[EMPTY for i in range(bs)] for i in range(bs)]

user = None
board = initial_state(bs)
ai_turn = False


def whichplayer(board):
    """
    Returns player who has the next turn on a board.
    """
    if (board == initial_state(bs)) | ((pd.notna(board).sum())%2 == 0):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = []
    for i in range(bs):
        for j in range(bs):
            if pd.isna(board[i][j]):
                all_actions.append((i,j))
    return all_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    nboard = copy.deepcopy(board)
    assert pd.isna(nboard[action[0]][action[1]])==True, "Invalid action"
    nboard[action[0]][action[1]] = whichplayer(board)
    return nboard


def X_winner(subboard):
    assert len(subboard) == nt, 'Check the size again'
    ## diagonal check
    if ([subboard[i][i] for i in range(nt)]==[X for i in range(nt)]) | ([subboard[i][nt-i-1] for i in range(nt)]==[X for i in range(nt)]): 
        return True

    ## checking if there are row or column with all X
    for i in range(nt):
        if (subboard[i]==[X for j in range(nt)]) | ([v[i] for v in subboard]==[X for j in range(nt)]):
            return True

    return False


def O_winner(subboard):
    assert len(subboard) == nt, 'Check the size again'
    ## diagonal check
    if ([subboard[i][i] for i in range(nt)]==[O for i in range(nt)]) | ([subboard[i][nt-i-1] for i in range(nt)]==[O for i in range(nt)]): 
        return True
    
        ## checking if there are row or column with all O
    for i in range(nt):
        if (subboard[i]==[O for j in range(nt)]) | ([v[i] for v in subboard]==[O for j in range(nt)]):
            return True
    
    return False


def whowinner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(bs-nt+1):
        for j in range(bs-nt+1):
            subboard = [[board[i+row][j+col] for col in range(nt)] for row in range(nt)]
            if X_winner(subboard):
                return X
            elif O_winner(subboard):
                return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (pd.isna(board).sum()==0) | (whowinner(board)!=None):
        return True
    else:
        return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if whowinner(board)==X:
        return 1
    elif whowinner(board)==O:
        return -1
    else:
        return 0


## We will now update the alpha-beta pruning
# Alpha: Best already explored option for player Max  'X'
# Beta: Best already explored option for player Min  'O'

## define the two recursive funcs to be used later 
def MAX_VALUE(board, alpha, beta, level=0):
    if terminal(board):         
        return utility(board), None 

    v = -np.inf
    # intialize the values  
    action_board = actions(board)  
    random_choice_list = [x for x in action_board\
                if (x[0] >= math.floor(bs/2)-1) & (x[0] <= math.floor(bs/2)+1) &  (x[1] >= math.floor(bs/2)-1) & (x[1] <= math.floor(bs/2)+1)]
    

    ## restrict the computation by using level
    if level < AIlevel:
        for action in np.random.permutation(action_board): 
            nboard = result(board, action)
            new_v = MIN_VALUE(nboard, alpha, beta, level=level+1)[0]
            if new_v == 1:
                return (1, action)
                break
            elif new_v > v:
                v = new_v
                final_action = action
            
            # check the alpha and beta
            if v > alpha:
                alpha = v
            if v >= beta:
                return (v, action)
                break


    else:
        if len(random_choice_list) > 0:
            final_action = random.choice(random_choice_list)
        else:
            final_action = random.choice(action_board)
        v = utility(result(board, final_action))

    return v, final_action


def MIN_VALUE(board, alpha, beta, level=0):
    if terminal(board):
        return utility(board), None

    v = np.inf
    # intialize the values  
    action_board = actions(board)  
    random_choice_list = [x for x in action_board\
                if (x[0] >= math.floor(bs/2)-1) & (x[0] <= math.floor(bs/2)+1) &  (x[1] >= math.floor(bs/2)-1) & (x[1] <= math.floor(bs/2)+1)]
    ## Q: Why setting up the final_action here will be problematic?

    if level < AIlevel:
        for action in np.random.permutation(action_board):
            nboard = result(board, action)
            new_v = MAX_VALUE(nboard, alpha, beta, level=level+1)[0]
            if new_v == -1:
                return (-1, action)
                break
            if new_v < v:
                v = new_v
                final_action = action

            # check alpha and beta
            if v < beta:
                beta = v
            if v <= alpha:
                return (v, action)
                break

    else:
        if len(random_choice_list) > 0:
            final_action = random.choice(random_choice_list)
        else:
            final_action = random.choice(action_board)
        v = utility(result(board, final_action))

    return v, final_action


## TODO: main function change to board with bigger size 
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    start = time.time()
    # check if it is the start of the game to use the open-book strategy
    if (bs > 5) & (pd.notna(board).sum() < 4):
        v = 0
        final_action = random.choice([x for x in actions(board)\
            if (x[0] >= math.floor(bs/2)-1) & (x[0] <= math.floor(bs/2)) &  (x[1] >= math.floor(bs/2)-1) & (x[1] <= math.floor(bs/2))])
    else:
        alpha = -np.inf
        beta = np.inf
        if whichplayer(board)==X:
            v, final_action = MAX_VALUE(board, alpha, beta)
        else:
            v, final_action = MIN_VALUE(board, alpha, beta)

    print(f'Value {v}, Action {final_action}, AI thinking time: {round(time.time() - start,4)}')
    return final_action



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)
    

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                    height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(bs):
            row = []
            for j in range(bs):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, bs)

                if board[i][j] != EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = terminal(board)
        player = whichplayer(board)

        # Show title
        if game_over:
            winner = whowinner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"AI thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = minimax(board)
                board = result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(bs):
                for j in range(bs):
                    if (board[i][j] == EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / bs, height - 65, width / bs, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    print('******************* New Game *************************')
                    board = initial_state(bs)
                    ai_turn = False

    pygame.display.flip()


# client.close()