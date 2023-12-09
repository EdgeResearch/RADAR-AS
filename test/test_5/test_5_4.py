import os
import pyNetLogo
import pandas as pd
from pathlib import Path
from test_5_parameters import *

netlogo = pyNetLogo.NetLogoLink(gui=False)
modelfile = os.path.abspath('netlogo/FakeNewsSimulation.nlogo')
netlogo.load_model(modelfile)
netlogoCommands = NetlogoCommands(netlogo, modelfile)

treshold = test_5.treshold
network_polarization = test_5.network_polarization[9:]
opinion_metric_steps = test_5.opinion_metric_steps

total_nodes = netlogoCommands.get_total_agents()
total_ticks = netlogoCommands.get_total_ticks()

netlogoCommands.set_opinion_polarization(test_5.opinion_polarization)
netlogoCommands.set_initial_opinion_metric_value(0.5)
netlogoCommands.set_echo_chamber_fraction(test_5.echo_chamber_fraction)
netlogoCommands.set_treshold(treshold)
netlogoCommands.set_nodes(test_5.nb_nodes)
netlogoCommands.set_total_ticks(test_5.total_ticks)

global_cascades = []
global_cascades_means = []
df = pd.DataFrame({"Opinion Metric Step": [], "Network Polarization": [],'Virality': []})
print("Test 5 with echo chamber fraction {}".format(test_5.echo_chamber_fraction))
print("PO is set to {}".format(test_5.opinion_polarization))

print("teta is set to: {}".format(netlogo.report("teta")))
print("total ticks: {}".format(total_ticks))

for i in range(len(network_polarization)):
    netlogoCommands.set_network_polarization(network_polarization[i])
    print("P_N is set to: {}".format(netlogo.report("P_N")))
    for j in range(len(opinion_metric_steps)):
        netlogoCommands.set_opinion_metric_step(opinion_metric_steps[j])
        print("opinion-metric-step is set to: {}".format(netlogo.report("opinion-metric-step")))
        global_cascades = []
        for k in range (test_5.number_of_iterations):
            netlogoCommands.setup()
            for l in range (test_5.total_ticks):
                netlogoCommands.go()
            global_cascades.append(netlogoCommands.get_global_cascade_fraction())

        new_df = pd.DataFrame({"Opinion Metric Step": [opinion_metric_steps[j]], "Network Polarization": [network_polarization[i]], 'Virality': [calculate_fraction(global_cascades)]})
        df = pd.concat([df, new_df], ignore_index=True)

filepath = Path(test_5.path + 'test_5_4.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)

netlogo.kill_workspace()
