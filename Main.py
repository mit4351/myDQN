#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
1.オセロの基本ロジックの実装
2.完全ランダムな手で打つAIの実装
3.今現在、最もたくさん石が取れる手を選ぶAIの実装　
4.ちょっとだけオセロの定石を知ってるAIの実装
5.もうちょっとオセロの定石を知っているAIの実装　 <=　本稿はココ
6.MinMax法で打つAIの実装
7.AlphaBeta法で打つAIの実装
8.モンテカルロ法で打つAIの実装
9.モンテカルロ木探索?で打つAIの実装
10.(このあたりで機械学習を取り入れたい?)
"""

import sys
# Main function
import ReverseBoard
import Player
import ReverseCommon
import Game
import datetime

if __name__ == "__main__":

    args = 8 
    if len(sys.argv) > 1:
       args = int(sys.argv[1])
    print("マス目::" + str(args))


    # 勝利数
    black_win = 0
    white_win = 0

    # 試行回数
    #times = 3000
    times = 10

    # 盤面を出力するか
    #output = False
    output = True

    #print "開始(%d): %s" % (times, datetime.datetime.today())
    starttime    =  datetime.datetime.today()

    # 勝負
    for i in range(0, times):

        # 盤面作成
        reverse_board = ReverseBoard.ReverseBoard(args)

        # プレイヤー
        #black_player = Player.RandomAi(ReverseCommon.BLACK)
        #black_player = Player.NextStoneMaxAi(ReverseCommon.BLACK)
        black_player = Player.RandomAiKnowGoodMove(ReverseCommon.BLACK)
        #white_player = Player.RandomAi(ReverseCommon.WHITE)
        #white_player = Player.Human(ReverseCommon.WHITE)
        white_player = Player.NextStoneMaxAi(ReverseCommon.WHITE)
        #white_player = Player.RandomAiKnowGoodMove(ReverseCommon.WHITE)

        # ゲーム開始
        game = Game.Game(black_player, white_player, reverse_board)
        game.play(output)

        # 勝者判定
        if game.get_winner() == black_player:
            black_win += 1
        else:
            white_win += 1

    #print "終了(%d): %s" % (times, datetime.datetime.today())
    endtime    =  datetime.datetime.today()

    # 各AIの勝利数
    print ("****************** 対戦結果 **************************")
    print ("* 開始(%d): %s" % (times, starttime))
    print ("* 終了(%d): %s" % (times, endtime))
    print ("* black:", black_win, ", white:", white_win, "\t*")
    print ("******************************************************")

