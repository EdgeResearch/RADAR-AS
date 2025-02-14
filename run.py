import os
import pynetlogo
from environment.fake_news_diffusion_env import FakeNewsSimulation
from netlogo.simulation_controls import NetlogoCommands

netlogo = pynetlogo.NetLogoLink(gui=True)
modelfile = os.path.abspath('./netlogo/FakeNewsSimulation.nlogo')
netlogo.load_model(modelfile)
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
    print("Positive emotions : {:.0f}, Negative emotions : {:.0f}, Neutral emotions : {:.0f}".format(
        netlogoCommands.get_positive_emotions(), netlogoCommands.get_negative_emotions(), netlogoCommands.get_neutral_emotions()))
    print("--------------------------------")
    total_reward += reward

    if terminated == True:
        print("Total Reward: {} ".format(total_reward))
        env.reset()
        break
print("Done.")
