from flask import Flask, jsonify, request, render_template
from test_general_parameters import TestGeneralParametes
import test_general
import utils
import tmpTest

app = Flask(__name__, template_folder="./templates")

# Variabili globali
#netlogo = None
#netlogoCommands = None

@app.route('/test', methods=['POST'])
def prova():
   data_for_chart = '{"thresholds": [0.15, 0.174, 0.198], "datasets": [[0.7, 0.9], [0.9, 0.8], [0.9, 1.0]], "network_polarization": [0.2, 0.4]}'
   print("Sono qua!")
   return render_template("result-page.html", data=data_for_chart)

@app.route('/submit', methods=['POST'])
def submit():
    # global netlogo, netlogoCommands

    testParameters = TestGeneralParametes()
    ticks = int(request.form['ticks'])
    iterations = int(request.form['iterations'])
    opinion_polarization = int(request.form['opinion_polarization'])
    network_polarization = request.form['network_polarization']
    thresholds = request.form['thresholds']

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

    """
    if netlogo is None and netlogoCommands is None:
        print("Chiamo la funzione per caricare")
        
    else:
        print("Le variabili hanno già il modello")
    """
    netlogo, netlogoCommands = test_general.load_sim_model()
    dataframe = test_general.start_test(netlogo, netlogoCommands, testParameters)

    data_for_chart = utils.setup_data_for_chart(dataframe)
    print(f"Mando: {data_for_chart}")
    print("Spengo il sistema...")
    netlogo.kill_workspace()
    return render_template("result-page.html", data=data_for_chart)


@app.route('/home')
def goHome():
    return render_template("test-page-1.html")
@app.route("/")
@app.route("/index")
def index():
    return render_template("test-page-1.html")

if __name__ == "__main__":
    app.run(debug=True)