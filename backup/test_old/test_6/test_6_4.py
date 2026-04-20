import os
import pyNetLogo
import pandas as pd
from pathlib import Path
from test_6_parameters import *
import numpy as np
from collections import defaultdict

netlogo = pyNetLogo.NetLogoLink(gui=False)
modelfile = os.path.abspath('netlogo/FakeNewsSimulation.nlogo')
netlogo.load_model(modelfile)
netlogoCommands = NetlogoCommands(netlogo, modelfile)

netlogoCommands.set_opinion_polarization(test_6.opinion_polarization)
netlogoCommands.set_initial_opinion_metric_value(0.5)
netlogoCommands.set_echo_chamber_fraction(test_6.echo_chamber_fraction)
netlogoCommands.set_treshold(test_6.treshold)
netlogoCommands.set_network_polarization(test_6.network_polarization)
netlogoCommands.set_opinion_metric_step(test_6.opinion_metric_step)
netlogoCommands.set_nodes(test_6.nb_nodes)

total_nodes = netlogoCommands.get_total_agents()
total_ticks = netlogoCommands.get_total_ticks()

df = pd.DataFrame({"A Agents": [], "B Agents": [], "Neutral Agents": [], "A Var": [], "B Var": [], "N Var": []})

print("Test 6 with echo chamber fraction {}".format(test_6.echo_chamber_fraction))
print("PO is set to {}".format(test_6.opinion_polarization))
print("teta is set to: {}".format(netlogo.report("teta")))

a_nodes = defaultdict(list)
b_nodes = defaultdict(list)
neutral_nodes = defaultdict(list)
a = []
b = []
n = []
a_var = []
b_var = []
n_var = []

for i in range(test_6.number_of_iterations):
    netlogoCommands.setup()
    current_tick = netlogoCommands.get_current_tick()
    a_nodes[current_tick].append(netlogoCommands.get_a_active_agents())
    b_nodes[current_tick].append(netlogoCommands.get_b_active_agents())
    neutral_nodes[current_tick].append(netlogoCommands.get_neutral_agents())
    for l in range (total_ticks):
        netlogoCommands.go()
        if (netlogoCommands.get_current_tick() % 10 == 0):
            current_tick = netlogoCommands.get_current_tick()
            a_nodes[current_tick].append(netlogoCommands.get_a_active_agents())
            b_nodes[current_tick].append(netlogoCommands.get_b_active_agents())
            neutral_nodes[current_tick].append(netlogoCommands.get_neutral_agents())

for m in a_nodes:
    a.append(sum(a_nodes[m]) / len(a_nodes[m]))
    b.append(sum(b_nodes[m]) / len(b_nodes[m]))
    n.append(sum(neutral_nodes[m]) / len(neutral_nodes[m]))
    a_var.append(np.std(a_nodes[m]))
    b_var.append(np.std(b_nodes[m]))
    n_var.append(np.std(neutral_nodes[m]))

df = pd.DataFrame({ "A Agents": a, "B Agents": b, "Neutral Agents": n, "A Var": a_var, "B Var": b_var, "N Var": n_var})

filepath = Path(test_6.path + 'test_6_4.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)

netlogo.kill_workspace()