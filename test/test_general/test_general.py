import os
import pynetlogo
import pandas as pd
from pathlib import Path
from test_general_parameters import TestGeneralParametes
from test_general_parameters import NetlogoCommands
from test_general_parameters import calculate_fraction

modelfile = os.path.abspath('../../netlogo/FakeNewsSimulation.nlogo')


def load_sim_model():
    netlogo = pynetlogo.NetLogoLink(gui=False)

    print(">> Carico il modello NetLogo...")

    netlogo.load_model(modelfile)

    print(">> MODELLO CARICATO ")

    netlogoCommands = NetlogoCommands(netlogo, modelfile)

    return netlogo, netlogoCommands

def start_test(netlogo, netlogoCommands, testParameters):
    print(">> Recupero i parametri... ")
    # Recupera i parametri
    ticks = testParameters.total_ticks
    tresholds = testParameters.thresholds
    network_polarization = testParameters.network_polarization
    opinion_metric_steps = testParameters.opinion_metric_steps
    opinion_metric_value = testParameters.opinion_metric_value
    total_nodes = netlogoCommands.get_total_agents()
    total_ticks = netlogoCommands.get_total_ticks()
    opinion_polarization = testParameters.opinion_polarization
    number_of_iterations = testParameters.number_of_iterations
    print(f"NUMERO DI ITERAZIONI: {number_of_iterations}")
    netlogoCommands.set_opinion_polarization(opinion_polarization)
    netlogoCommands.set_initial_opinion_metric_value(opinion_metric_value)
    netlogoCommands.set_echo_chamber_fraction(TestGeneralParametes.echo_chamber_fraction)
    netlogoCommands.set_nodes(TestGeneralParametes.nb_nodes)
    netlogoCommands.set_total_ticks(TestGeneralParametes.total_ticks)

    print(">> PARAMETRI RECUPERATI ")

    global_cascades = []
    global_cascades_means = []
    df = pd.DataFrame({"Thresholds": [], "Network Polarization": [], 'Virality': []})

    for i in range(len(network_polarization)):
        netlogoCommands.set_network_polarization(network_polarization[i])
        print("P_N is set to: {}".format(netlogo.report("P_N")))
        for j in range(len(tresholds)):
            netlogoCommands.set_treshold(tresholds[j])
            print("teta is set to: {}".format(netlogo.report("teta")))
            global_cascades = []
            for k in range(number_of_iterations):
                netlogoCommands.setup()
                for l in range(ticks):
                    netlogoCommands.go()
                global_cascades.append(netlogoCommands.get_global_cascade_fraction())

            new_df = pd.DataFrame({"Thresholds": [tresholds[j]], "Network Polarization": [network_polarization[i]],
                                   'Virality': [calculate_fraction(global_cascades)]})
            df = pd.concat([df, new_df], ignore_index=True)
    print(">> TEST TERMINATO")
    print(">> Salvo i risultati...")
    filepath = Path(TestGeneralParametes.path + 'test_general_1.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f">> Risultati salvati in {TestGeneralParametes.path}")
    return df
