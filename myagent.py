#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import copy

import numpy as np
np.random.seed(0)
from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.types import Observation
from rlglue.utils import TaskSpecVRLGLUE3

import Player
import ReverseCommon


# エージェントクラス
class RevaseAgent(Agent):

    # エージェントの初期化
    # 学習の内容を定義する
    def __init__(self, gpu):
        print("__init__")
        # 盤の情報
        self.n_rows = 8
        self.n_cols = self.n_rows

        # 学習のInputサイズ
        self.dim = self.n_rows * self.n_cols
        self.bdim = self.dim * 2

        self.gpu = gpu

        # 学習を開始させるステップ数
        self.learn_start = 5 * 10**3

        # 保持するデータ数
        self.capacity = 1 * 10**4

        # eps = ランダムに○を決定する確率
        self.eps_start = 1.0
        self.eps_end = 0.001
        self.eps = self.eps_start

        # 学習時にさかのぼるAction数
        self.n_frames = 3

        # 一度の学習で使用するデータサイズ
        self.batch_size = 32

        self.replay_mem = []
        self.last_state = None
        self.last_action = None
        self.reward = None
        self.state = np.zeros((1, self.n_frames, self.bdim)).astype(np.float32)

        self.step_counter = 0

        self.update_freq = 1 * 10**4

        self.r_win = 1.0
        self.r_draw = -0.5
        self.r_lose = -1.0

        self.frozen = False

        self.win_or_draw = 0
        self.stop_learning = 200


    # ゲーム情報の初期化
    def agent_init(self, task_spec_str):
        print("agent_init::::::")
        ReverseCommon.TaskSpecDisplay(task_spec_str)
        task_spec = TaskSpecVRLGLUE3.TaskSpecParser(task_spec_str)

        if not task_spec.valid:
            raise ValueError(
                'Task spec could not be parsed: {}'.format(task_spec_str))

        self.gamma = task_spec.getDiscountFactor()

    # environment.py env_startの次に呼び出される。
    # 1手目の○を決定し、返す
    def agent_start(self, observation):
        print("agent_start")
        # プレイヤ
        self.player = Player.NextStoneMaxAi(ReverseCommon.BLACK)

        # stepを1増やす
        self.step_counter += 1
        # observationを[0-2]の9ユニットから[0-1]の18ユニットに変換する
        self.update_state(observation)

        # ○の場所を決定する
        int_action = self.select_int_action()
        action = Action()
        action.intArray = [int_action]

        return action

    # エージェントの二手目以降、ゲームが終わるまで
    def agent_step(self, reward, observation):
        #print("agent_step")
        # ステップを1増加
        self.step_counter += 1
        self.update_state(observation)

        # ○の場所を決定
        int_action = self.select_int_action()
        action = Action()
        action.intArray = [int_action]
        self.reward = reward

        # ○の位置をエージェントへ渡す
        return action

    # ゲームが終了した時点で呼ばれる
    def agent_end(self, reward):
        print("agent_end")
        # 環境から受け取った報酬
        self.reward = reward


    def agent_cleanup(self):
        print("agent_cleanup")
        #pass

    def agent_message(self, message):
        print("gent_message")
        #pass


    def update_state(self, observation=None):
        if observation is None:
            frame = np.zeros(1, 1, self.bdim).astype(np.float32)
        else:
            observation_binArray = []

            for int_observation in observation.intArray:
                bin_observation = '{0:02b}'.format(int_observation)
                observation_binArray.append(int(bin_observation[0]))
                observation_binArray.append(int(bin_observation[1]))

            frame = (np.asarray(observation_binArray).astype(np.float32)
                                                     .reshape(1, 1, -1))
        self.state = np.hstack((self.state[:, 1:], frame))


    def select_int_action(self):
        free = []
        bits = self.state[0, -1]

        for i in range(0, len(bits), 2):
            if bits[i] == 0 and bits[i+1] == 0:
                free.append(int(i / 2))

        int_action = free[np.random.randint(len(free))]

        #print("int_action::" + str(int_action) + "  free::" + str(free) ) 
        return int_action


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deep Q-Learning')
    parser.add_argument('--gpu', '-g', default=-1, type=int,
                        help='GPU ID (negative value indicates CPU)')
    args = parser.parse_args()

    AgentLoader.loadAgent(RevaseAgent(args.gpu))
