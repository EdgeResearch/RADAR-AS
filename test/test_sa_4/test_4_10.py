import os
import time
import pyNetLogo
import pandas as pd
from pathlib import Path
from environment.fake_news_diffusion_env import FakeNewsSimulation
from deepq_simulation import DeepQLearning
from test_4_parameters import *

netlogo = pyNetLogo.NetLogoLink(gui=False)
modelfile = os.path.abspath('netlogo/FakeNewsSimulation.nlogo')
netlogo.load_model(modelfile)
netlogoCommands = NetlogoCommands(netlogo, modelfile)
env = FakeNewsSimulation(netlogoCommands)

netlogoCommands = NetlogoCommands(netlogo, modelfile)
netlogoCommands.set_opinion_polarization(test_sa_4.opinion_polarization)
netlogoCommands.set_initial_opinion_metric_value(0.5)
netlogoCommands.set_echo_chamber_fraction(test_sa_4.echo_chamber_fraction)
netlogoCommands.set_opinion_metric_step(test_sa_4.opinion_metric_step)
netlogoCommands.set_nodes(test_sa_4.nb_nodes)
env.set_most_influent_a_nodes_criteria(test_sa_4.node_span, test_sa_4.choose_method)
netlogoCommands.set_warning(test_sa_4.warning)
netlogoCommands.set_warning_impact(test_sa_4.warning_impact)
netlogoCommands.set_warning_impact_neutral(test_sa_4.warning_impact_neutral)
netlogoCommands.set_node_range_static_b(test_sa_4.node_range_static_b)
netlogoCommands.set_treshold(test_sa_4.treshold)

total_nodes = netlogoCommands.get_total_agents()
total_ticks = netlogoCommands.get_total_ticks()

ticks = netlogoCommands.get_total_ticks()
ticks = int(ticks)
dql = DeepQLearning()

network_polarization = [test_sa_4.network_polarization[9]]
node_range = test_sa_4.node_range

global_cascades = []
global_cascades_means = []
df = pd.DataFrame({"Node Range": [], "Network Polarization": [],'Virality': []})

print("teta is set to: {}".format(netlogo.report("teta")))
start_time = time.time()

for i in range(len(network_polarization)):
    netlogoCommands.set_network_polarization(network_polarization[i])
    print("P_N is set to: {}".format(netlogo.report("P_N")))
    for j in range(len(node_range)):
        
        global_cascades = []
        
        netlogoCommands.set_node_range(test_sa_4.node_range[j])
        print("Node range is set to {}".format(netlogo.report("node-range")))

        print("Training model")
        dql.run_model_training(env, netlogoCommands, test_sa_4.number_of_iterations)

        print("Testing model")
        for k in range (test_sa_4.number_of_iterations):
            obs = env.reset()
            for l in range (ticks):
                if (l == 0):
                    obs, reward, terminated, done, info = env.step(0)
                elif (l % test_sa_4.sa_delay == 0):
                    obs, reward, terminated, done, info, action = dql.predict_sa_action(env, obs)
                else:
                    obs, reward, terminated, done, info = env.step(0)
            global_cascades.append(netlogoCommands.get_global_cascade_fraction())

        new_df = pd.DataFrame({"Node Range": [node_range[j]], "Network Polarization": [network_polarization[i]], 'Virality': [calculate_fraction(global_cascades)]})
        df = pd.concat([df, new_df], ignore_index=True)

total_time = (time.time() - start_time)/60
print("Total time %s minutes ---" % total_time)
filepath = Path(test_sa_4.path + 'test_10.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)

netlogo.kill_workspace()
