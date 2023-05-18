import gymnasium as gym
import numpy as np
import random
import collections
import pickle

env = gym.make("LunarLander-v2", render_mode="human")
#observation, info = env.reset()

#actionN = env.action_space.n
#stateN  = env.observation_space.n
#q_table = np.zeros((stateN,actionN))

def discretize_state(state):
    discrete_state = (min(2, max(-2, int((state[0]) / 0.05))), \
                        min(2, max(-2, int((state[1]) / 0.1))), \
                        min(2, max(-2, int((state[2]) / 0.1))), \
                        min(2, max(-2, int((state[3]) / 0.1))), \
                        min(2, max(-2, int((state[4]) / 0.1))), \
                        min(2, max(-2, int((state[5]) / 0.1))), \
                        int(state[6]), \
                        int(state[7]))

    return discrete_state

def NextQ(states, state, num_actions):
    qv = []
    for a in range(num_actions):
        qv.append(states[state + (a, )])
    return max(qv)

#q_table = collections.defaultdict(float)
hand = open("./dump.ql", "rb")
q_table=pickle.load(hand)

lr = 0.3
gamma = 0.7
eps = 100
expRate = 0.0
numActions = env.action_space.n
c = 0
tdone=0
terr=0
for i in range(eps):
    c=c+1
    state = discretize_state(env.reset()[0])
    x = True
    
    while x:
        if random.uniform(0,1) > expRate:
            qv = []
            for a in range(numActions):
                qv.append(q_table[state + (a, )])
            action = np.argmax(qv)
        else:
            action = env.action_space.sample()
        cstate = state + (action, )
        #print(cstate)
        
        nstate,r,done,t,i = env.step(action)
        nstate = discretize_state(nstate)
        q_table[cstate] = q_table[cstate] + lr * (r + gamma * NextQ(q_table, nstate, numActions) - q_table[cstate])
        
        state = nstate
        if done:
            tdone+=1
            break
        if t:
            terr+=1
            break
    print("----------------------------------------------------------------\n\nNew table:",
    q_table,"\nNumber: ",c,"\nDone: ",tdone," Error: ",terr)
env.close()

f = open("./dump.ql", "wb")
pickle.dump(q_table,f)
f.close()

