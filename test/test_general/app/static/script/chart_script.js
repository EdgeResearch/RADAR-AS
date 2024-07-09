let config = null;
async function prepare_chart_data(data, xLabel, yLabel, dataLabel) {
    const txt_for_test = '{"thresholds": [0.15, 0.174, 0.198, 0.222, 0.246, 0.27, 0.294, 0.318, 0.342, 0.366, 0.39, 0.414], "datasets": [[0.78, 0.83, 0.9, 0.87, 0.93, 0.94, 0.9, 0.92, 0.83, 0.79, 0.71, 0.69, 0.63], [0.81, 0.86, 0.85, 0.88, 0.92, 0.94, 0.9, 0.8, 0.87, 0.77, 0.69, 0.66, 0.56], [0.77, 0.82, 0.82, 0.88, 0.94, 0.93, 0.91, 0.91, 0.89, 0.85, 0.76, 0.7, 0.57], [0.77, 0.86, 0.88, 0.86, 0.89, 0.93, 0.87, 0.91, 0.86, 0.83, 0.73, 0.75, 0.59], [0.81, 0.82, 0.81, 0.9, 0.84, 0.95, 0.94, 0.94, 0.93, 0.86, 0.83, 0.73, 0.61], [0.74, 0.81, 0.82, 0.87, 0.91, 0.97, 0.91, 0.93, 0.89, 0.77, 0.8, 0.78, 0.64], [0.68, 0.79, 0.81, 0.8, 0.86, 0.84, 0.87, 0.89, 0.89, 0.82, 0.87, 0.78, 0.64], [0.45, 0.55, 0.56, 0.64, 0.62, 0.76, 0.66, 0.8, 0.86, 0.86, 0.86, 0.79, 0.59], [0.33, 0.28, 0.33, 0.46, 0.44, 0.55, 0.7, 0.71, 0.7, 0.68, 0.73, 0.55, 0.36], [0.13, 0.14, 0.21, 0.25, 0.28, 0.34, 0.36, 0.57, 0.59, 0.53, 0.48, 0.34, 0.22], [0.05, 0.07, 0.04, 0.09, 0.12, 0.09, 0.23, 0.2, 0.22, 0.21, 0.15, 0.14, 0.06], [0.01, 0.02, 0.02, 0.04, 0.04, 0.06, 0.06, 0.14, 0.07, 0.09, 0.05, 0.05, 0.05]], "network_polarization": [0.0, 0.083, 0.166, 0.25, 0.333, 0.416, 0.5, 0.583, 0.666, 0.75, 0.833, 0.916, 1.0]}';
    console.log("In prepare leggo: ")
    console.log(data)
    const data_for_chart = JSON.parse(data.replace(/&#34;/g,'"'));
    const xValues = data_for_chart["network_polarization"];
    const virality_datasets = data_for_chart["datasets"];
    const yValues = [];
    // Ciclo che itera la lista per indice
    for (let i = 0; i < virality_datasets.length; i++) {
        //Genera i colori per la nuova linea del grafico
        let red = getRandomInt(120, 220);
        let green = getRandomInt(120, 220);
        let blue = getRandomInt(120, 220);

        //Crea la linea
        let newDataset = {
            label: dataLabel + ': ' + data_for_chart["thresholds"][i],
            data: virality_datasets[i],
            borderColor: `rgba(${red},${green},${blue},1)`,
            borderWidth: 4,
            fill: false,
            lineTension: 0,

        }
        yValues.push(newDataset)
    }

    config = {
        type: "line",
        data: {
            labels: xValues,
            datasets: yValues
        },
        options: {
            title: {
                display: true,
                text: 'Test_General Results',
                fontSize: 20,
                fontStyle: 'bold'
            },
            legend: {
                display: true,
                position: 'right',
                labels: {
                    fontSize: 14, // Imposta la dimensione del font per le etichette della legenda
                    fontStyle: 'bold' // Imposta lo stile del font per le etichette della legenda
                }
            },
            scales: {
                yAxes: [
                    {
                        ticks: {
                            min: 0,
                            max: 1,
                            fontSize: 14,
                            fontStyle: 'bold'
                        },
                        scaleLabel: {
                            display: true,
                            labelString: yLabel,
                            fontSize: 16,
                            fontStyle: 'bold'
                        }
                    }
                ],
                xAxes: [
                {
                    scaleLabel: {
                        display: true,
                        labelString: xLabel,
                        fontSize: 16,
                        fontStyle: 'bold'
                    }
                }
            ]},
        }
    }
}


function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}