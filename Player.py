#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import random
import ReverseCommon


class Player:
    """ プレーヤの基盤クラス(AIも含む) """

    def __init__(self, color):
        """ コンストラクタ """
        self._color = color

    def next_move(self, board):
        """ 次の手を返す """
        pass

    @property
    def color(self):
        """ 自分の色を返す """
        return self._color


class RandomAi(Player):
    """ ランダムで石を置くAI """

    def next_move(self, board):
        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        # ランダムで次の手を選ぶ
        index = random.randint(0, len(all_candidates) - 1)
        return all_candidates[index]

class NextStoneMaxAi(Player):
    """今回の１手で最も石が取れる場所に置くAI"""

    def next_move(self, board):
        # 石を置ける全候補地
        all_candidatess = ReverseCommon.get_puttable_points(board, self._color)

        # 今回の一手で最も石が取れる場所一覧
        filtered_candidates = []
        max_score = -1
        for candidates in all_candidatess:
            next_board = ReverseCommon.put_stone(board, self._color, candidates[0], candidates[1])
            score = ReverseCommon.get_score(next_board, self._color)
            if score >= max_score:
                filtered_candidates.append(candidates)
                max_score = score

        return filtered_candidates[random.randint(0, len(filtered_candidates) - 1)]



class Human(Player):
    """人間です。"""

    def next_move(self, board):
        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        while True:
            try:
                # x,yの形式で入力する
                next_move_str = raw_input("next_move > ")
                next_move_str_split = next_move_str.split(",")
                if len(next_move_str_split) == 2:
                    next_move = [int(next_move_str_split[0]), int(next_move_str_split[1])]
                    if next_move in all_candidates:
                        return next_move
                    else:
                        print ("can't put there.")
            except ValueError:
                print ("format error.")


class RandomAiKnowGoodMove(Player):
    """ 最低限の手の良し悪しを知っているAI """

    def next_move(self, board):
        board_size = len(board)
        known_good_moves = [[0, 0], [0, board_size -1], [board_size -1, 0], [board_size -1, board_size -1]]
        known_bad_moves = [[0, 1], [1, 0], [1, 1], [0, board_size -2], [1, board_size -2], [1, board_size -1], [board_size -2, 0], [board_size -2, 1], [board_size -1, 1], [board_size -1, board_size -2], [board_size -2, board_size -1], [board_size -2, board_size -2]]

        all_candidates = ReverseCommon.get_puttable_points(board, self._color)

        # 4隅が取れるなら取る
        good_moves = filter(lambda good_move: good_move in known_good_moves, all_candidates)
        if len(good_moves) > 0:
            return good_moves[random.randint(0, len(good_moves) - 1)]

        # 4隅に隣接する場所は避ける
        not_bad_moves = filter(lambda  not_bad_move: not_bad_move not in (known_good_moves + known_bad_moves), all_candidates)
        if len(not_bad_moves) > 0:
            return not_bad_moves[random.randint(0, len(not_bad_moves) - 1)]

        return all_candidates[random.randint(0, len(all_candidates) - 1)]

