import gymnasium as gym
import numpy as np
import collections
import random
import pickle

env = gym.make("ALE/BattleZone-v5", render_mode="human", obs_type="ram")

actions = env.action_space.n

#qTable = collections.defaultdict(float)
hand = open("./dump.ql","rb")
qTable = pickle.load(hand)
hand.close()

eps = 1
gamma = 0.4
lr = 0.1
randAct = 0.0

def converter(n):
  out = 0
  for bit in n:
    out = (out << 1) | bit
  return out


def NextQ(qTable, state):
    qv = []
    for a in range(actions):
        qv.append(qTable[(state,a)])
    return max(qv)


stats = []

for i in range(eps):
    totalEpReward = 0
    state = converter(env.reset()[0])
    action = 0
    x = True
    while x:
        if random.uniform(0,1) > randAct:
            qv = []
            for i in range(actions):
                qv.append(qTable[(state,i)])
            action = np.argmax(qv)
        else:
            action = env.action_space.sample()

        nstate, reward, done, trunc, i = env.step(action)
        nextState = converter(nstate)
        
        cstate = (state,action)
        print(cstate)
        qTable[cstate] = qTable[cstate] + lr * (reward + gamma * NextQ(qTable,nextState) - qTable[cstate])

        totalEpReward += reward
        state = nextState
        if done:
            break
        if trunc:
            break



    stats.append((i,totalEpReward))
   #print(qTable)
f = open("./dump.ql","wb")
pickle.dump(qTable,f)
f.close()