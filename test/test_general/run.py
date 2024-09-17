import time

from bottle import Bottle, run, request, static_file, template, response
import sys
import os
import json
from test.test_general import utils, test_general_2, test_general_1
from test.test_general.test_general_parameters import TestGeneralParametes
from test_general_sa_1.test_general_parameters_sa import SuperAgentTestGeneralParametes
from test_general_sa_1 import test_general_sa_1
from test.test_general.utils import Tee, LogManager

app = Bottle()


@app.route('/test', method='POST')
def prova():
    data_for_chart = '{"thresholds": [0.15, 0.174, 0.198], "datasets": [[0.7, 0.9], [0.9, 0.8], [0.9, 1.0]], "network_polarization": [0.2, 0.4]}'
    return template("result-page.html", data=data_for_chart)


@app.post('/submit_test_1')
def submit_test_1():
    response.content_type = 'text/event-stream'
    response.cache_control = 'no-cache'

    def start_test_1():
        testParameters = TestGeneralParametes()
        # Crea un'istanza di Tee per gestire i log su terminale e file simultaneamente
        path = testParameters.path + "test_general_1/"
        testParameters.set_path(path)
        tee = Tee(testParameters.path + os.path.sep + 'log.txt')
        # Redirect sys.stdout to the tee object
        sys.stdout = tee
        path = testParameters.path + os.path.sep + "test_general_1"
        inputParameters = request.json
        try:
            ticks = int(inputParameters['ticks'])
            iterations = int(inputParameters['iterations'])
            opinion_polarization = float(inputParameters['opinion_polarization'])
            network_polarization = inputParameters['network_polarization']
            thresholds = inputParameters['thresholds']

            network_polarization = [float(value) for value in network_polarization.split(",")]
            thresholds = [float(value) for value in thresholds.split(",")]

            log_messages = [
                {"status": "in_progress", "value": f"Number of Ticks: {ticks}"},
                {"status": "in_progress", "value": f"Number of Iterazioni: {iterations}"},
                {"status": "in_progress", "value": f"Opinion Polarization: {opinion_polarization}"},
                {"status": "in_progress", "value": f"Network Polarization: {network_polarization}"},
                {"status": "in_progress", "value": f"Thresholds: {thresholds}"}
            ]

            for msg in log_messages:
                print(msg["value"])
                yield json.dumps(msg) + "\n"
                time.sleep(1)

            testParameters.set_total_ticks(ticks)
            testParameters.set_number_of_iterations(iterations)
            testParameters.set_opinion_polarization(opinion_polarization)
            testParameters.set_network_polarization(network_polarization)
            testParameters.set_thresholds(thresholds)

            parameters = {
                "ticks": ticks,
                "iterations": iterations,
                "opinion_polarization": opinion_polarization,
                "network_polarization": network_polarization,
                "thresholds": thresholds
            }

            log_message = {"status": "in_progress", "value": ">> Loading the NetLogo model..."}
            print(log_message["value"])
            yield json.dumps(log_message) + "\n"
            netlogo, netlogoCommands = test_general_1.load_sim_model()

            log_messages = [
                {"status": "in_progress", "value": ">> Model Loaded"},
                {"status": "in_progress", "value": ">> Starting the test..."},
            ]

            for msg in log_messages:
                print(msg["value"])
                yield json.dumps(msg) + "\n"
                time.sleep(1)

            dataframe, img_chart = test_general_1.start_test_1(netlogo, netlogoCommands, testParameters)

            log_message = {"status": "in_progress", "value": ">> Test completed"}
            print(log_message["value"])
            yield json.dumps(log_message) + "\n"

            data_for_chart = utils.setup_data_for_chart(dataframe, "Thresholds")

            time.sleep(1)

            log_message = {"status": "in_progress", "value": ">> Shutting down the system..."}
            print(log_message["value"])
            yield json.dumps(log_message) + "\n"

            netlogo.kill_workspace()

            # Get the captured output from the string buffer
            output = tee.get_value()
        finally:
            # Reimposta sys.stdout al valore originale (terminale)
            sys.stdout = tee.stdout
            tee.close()

        response_data = {
            "data_for_chart": data_for_chart,
            "img_chart": img_chart,
            "log_output": output
        }

        final_log_message = {"status": "done", "value": response_data}
        print(response_data)
        yield json.dumps(final_log_message) + "\n"
        
    return start_test_1()


