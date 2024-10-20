import os
import sys
import time

import pynetlogo
import pandas as pd
from pathlib import Path
import io
import base64
from matplotlib import pyplot as plt

sys.path.insert(1, f'.{os.sep}test_general_sa_1')
from test_general_parameters_sa import SuperAgentTestGeneralParametes
from test_general_parameters_sa import NetlogoCommands
from test_general_parameters_sa import calculate_fraction
from environment.fake_news_diffusion_env import FakeNewsSimulation
from deepq_simulation import DeepQLearning

modelfile = os.path.abspath('test_general_sa_1/netlogo/FakeNewsSimulation.nlogo')


def load_sim_model():
    netlogo = pynetlogo.NetLogoLink()

    netlogo.load_model(modelfile)

    netlogoCommands = NetlogoCommands(netlogo, modelfile)

    return netlogo, netlogoCommands


def start_test_sa_1(netlogo, netlogoCommands, testParameters):
    print(">> Retrieving the parameters... ")
    # Recupera i parametri
    ticks = testParameters.total_ticks
    tresholds = testParameters.thresholds
    network_polarization = testParameters.network_polarization
    opinion_metric_step = testParameters.opinion_metric_step
    opinion_metric_value = testParameters.opinion_metric_value
    total_nodes = netlogoCommands.get_total_agents()
    total_ticks = netlogoCommands.get_total_ticks()
    opinion_polarization = testParameters.opinion_polarization
    number_of_iterations = testParameters.number_of_iterations

    warning = testParameters.warning
    node_range_static_b = testParameters.node_range_static_b
    node_range = testParameters.node_range
    choose_method = testParameters.choose_method
    warning_impact = testParameters.warning_impact
    warning_impact_neutral = testParameters.warning_impact_neutral
    sa_delay = testParameters.sa_delay
    print(">> Parameters Retrieved")


    env = FakeNewsSimulation(netlogoCommands)

    netlogoCommands = NetlogoCommands(netlogo, modelfile)
    netlogoCommands.set_opinion_polarization(opinion_polarization)
    netlogoCommands.set_initial_opinion_metric_value(0.5)
    netlogoCommands.set_echo_chamber_fraction(testParameters.echo_chamber_fraction)
    netlogoCommands.set_opinion_metric_step(opinion_metric_step)
    netlogoCommands.set_nodes(testParameters.nb_nodes)
    env.set_most_influent_a_nodes_criteria(10, choose_method)
    netlogoCommands.set_warning(warning)
    netlogoCommands.set_node_range_static_b(node_range_static_b)
    netlogoCommands.set_node_range(node_range)
    netlogoCommands.set_warning_impact(warning_impact)
    netlogoCommands.set_warning_impact_neutral(warning_impact_neutral)

    total_nodes = netlogoCommands.get_total_agents()
    total_ticks = netlogoCommands.get_total_ticks()

    ticks = netlogoCommands.get_total_ticks()
    ticks = int(ticks)

    dql = DeepQLearning()

    global_cascades = []
    global_cascades_means = []
    df = pd.DataFrame({"Thresholds": [], "Network Polarization": [], 'Virality': []})
    start_time = time.time()

    for i in range(len(network_polarization)):
        netlogoCommands.set_network_polarization(network_polarization[i])
        print("P_N is set to: {}".format(netlogo.report("P_N")))
        for j in range(len(tresholds)):
            netlogoCommands.set_treshold(tresholds[j])
            print("teta is set to: {}".format(netlogo.report("teta")))
            global_cascades = []

            print("Training model")

            dql.run_model_training(env, netlogoCommands, number_of_iterations)

            print("Testing model")
            for k in range(number_of_iterations):
                obs = env.reset()
                for l in range(ticks):
                    if l == 0:
                        obs = env.step(0)
                    elif l % sa_delay == 0:
                        obs = dql.predict_sa_action(env, obs)
                    else:
                        obs = env.step(0)
                global_cascades.append(netlogoCommands.get_global_cascade_fraction())

            new_df = pd.DataFrame({"Thresholds": [tresholds[j]], "Network Polarization": [network_polarization[i]],
                                   'Virality': [calculate_fraction(global_cascades)]})
            df = pd.concat([df, new_df], ignore_index=True)

    total_time = (time.time() - start_time) / 60
    print("Total time %s minutes ---" % total_time)

    print(">> Salvo i risultati...")
    filepath = Path(testParameters.path + 'test_general_sa_1.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(">> Saving the results...")

    print(f">> Creating the graph...")
    img_chart, image_chart_path = plot_chart(testParameters)
    print(f">> Graph created and saved in   {SuperAgentTestGeneralParametes.path}")

    data_to_return = {
        "dataframe": df,
        "img_chart_web" : img_chart,
        "dataset_filepath": filepath,
        "result_chart_filepath": image_chart_path
    }

    return data_to_return

def plot_chart(testParameters):
    colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

    tresholds = testParameters.thresholds

    markers = ['o-', 's--', 'D:', "^-", "v--", "o--", "s-", "D--", "^:", "v-", "o--", "s:"]

    path = testParameters.path
    df = pd.read_csv(path + 'test_general_sa_1.csv')

    x_values = []
    y_values = []

    for i in range(len(tresholds)):
        x = df.loc[df['Thresholds'] == tresholds[i]]
        x_values.append(x.loc[:, "Network Polarization"])
        y_values.append(x.loc[:, "Virality"])

    fig=plt.figure(figsize=(10, 5))
    plt.rcParams.update({'font.size': 18})
    ax=plt.subplot(111)

    for i in range (len(tresholds)):
        if (i > 4 and i < 10):
            ax.plot(x_values[i], y_values[i], markers[i], fillstyle = "none" , label=tresholds[i], color = colorarray[i])
        else:
            ax.plot(x_values[i], y_values[i], markers[i], label=tresholds[i], color = colorarray[i])


    plt.ylabel("Virality (Global Cascade fraction)")
    plt.xlabel("Pn (Network Polarization)")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="\u03B8 (threshold)")
    plt.grid(visible=True,linewidth=0.2)

    filepath = Path(path + 'test_sa_1_1_2step.pdf')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, bbox_inches='tight')

    # Salvare il grafico in un oggetto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='jpeg', bbox_inches='tight', dpi=80)
    buffer.seek(0)

    # Convertire il contenuto del buffer in una stringa base64
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return img_base64, filepath