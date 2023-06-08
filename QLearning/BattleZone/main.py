import gymnasium as gym
import numpy as np
import collections
import random
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mode",   default=None,   help="Render mode: human/None")
parser.add_argument("--epoch",  default=10,     help="Iterations.", type=int)
parser.add_argument("--load",   default="dump.ql")
parser.add_argument("--save",   default="dump.ql", help="File to save the model.")
parser.add_argument("--randact",default=0.5, help="Random action.")
parser.add_argument("--dict",   default="disk", help="Dict ram/disk.")
args = parser.parse_args()


def converter(n):
  out = 0
  for bit in n:
    out = (out << 1) | bit
  return out


def NextQ(qTable, state, actions):
    qv = []
    for a in range(actions):
        qv.append(qTable[(state,a)])
    return max(qv)

def main(eps,gamma,lr,randAct,qTable,env,actions):
    stats = []
    doneTax = 0
    truncTax = 0

    for i in range(0,eps):
        totalEpReward = 0
        state = converter(env.reset()[0])
        action = 0
        x = True
        while x:
            if random.uniform(0,1) > randAct:
                qv = []
                for j in range(actions):
                    qv.append(qTable[(state,j)])
                action = np.argmax(qv)
            else:
                action = env.action_space.sample()

            nstate, reward, done, trunc, info = env.step(action)
            nextState = converter(nstate)
            
            cstate = (state,action)
            qTable[cstate] = qTable[cstate] + lr * (reward + gamma * NextQ(qTable,nextState,actions) - qTable[cstate])

            totalEpReward += reward
            state = nextState
            if done:
                doneTax+=1
                break
            if trunc:
                truncTax+=1
                break
        stats.append((i,totalEpReward,doneTax,truncTax))
        #if i%10 == 0:
        print("Iteration:",i," Total Rewards:",totalEpReward," Done:",doneTax," Trunc:",truncTax)
    mts = open("metrics.txt","wb")
    pickle.dump(stats,mts)
    mts.close()
    return qTable

env = gym.make("ALE/BattleZone-v5", render_mode=args.mode, obs_type="ram")
actions = env.action_space.n

qTable = None
if args.dict == "disk":
    hand = open(args.load,"rb")
    qTable = pickle.load(hand)
    hand.close()
elif args.dict == "ram":
    print("Problems opening file model, loading in memory training.")
    qTable = collections.defaultdict(float)
else:
    exit(1)

eps = args.epoch
gamma = 0.4
lr = 0.1
randAct = 0.0

qt = main(eps,gamma,lr,randAct,qTable,env,actions)
f = open(args.save,"wb")
pickle.dump(qt,f)
f.close()