@app.post('/submit_test_2')
def submit_test_2():
    response.content_type = 'text/event-stream'
    response.cache_control = 'no-cache'

    def start_test_2():
        testParameters = TestGeneralParametes()
        path = testParameters.path + "test_general_2/"
        testParameters.set_path(path)
        # Crea un'istanza di Tee per gestire i log su terminale e file simultaneamente
        tee = Tee(testParameters.path + os.path.sep + 'log.txt')
        # Redirect sys.stdout to the tee object
        sys.stdout = tee
        inputParameters = request.json
        try:
            ticks = int(inputParameters['ticks'])
            iterations = int(inputParameters['iterations'])
            opinion_polarization = float(inputParameters['opinion_polarization'])
            network_polarization = inputParameters['network_polarization']
            threshold = inputParameters['thresholds']
            nb_nodes = inputParameters['nodes']

            network_polarization = [float(value) for value in network_polarization.split(",")]
            nb_nodes = [int(value) for value in nb_nodes.split(",")]

            log_messages = [
                {"status": "in_progress", "value": f"Number of Tick: {ticks}"},
                {"status": "in_progress", "value": f"Number of Iterazioni: {iterations}"},
                {"status": "in_progress", "value": f"Opinion Polarization: {opinion_polarization}"},
                {"status": "in_progress", "value": f"Network Polarization: {network_polarization}"},
                {"status": "in_progress", "value": f"Treshold: {threshold}"},
                {"status": "in_progress", "value": f"Total Nodes: {nb_nodes}"}
            ]

            for msg in log_messages:
                print(msg["value"])
                yield json.dumps(msg) + "\n"
                time.sleep(1)

            testParameters.set_total_ticks(ticks)
            testParameters.set_number_of_iterations(iterations)
            testParameters.set_opinion_polarization(opinion_polarization)
            testParameters.set_network_polarization(network_polarization)
            testParameters.set_thresholds(threshold)
            testParameters.set_nb_nodes(nb_nodes)

            log_message = {"status": "in_progress", "value": ">> Loading the NetLogo model..."}
            print(log_message["value"])
            yield json.dumps(log_message) + "\n"
            netlogo, netlogoCommands = test_general_2.load_sim_model()

            log_messages = [
                {"status": "in_progress", "value": ">> Model Loaded"},
                {"status": "in_progress", "value": ">> Starting the test..."},
            ]

            for msg in log_messages:
                print(msg["value"])
                yield json.dumps(msg) + "\n"
                time.sleep(1)

            dataframe, img_chart = test_general_2.start_test_2(netlogo, netlogoCommands, testParameters)

            log_message = {"status": "in_progress", "value": ">> Test completed"}
            print(log_message["value"])
            yield json.dumps(log_message) + "\n"

            data_for_chart = utils.setup_data_for_chart(dataframe, "Nodes")

            time.sleep(1)
            log_message = {"status": "in_progress", "value": ">> Shutting down the system..."}
            print(log_message["value"])
            yield json.dumps(log_message) + "\n"

            netlogo.kill_workspace()

            # Get the captured output from the string buffer
            output = tee.get_value()
        finally:
            # Reimposta sys.stdout al valore originale (terminale)
            sys.stdout = tee.stdout
            tee.close()

        response_data = {
            "data_for_chart": data_for_chart,
            "img_chart": img_chart,
            "log_output": output
        }

        final_log_message = {"status": "done", "value": response_data}
        yield json.dumps(final_log_message) + "\n"

    return start_test_2()


