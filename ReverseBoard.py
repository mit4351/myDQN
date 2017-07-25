#!/usr/bin/python
# -*- coding: utf-8 -*-
import ReverseCommon
import numpy as np


class ReverseBoard:
    """ オセロ盤 size 偶数"""
    def __init__(self, size=8):
        """ Constructor """
        # ボード初期化
        self._board =  np.arange(size*size).reshape((size,size))
        self._board[:,:] = ReverseCommon.NONE
        #self._board = [[ReverseCommon.NONE for i in range(size)] for j in range(size)]
        self._board[size/2 -1][size/2 -1] = ReverseCommon.WHITE
        self._board[size/2][size/2] = ReverseCommon.WHITE
        self._board[size/2 -1][size/2] = ReverseCommon.BLACK
        self._board[size/2][size/2 -1] = ReverseCommon.BLACK
        # 黒のターンに初期化
        self._turn = ReverseCommon.BLACK

    def change_turn(self):
        """ 交代 """
        if self._turn == ReverseCommon.WHITE:
            self._turn = ReverseCommon.BLACK
        else:
            self._turn = ReverseCommon.WHITE

    def put_stone(self, color, i, j):
        """ 置く & ひっくり返す """
        self._board = ReverseCommon.put_stone(self._board, color, i, j)

        # プレーヤ交代
        enemy = ReverseCommon.getenemy(color)  #not(color)
        if len(ReverseCommon.get_puttable_points(self._board, enemy)) > 0:
            self.change_turn()

    def is_game_set(self):
        """ ゲームセットか返す　"""
        return ReverseCommon.is_game_set(self._board)

    def is_my_turn(self, color):
        """ 自分のターンか返す """
        if self._turn == color:
            return True
        return False

    @property
    def board(self):
        """ 盤面を返す"""
        return self._board


class CustomReverseBoard(ReverseBoard):
    """ 途中状態の盤面を作るようのクラス """
    def __init__(self, board, turn):
        self._board = board
        self._turn = turn

