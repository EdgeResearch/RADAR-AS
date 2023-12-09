import os
import pyNetLogo
from environment.fake_news_diffusion_env import FakeNewsSimulation
from netlogo.simulation_controls import NetlogoCommands

netlogo = pyNetLogo.NetLogoLink(gui=False)
modelfile = os.path.abspath('./netlogo/FakeNewsSimulation.nlogo')
netlogoCommands = NetlogoCommands(netlogo, modelfile)
env = FakeNewsSimulation(netlogoCommands)

env.set_most_influent_a_nodes_criteria(10, netlogoCommands.PAGERANK)
obs = env.reset()
print(env.observation_space.shape)

total_reward = 0

print(netlogoCommands.get_most_influent_a_nodes(env.node_span, env.criteria))
while True:
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    print("Action chosen : {}, Observation : {}, reward : {}".format(action, obs, reward))
    total_reward += reward

    if terminated == True:
        print("Total Reward: {} ".format(total_reward))
        env.reset()
        break

print("Done.")
env.close()