@app.post('/submit_test_sa_1')
def submit_test_sa_1():
    response.content_type = 'text/event-stream'
    response.cache_control = 'no-cache'

    def start_test_sa_1():
        testParameters = SuperAgentTestGeneralParametes()
        # Crea un'istanza di Tee per gestire i log su terminale e file simultaneamente
        path = testParameters.path
        testParameters.set_path(path)

        log_manager = LogManager(path + 'log.txt')

        inputParameters = request.json
        ticks = int(inputParameters['ticks'])
        iterations = int(inputParameters['iterations'])
        opinion_polarization = float(inputParameters['opinion_polarization'])
        network_polarization = inputParameters['network_polarization']
        thresholds = inputParameters['thresholds']

        network_polarization = [float(value) for value in network_polarization.split(",")]
        thresholds = [float(value) for value in thresholds.split(",")]

        warning = inputParameters['warning']
        node_range_static_b = float(inputParameters['node_range_static_b'])
        node_range = float(inputParameters['node_range'])
        choose_method = inputParameters['choose_method']
        warning_impact = float(inputParameters['warning_impact'])
        warning_impact_neutral = float(inputParameters['warning_impact_neutral'])
        sa_delay = int(inputParameters['sa_delay'])

        log_messages = [
            {"status": "in_progress", "value": f"Numero di Ticks: {ticks}"},
            {"status": "in_progress", "value": f"Numero di Iterazioni: {iterations}"},
            {"status": "in_progress", "value": f"Opinion Polarization: {opinion_polarization}"},
            {"status": "in_progress", "value": f"Network Polarization: {network_polarization}"},
            {"status": "in_progress", "value": f"Thresholds Polarization: {thresholds}"},
            {"status": "in_progress", "value": f"warning: {warning}"},
            {"status": "in_progress", "value": f"node_range_static_b: {node_range_static_b}"},
            {"status": "in_progress", "value": f"node_range: {node_range}"},
            {"status": "in_progress", "value": f"choose_method: {choose_method}"},
            {"status": "in_progress", "value": f"warning_impact: {warning_impact}"},
            {"status": "in_progress", "value": f"warning_impact_neutral: {warning_impact_neutral}"},
            {"status": "in_progress", "value": f"sa_delay: {sa_delay}"},

        ]
        for msg in log_messages:
            print(msg["value"])
            log_manager.insert_line(msg["value"])
            yield json.dumps(msg) + "\n"
            time.sleep(0.5)

        testParameters.set_total_ticks(ticks)
        testParameters.set_number_of_iterations(iterations)
        testParameters.set_opinion_polarization(opinion_polarization)
        testParameters.set_network_polarization(network_polarization)
        testParameters.set_thresholds(thresholds)
        testParameters.set_warning(warning)
        testParameters.set_node_range_static_b(node_range_static_b)
        testParameters.set_node_range(node_range)
        testParameters.set_choose_method(choose_method)
        testParameters.set_warning_impact(warning_impact)
        testParameters.set_warning_impact_neutral(warning_impact_neutral)
        testParameters.set_sa_delay(sa_delay)

        log_message = {"status": "in_progress", "value": ">> Carico il modello di netlogo..."}
        print(log_message["value"])
        log_manager.insert_line(log_message["value"])
        yield json.dumps(log_message) + "\n"

        netlogo, netlogoCommands = test_general_sa_1.load_sim_model()

        log_messages = [
            {"status": "in_progress", "value": ">> Modello caricato"},
            {"status": "in_progress", "value": ">> Avvio il test..."},
        ]

        for msg in log_messages:
            print(msg["value"])
            log_manager.insert_line(msg["value"])
            yield json.dumps(msg) + "\n"
            time.sleep(1)

        dataframe, img_chart = test_general_sa_1.start_test_sa_1(netlogo, netlogoCommands, testParameters)

        log_message = {"status": "in_progress", "value": ">> Test terminato"}
        print(log_message["value"])
        log_manager.insert_line(log_message["value"])
        yield json.dumps(log_message) + "\n"

        data_for_chart = utils.setup_data_for_chart(dataframe, "Thresholds")

        time.sleep(1)
        log_message = {"status": "in_progress", "value": ">> Spengo il sistema..."}
        print(log_message["value"])
        log_manager.insert_line(log_message["value"])
        yield json.dumps(log_message) + "\n"

        netlogo.kill_workspace()

        output = log_manager.get_contents()
        log_manager.clear_log()

        response_data = {
            "data_for_chart": data_for_chart,
            "img_chart": img_chart,
            "log_output": output
        }

        final_log_message = {"status": "done", "value": response_data}
        yield json.dumps(final_log_message) + "\n"


    return start_test_sa_1()


@app.route('/home')
def goHome():
    return template("./app/templates/homepage.html")


@app.route('/results')
def renderResults():
    return template("./app/templates/result-page.html")


@app.route('/test1_page')
def renderTest1Page():
    return template("./app/templates/test-page-1.html")


@app.route('/test2_page')
def renderTest2Page():
    return template("./app/templates/test-page-2.html")


@app.route("/")
@app.route("/index")
def index():
    return template("./app/templates/homepage.html")


# Rotta per servire file statici (CSS, JS, immagini)
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./app/static')


if __name__ == "__main__":
    run(app, host='localhost', port=8081, debug=True)
