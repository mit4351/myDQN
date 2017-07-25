#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import os
from rlglue.utils import TaskSpecVRLGLUE3


# 定数
# 何も置かれていない
NONE = 0
# 白
WHITE = 1
# 黒
BLACK = 2

# Common Functions

def get_score(board, color):
    """ 指定した色の現在のスコアを返す """
    size = len(board)
    score = 0
    for i in range(0, size):
        for j in range(0, size):
            if board[i][j] == color:
                score += 1
    return score


def get_remain(board):
    """ 何も置かれていない場所の数を返す """
    size = len(board)
    count = 0
    for i in range(0, size):
        for j in range(0, size):
            if board[i][j] == None:
                count += 1
    return count


def getenemy(color):
    if color == BLACK:
       return WHITE
    return BLACK

def has_right_reversible_stone(board, i, j, color):
    """ 指定座標の右側に返せる石があるか調べる """
    size = len(board)
    enemy = getenemy(color)
    mannaka = size / 2 +1
    if j <= mannaka and board[i][j+1] == enemy:
        for k in range(j + 2, size):
            if board[i][k] == color:
                return True
            elif board[i][k] == NONE:
                break
    return False


def has_left_reversible_stone(board, i, j, color):
    """ 指定座標の左側に返せる石があるか調べる """
    enemy = getenemy(color)
    if j >=2 and board[i][j-1] == enemy:
        for k in range(j - 2, -1, -1):
            if board[i][k] == color:
                return True
            elif board[i][k] == NONE:
                break
    return False


def has_upper_reversible_stone(board, i, j, color):
    """ 指定座標の上に返せる石があるか調べる """
    enemy = getenemy(color)
    if i >= 2 and board[i-1][j] == enemy:
        for k in range(i - 2, -1, -1):
            if board[k][j] == color:
                return True
            elif board[k][j] == NONE:
                break
    return False


def has_lower_reversible_stone(board, i, j, color):
    """ 指定座標の下に返せる石があるか調べる """
    size = len(board)
    enemy = getenemy(color)
    mannaka = size / 2 +1
    if i <= mannaka and board[i+1][j] == enemy:
        for k in range(i + 2, size):
            if board[k][j] == color:
                return True
            elif board[k][j] == NONE:
                break
    return False


def has_right_upper_reversible_stone(board, i, j, color):
    """ 指定座標の右上に返せる石があるか調べる """
    size = len(board)
    enemy = getenemy(color)
    mannaka = size / 2 +1
    if i >= 2 and j <= mannaka and board[i-1][j+1] == enemy:
        k = 2
        while i - k >= 0 and j + k < size:
            if board[i-k][j+k] == color:
                return True
            elif board[i-k][j+k] == NONE:
                break
            k += 1
    return False


def has_left_lower_reversible_stone(board, i, j, color):
    """ 指定座標の左下に返せる石があるか調べる """
    size = len(board)
    enemy = getenemy(color)
    mannaka = size / 2 +1
    if j >= 2 and i <= mannaka and board[i+1][j-1] == enemy:
        k = 2
        while i + k < size  and j - k >= 0:
            if board[i+k][j-k] == color:
                return True
            elif board[i+k][j-k] == NONE:
                break
            k += 1
    return False


def has_left_upper_reversible_stone(board, i, j, color):
    """ 指定座標の左上に返せr石があるか調べる """
    enemy = getenemy(color)
    if i >= 2 and j >= 2 and board[i-1][j-1] == enemy:
        k = 2
        while i - k >= 0 and j - k >= 0:
            if board[i-k][j-k] == color:
                return True
            elif board[i-k][j-k] == NONE:
                break
            k += 1
    return False


def has_right_lower_reversible_stone(board, i, j, color):
    """ 指定座標の右下に返せる石があるか調べる """
    size = len(board)
    enemy = getenemy(color)
    mannaka = size / 2 +1
    if i <= mannaka and j <= mannaka and board[i+1][j+1] == enemy:
        k = 2
        while i + k < size and j + k < size:
            if board[i+k][j+k] == color:
                return True
            elif board[i+k][j+k] == NONE:
                break
            k += 1
    return False


def is_game_set(board):
    """ ゲーム終了か判定する """
    if len(get_puttable_points(board, WHITE)) == 0 and len(get_puttable_points(board, BLACK)) == 0:
        return True
    return False


def get_puttable_points(board, color):
    """ 指定した色が置ける座標をすべて返す """
    size = len(board)
    points = []
    for i in range(0, size):
        for j in range(0,size):
            if board[i][j] != NONE:
                # 何か置かれている場所はする
                continue

            # 左右に走査
            if has_right_reversible_stone(board, i, j, color) or has_left_reversible_stone(board, i, j, color):
                points.append([i, j])
                continue

            # 上下に走査
            if has_upper_reversible_stone(board, i, j, color) or has_lower_reversible_stone(board, i, j, color):
                points.append([i, j])
                continue

            # 右斜め上、左斜め下
            if has_right_upper_reversible_stone(board, i, j, color) or has_left_lower_reversible_stone(board, i, j, color):
                points.append([i, j])
                continue

            # 左上、右下
            if has_left_upper_reversible_stone(board, i, j, color) or has_right_lower_reversible_stone(board, i, j, color):
                points.append([i, j])
                continue
    return points


