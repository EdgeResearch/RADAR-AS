import sys
import eel
import os
import time
import pandas as pd
import json
from test.test_general import test_general_1, utils, test_general_2
from test.test_general.test_general_parameters import TestGeneralParametes
from test.test_general.utils import Tee

dirname = os.path.dirname(__file__)
eel.init(os.path.join(dirname, "app/"))

@eel.expose
def submit_test_1(input):
    testParameters = TestGeneralParametes()
    # Crea un istanza di Tee per gestire i log su terminale e file simultaneamente
    path = testParameters.path + "test_general_1/"
    testParameters.set_path(path)
    tee = Tee(testParameters.path + os.pathsep + 'log.txt')
    # Redirect sys.stdout to the tee object
    sys.stdout = tee
    path = testParameters.path + os.pathsep + "test_general_1"
    try:
        inputParameters = json.loads(input)
        ticks = int(inputParameters['ticks'])
        iterations = int(inputParameters['iterations'])
        opinion_polarization = float(inputParameters['opinion_polarization'])
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

        netlogo, netlogoCommands = test_general_1.load_sim_model()
        dataframe, img_chart = test_general_1.start_test_1(netlogo, netlogoCommands, testParameters)

        data_for_chart = utils.setup_data_for_chart(dataframe, "Thresholds")

        print("Spengo il sistema...")
        netlogo.kill_workspace()

        # Get the captured output from the string buffer
        output = tee.get_value()
    finally:
        # Reimposta sys.stdout al valore originale (terminale)
        sys.stdout = tee.stdout
        tee.close()

    response = {
        "data_for_chart" : data_for_chart,
        "img_chart" : img_chart,
        "log_output" : output
    }

    jsonResponse = json.dumps(response)

    return jsonResponse

@eel.expose
def submit_test_2(input):
    testParameters = TestGeneralParametes()
    path = testParameters.path + "test_general_2/"
    testParameters.set_path(path)
    # Crea un istanza di Tee per gestire i log su terminale e file simultaneamente
    tee = Tee(testParameters.path + os.pathsep + 'log.txt')
    # Redirect sys.stdout to the tee object
    sys.stdout = tee
    try:
        inputParameters = json.loads(input)
        ticks = int(inputParameters['ticks'])
        iterations = int(inputParameters['iterations'])
        opinion_polarization = float(inputParameters['opinion_polarization'])
        network_polarization = inputParameters['network_polarization']
        threshold = inputParameters['thresholds']
        nb_nodes = inputParameters['nodes']

        network_polarization = [float(value) for value in network_polarization.split(",")]
        nb_nodes = [int(value) for value in nb_nodes.split(",")]

        print(f"Numero di Tick: {ticks}")
        print(f"Numero di Iterazioni: {iterations}")
        print(f"Opinion Polarization: {opinion_polarization}")
        print(f"Network Polarization: {network_polarization}")
        print(f"Treshold: {threshold}")
        print(f"Numero di Nodi {nb_nodes}")

        testParameters.set_total_ticks(ticks)
        testParameters.set_number_of_iterations(iterations)
        testParameters.set_opinion_polarization(opinion_polarization)
        testParameters.set_network_polarization(network_polarization)
        testParameters.set_thresholds(threshold)
        testParameters.set_nb_nodes(nb_nodes)

        netlogo, netlogoCommands = test_general_2.load_sim_model()
        dataframe, img_chart = test_general_2.start_test_2(netlogo, netlogoCommands, testParameters)

        data_for_chart = utils.setup_data_for_chart(dataframe, "Nodes")

        print("Spengo il sistema...")
        netlogo.kill_workspace()

        # Get the captured output from the string buffer
        output = tee.get_value()
    finally:
        # Reimposta sys.stdout al valore originale (terminale)
        sys.stdout = tee.stdout
        tee.close()

    response = {
        "data_for_chart" : data_for_chart,
        "img_chart" : img_chart,
        "log_output" : output
    }

    jsonResponse = json.dumps(response)

    return jsonResponse



if __name__ == "__main__":
    eel.start("templates/homepage.html")
