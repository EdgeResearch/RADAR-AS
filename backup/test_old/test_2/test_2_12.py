import os
import numpy as np
import pyNetLogo
import pandas as pd
from pathlib import Path
from test_2_parameters import *

netlogo = pyNetLogo.NetLogoLink(gui=False)
modelfile = os.path.abspath('netlogo/FakeNewsSimulation.nlogo')
netlogo.load_model(modelfile)
netlogoCommands = NetlogoCommands(netlogo, modelfile)

ticks = netlogoCommands.get_total_ticks()
ticks = int(ticks)

nodes = test_2.nodes
network_polarization = [test_2.network_polarization[11]]

netlogoCommands.set_opinion_polarization(test_2.opinion_polarization)
netlogoCommands.set_treshold(test_2.treshold)

global_cascades = []
global_cascades_means = []

df = pd.DataFrame({"Nodes": [], "Network Polarization": [],'Virality': []})

for i in range(len(network_polarization)):
    netlogoCommands.set_network_polarization(network_polarization[i])
    print("P_N is set to: {}".format(netlogo.report("P_N")))
    for j in range(len(nodes)):
        netlogoCommands.set_nodes(nodes[j])
        print("nb-nodes is set to: {}".format(netlogo.report("nb-nodes")))
        global_cascades = []
        for k in range (test_2.number_of_iterations):
            netlogoCommands.setup()
            for l in range (ticks):
                netlogoCommands.go()
            global_cascades.append(netlogoCommands.get_global_cascade_fraction())

        new_df = pd.DataFrame({"Nodes": [nodes[j]], "Network Polarization": [network_polarization[i]], 'Virality': [calculate_fraction(global_cascades)]})
        df = pd.concat([df, new_df], ignore_index=True)

filepath = Path(test_2.path + 'test_2_12.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)

netlogo.kill_workspace()