def put_stone(board, color, i, j):
    """ ひっくり返す """
    new_board = copy.deepcopy(board)

    # 右側をひっくり返しord[i][k] != color:
    if has_right_reversible_stone(new_board, i, j, color):
        k = j + 1
        while new_board[i][k] != color:
            new_board[i][k] = color
            k += 1

    # 左側をひっくり返していく
    if has_left_reversible_stone(new_board, i, j, color):
        k = j - 1
        while new_board[i][k] != color:
            new_board[i][k] = color
            k -= 1

    # 上側をひっくり返していく
    if has_upper_reversible_stone(new_board, i, j, color):
        k = i - 1
        while new_board[k][j] != color:
            new_board[k][j] = color
            k -= 1

    # 下側をひっくり返していく
    if has_lower_reversible_stone(new_board, i, j, color):
        k = i + 1
        while new_board[k][j] != color:
            new_board[k][j] = color
            k += 1

    # 右下をひっくりかえしていく
    if has_right_lower_reversible_stone(new_board, i, j, color):
        k = 1
        while new_board[i+k][j+k] != color:
            new_board[i+k][j+k] = color
            k += 1

    # 左上をひっくりかえしていく
    if has_left_upper_reversible_stone(new_board, i, j, color):
        k = 1
        while new_board[i-k][j-k] != color:
            new_board[i-k][j-k] = color
            k += 1

    # 右上をひっくりかえしていく
    if has_right_upper_reversible_stone(new_board, i, j, color):
        k = 1
        while new_board[i-k][j+k] != color:
            new_board[i-k][j+k] = color
            k += 1

    # 左下をひっくり返していく
    if has_left_lower_reversible_stone(new_board, i, j, color):
        k = 1
        while new_board[i+k][j-k] != color:
            new_board[i+k][j-k] = color
            k += 1

    new_board[i][j] = color
    return new_board


def getboardinfo(board,crrtflg=False):
    history = []

    b_size = len(board)
    hstr = "  "
    for i in range(b_size):
       if i < b_size +1 :
          hstr += " " + str(i+1)
       else:
          hstr += str(i+1)      
    history.append(hstr)

    for i in range(0, b_size):
        row = str(i+1) 
        if i < b_size +1:
           row += " |"
        else:
           row += "|"

        for j in range(0, b_size):
            if board[i][j] == NONE:
                row += " "
            elif board[i][j] == WHITE:
                row += "W"
            else:
                row += "B"
            row += "|"
        if (crrtflg):
           row += "\n"
        history.append(row)

    history.append("")
    if (crrtflg):
       history.append("\n")
    else:
       history.append("")
    return history


def print_board(board):
    """盤面表示"""
    for str in getboardinfo(board):
        print (str)



def history_write(history):
    f = open('myhistory.txt', 'a')
    #whistory = '\n'.join(history)
    f.writelines('# START\n' + history + '# END\n\n')
    f.close()

def TaskSpecDisplay(ts=""):
    print("TaskSpecDisplay")
    print(ts)
    if(len(ts)==0):
      ts ="""VERSION RL-Glue-3.0 PROBLEMTYPE episodic DISCOUNTFACTOR .7   """
      ts +=""" OBSERVATIONS INTS (NEGINF 1) ( 2 -5 POSINF ) DOUBLES (2 -1.2 0.5 )(-.07 .07) (UNSPEC 3.3) (0 100.5) CHARCOUNT 32 """
      ts +=""" ACTIONS INTS (5 0 4) DOUBLES (-.5 2) (2 7.8 9) (NEGINF UNSPEC) REWARDS (-5.0 5.0) EXTRA some other stuff goes here"""

    print(ts)
    TaskSpec = TaskSpecVRLGLUE3.TaskSpecParser(ts)

    if TaskSpec.valid:
       print( "=======================================================================================================")
       print( "Version: ["+TaskSpec.getVersion()+"]")
       print( "ProblemType: ["+TaskSpec.getProblemType()+"]")
       print( "DiscountFactor: ["+str(TaskSpec.getDiscountFactor())+"]")
       print( "=======================================================================================================")
       print( "\t \t \t \t Observations")
       print( "=======================================================================================================")
       print( "Observations: ["+TaskSpec.getObservations()+"]")
       print( "Integers:",TaskSpec.getIntObservations())
       print( "Doubles: ",TaskSpec.getDoubleObservations())
       print( "Chars:   ",TaskSpec.getCharCountObservations())
       print( "=======================================================================================================")
       print( "\t \t \t \t Actions")
       print( "======================================================================================================")
       print( "Actions: ["+TaskSpec.getActions()+"]")
       print( "Integers:",TaskSpec.getIntActions())
       print( "Doubles: ",TaskSpec.getDoubleActions())
       print( "Chars:   ",TaskSpec.getCharCountActions())
       print( "=======================================================================================================")
       print( "Reward :["+TaskSpec.getReward()+"]")
       print( "Reward Range:",TaskSpec.getRewardRange())
       print( "Extra: ["+TaskSpec.getExtra()+"]")
       print( "remeber that by using len() you get the cardinality of lists!")
       print( "Thus:")
       print( "len(",TaskSpec.getDoubleObservations(),") ==> ",len(TaskSpec.getDoubleObservations())," Double Observations")
       print( TaskSpec.isSpecial("NEGINF"))


