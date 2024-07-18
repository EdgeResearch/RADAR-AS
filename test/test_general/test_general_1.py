import os
import pynetlogo
import pandas as pd
from pathlib import Path
import io
import base64
from matplotlib import pyplot as plt

from test_general_parameters import TestGeneralParametes
from test_general_parameters import NetlogoCommands
from test_general_parameters import calculate_fraction

def load_sim_model():
    modelfile = os.path.abspath('../../netlogo/FakeNewsSimulation.nlogo')
    netlogo = pynetlogo.NetLogoLink(gui=False)

    print(">> Carico il modello NetLogo...")

    netlogo.load_model(modelfile)

    print(">> MODELLO CARICATO ")

    netlogoCommands = NetlogoCommands(netlogo, modelfile)

    return netlogo, netlogoCommands


def start_test_1(netlogo, netlogoCommands, testParameters):
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
    filepath = Path(testParameters.path + 'test_general_1.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f">> Risultati salvati in {TestGeneralParametes.path}")

    print(f">> Creo il grafico...")
    img_chart = plot_chart(testParameters)
    print(f">> Grafico creato e salvato in  {TestGeneralParametes.path}")
    return df, img_chart

def plot_chart(testParameters):
    thresholds = testParameters.thresholds
    markers = ['o-', 's--', 'D:']
    colorarray=['black', 'dimgrey', 'grey']

    path = testParameters.path
    df = pd.read_csv(path + 'test_general_1.csv')

    x_values = []
    y_values = []

    for i in range(len(thresholds)):
        x = df.loc[df['Thresholds'] == thresholds[i]]
        x_values.append(x.loc[:, "Network Polarization"])
        y_values.append(x.loc[:, "Virality"])

    fig=plt.figure(figsize=(10, 5))
    plt.rcParams.update({'font.size': 18})
    ax=plt.subplot(111)

    for i in range (len(thresholds)):
        if (i > 4 and i < 10):
            ax.plot(x_values[i], y_values[i], markers[i], fillstyle = "none" , label=thresholds[i], color = colorarray[i])
        else:
            ax.plot(x_values[i], y_values[i], markers[i], label=thresholds[i], color = colorarray[i])


    plt.ylabel("Virality (Global Cascade fraction)")
    plt.xlabel("Pn (Network Polarization)")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="\u03B8 (threshold)")
    plt.grid(visible=True, linewidth=0.2)

    filepath = Path(path + 'test_1_result.pdf')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, bbox_inches='tight')

    # Salvare il grafico in un oggetto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    # Convertire il contenuto del buffer in una stringa base64
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return img_base64