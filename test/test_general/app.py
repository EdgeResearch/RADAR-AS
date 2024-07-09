import eel
import os
import time
import pandas as pd
import json
from test.test_general import test_general, utils
from test.test_general.test_general_parameters import TestGeneralParametes

dirname = os.path.dirname(__file__)
eel.init(os.path.join(dirname, "app/"))

@eel.expose
def submit(input):
    inputParameters = json.loads(input)
    testParameters = TestGeneralParametes()
    ticks = int(inputParameters['ticks'])
    iterations = int(inputParameters['iterations'])
    opinion_polarization = int(inputParameters['opinion_polarization'])
    network_polarization = inputParameters['network_polarization']
    thresholds = inputParameters['thresholds']

    network_polarization = [float(value) for value in network_polarization.split(",")]
    thresholds = [float(value) for value in thresholds.split(",")]

    print(f"Numero di Tick: {ticks}")
    print(f"Numero di Iterazioni: {iterations}")
    print(f"Opinion Polarization: {opinion_polarization}")
    print(f"Network Polarization: {network_polarization}")
    print(f"Tresholds Polarization: {thresholds}")

    testParameters.set_total_ticks(ticks)
    testParameters.set_number_of_iterations(iterations)
    testParameters.set_opinion_polarization(opinion_polarization)
    testParameters.set_network_polarization(network_polarization)
    testParameters.set_thresholds(thresholds)

    parameters = {"ticks": ticks, "iterations": iterations, "opinion_polarization": opinion_polarization,
                  "network_polarization": network_polarization, "thresholds": thresholds}

    netlogo, netlogoCommands = test_general.load_sim_model()
    dataframe = test_general.start_test(netlogo, netlogoCommands, testParameters)

    data_for_chart = utils.setup_data_for_chart(dataframe)
    print(f"Mando: {data_for_chart}")
    print("Spengo il sistema...")
    netlogo.kill_workspace()

    return data_for_chart




if __name__ == "__main__":
    eel.start("templates/homepage.html")
