import gymnasium as gym
import numpy as np
import collections

env = gym.make("ALE/BattleZone-v5", render_mode="human", obs_type="ram")

actions = env.action_space.n

eps = 1
qTable = collections.defaultdict(float)
gamma = 0.4
lr = 0.1

"""def conf(state):
    o = 0
    for b in state:
        for x in b:
            o = (o << 1) & x
    return o"""

def NextQ(qTable, state):
    return np.max(qTable[state, :])


stats = []

for i in range(eps):
    totalEpReward = 0
    state = tuple(env.reset()[0])
    
    x = True
    while x:
        action = env.action_space.sample()
        nstate, reward, done, trunc, i = env.step(action)
        nstate = tuple(nstate)
        totalEpReward += reward

        cstate = state + (action,)
        #print(cstate)
        qTable[cstate] = (1 - lr) * qTable[state, action] + gamma * (reward - qTable[state, action])

    stats.append((i,totalEpReward))
    print(qTable)