import gymnasium as gym
import numpy as np
import collections

env = gym.make("ALE/BattleZone-v5", render_mode=None, obs_type="ram")

actions = env.action_space.n

eps = 1
qTable = collections.defaultdict(float)
gamma = 0.4
lr = 0.1

def convert(n):
  out = 0
  for bit in n:
    out = (out << 1) | bit
  return out


def NextQ(qTable, state):
    qv = []
    for a in range(actions):
        qv.append(qTable[state + (a, )])
    return max(qv)


stats = []

for i in range(eps):
    totalEpReward = 0
    state = tuple(env.reset()[0])
    
    
    x = True
    while x:
        qv = []
        for i in range(actions):
            v = qTable[state + (i,)]
            if v > 0.0:
                print(v)
            qv.append(qTable[state + (i,)])
        #print(qv)

        action = env.action_space.sample()
        nstate, reward, done, trunc, i = env.step(action)
        nstate = tuple(nstate)
        totalEpReward += reward

        cstate = state + (action,)
        #print(cstate)
        qTable[cstate] = qTable[state, action] + lr * (reward + gamma * NextQ(qTable,nstate) - qTable[state, action])
        #v = qTable[cstate]

        state = nstate
        if done:
            break
        if trunc:
            break

    stats.append((i,totalEpReward))
    #print(qTable)