#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np
np.random.seed(0)
from rlglue.environment.Environment import Environment
from rlglue.environment import EnvironmentLoader as EnvironmentLoader
from rlglue.types import Observation
from rlglue.types import Reward_observation_terminal

import Player
import ReverseCommon
import ReverseBoard

class RevarsEnvironment(Environment):
    # 盤の状態 [空白, ○, ×]
    flg_free = 0
    flg_agent = 1
    flg_env = 2
    # 報酬
    r_win = 1.0
    r_draw = -0.5
    r_lose = -1.0
    # 敵プレイヤーが正常に打つ確率
    opp = 0.75

    #
    def __init__(self):
        print("__init__")
        self.n_rows = 8
        self.n_cols = self.n_rows
        self.history = []


    # RL_Glueの設定を行う。
    def env_init(self):
        print("env_init")
        # OBSERVATONS INTS = 盤の状態 (0 ~ 2 の値が 64次元)  ex) (0,0,0,0,0,0,0,0,
        #                                                         0,0,0,0,0,0,0,0,
        #                                                         0,0,0,0,0,0,0,0,
        #                                                         0,0,0,1,2,0,0,0,
        #                                                         0,0,0,2,1,0,0,0,
        #                                                         0,0,0,0,0,0,0,0,
        #                                                         0,0,0,0,0,0,0,0,
        #                                                         0,0,0,0,0,0,0,0)
        # ACTIONS INTS = ○を打つ場所を指定 (0 ~ 64)
        # REWARDS = 報酬 (-1.0 ~ 1.0)   ex) 勝 1, 引分 -0.5, 負 -1
        wresult = 'VERSION RL-Glue-3.0 PROBLEMTYPE episodic DISCOUNTFACTOR 0.99 OBSERVATIONS INTS (' 
        wresult += str(self.n_rows * self.n_cols) + ' 0 1) ACTIONS INTS (0 ' + str(self.n_rows * self.n_cols -1) + ') REWARDS (-1.0 1.0)'
        wresult += ' SENTEFLG 100'
 
        return wresult 

    # Episodeの開始
    def env_start(self):
        print("="*3 + "  env_start  " + "="*3)
        # 盤面作成
        self.reverse_board = ReverseBoard.ReverseBoard(self.n_rows)

        # 盤面を初期化
        self.map = self.reverse_board.board.ravel().tolist()

        # 盤の状態を保持し、最後に確認するためのリスト
        self.history = []
        self.history.append(ReverseCommon.getboardinfo(self.reverse_board.board,True))
        ReverseCommon.print_board(self.reverse_board.board)

        # プレイヤー
        #self.agent_player = Player.RandomAi(ReverseCommon.BLACK)
        self.agent_player = Player.NextStoneMaxAi(ReverseCommon.BLACK)
        #self.agent_player = Player.RandomAiKnowGoodMove(ReverseCommon.BLACK)
        #self.env_player = Player.RandomAi(ReverseCommon.WHITE)
        #self.env_player = Player.Human(ReverseCommon.WHITE)
        #self.env_player = Player.NextStoneMaxAi(ReverseCommon.WHITE)
        self.env_player = Player.RandomAiKnowGoodMove(ReverseCommon.WHITE)

        # 盤の状態をRL_Glueを通してエージェントに渡す
        observation = Observation()
        observation.intArray = self.map

        return observation

    def env_step(self, action):
        #print("env_step")
        # エージェントから受け取った○を打つ場所
        int_action_agent = action.intArray[0]
        # 盤に○を打
        self.map[int_action_agent] = self.flg_agent
        print("int_action_agent=%d" % int_action_agent)


        rot = Reward_observation_terminal()
        rot.r = 0.0
        rot.terminal = False

        # 置けなくなったら終了
        if self.reverse_board.is_game_set():
           ReverseCommon.history_write(self.history)
           env_score = ReverseCommon.get_score(self.reverse_board.board, self.env_player.color)
           agent_score = ReverseCommon.get_score(self.reverse_board.board, self.agent_player.color)
           if env_score == agent_score :
              rot.r = self.r_draw
           elif env_score >  agent_score: 
              rot.r = self.r_win
           else:
              rot.r = self.r_lose

           rot.terminal = True
           print("env_score=%d  agent_score=%d" % (env_score,agent_score))
           return rot

        # プレーヤ1(agent)
        if self.reverse_board.is_my_turn(self.agent_player.color):
           next_move = self.agent_player.next_move(self.reverse_board.board)
           self.reverse_board.put_stone(self.agent_player.color, next_move[0], next_move[1])
           self.history.append(ReverseCommon.getboardinfo(self.reverse_board.board,True))
           ReverseCommon.print_board(self.reverse_board.board)


        # 置けなくなったら終了
        if self.reverse_board.is_game_set():
           ReverseCommon.history_write(self.history)
           env_score = ReverseCommon.get_score(self.reverse_board.board, self.env_player.color)
           agent_score = ReverseCommon.get_score(self.reverse_board.board, self.agent_player.color)
           if env_score == agent_score :
              rot.r = self.r_draw
           elif env_score >  agent_score: 
              rot.r = self.r_win
           else:
              rot.r = self.r_lose

           rot.terminal = True
           print("env_score=%d  agent_score=%d" % (env_score,agent_score))
           return rot


        #if n_free == 0:
        #   rot.terminal = True

        #if not rot.terminal:
        #   int_action_env = None
        #   # 空白が1個所ならばそこに×を打つ
        #   if n_free == 1:
        #      int_action_env = free[0]
        #      rot.terminal = True
        #   else:
        #      int_action_env = free[np.random.randint(n_free)]

           # 盤に×を打つ
        #   self.map[int_action_env] = self.flg_env
           #print("int_action_env=%d" % int_action_env)

        # 空白の個所を取得する
        #free = [i for i, v in enumerate(self.map) if v == self.flg_free]
        #n_free = len(free)

        # 盤の状態と報酬、決着がついたかどうか をまとめて エージェントにおくる。
        observation = Observation()
        observation.intArray = self.map
        rot.o = observation

        # プレーヤ2(env)
        if self.reverse_board.is_my_turn(self.env_player.color):
           next_move = self.env_player.next_move(self.reverse_board.board)
           self.reverse_board.put_stone(self.env_player.color, next_move[0], next_move[1])
           self.history.append(ReverseCommon.getboardinfo(self.reverse_board.board,True))
           ReverseCommon.print_board(self.reverse_board.board)


        # 置けなくなったら終了
        if self.reverse_board.is_game_set():
           ReverseCommon.history_write(self.history)
           env_score = ReverseCommon.get_score(self.reverse_board.board, self.env_player.color)
           agent_score = ReverseCommon.get_score(self.reverse_board.board, self.agent_player.color)
           if env_score == agent_score :
              rot.r = self.r_draw
           elif env_score >  agent_score: 
              rot.r = self.r_win
           else:
              rot.r = self.r_lose

           rot.terminal = True
           print("env_score=%d  agent_score=%d" % (env_score,agent_score))
           return rot

        self.map = self.reverse_board.board.ravel().tolist()
        observation.intArray = self.map
        rot.o = observation

        # 決着がついた場合は agentのagent_end
        # 決着がついていない場合は agentのagent_step に続く
        return rot


    def env_cleanup(self):
        print("env_cleanup")
        #pass

    def env_message(self, message):
        print("env_message")
        #pass


if __name__ == '__main__':
    EnvironmentLoader.loadEnvironment(RevarsEnvironment())
