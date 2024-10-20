async function start_test_1() {

    if (!validateTest1()) {
        return;
    }

    disableButton();
    document.getElementById("loader-bar").style.display = "block";
    document.getElementById("log-box").style.display = "block";
    document.getElementById("info-box").style.display = "block";

    let ticks = document.getElementById("ticks").value;
    let iterations = document.getElementById("iterations").value;
    let opinion_polarization = document.getElementById("opinion_polarization").value;
    let network_polarization = document.getElementById("network_polarization").value;
    let thresholds = document.getElementById("thresholds").value;
    let email = document.getElementById("email").value;

    // Configura i dettagli della richiesta
    let input = {
        ticks: ticks,
        iterations: iterations,
        opinion_polarization: opinion_polarization,
        network_polarization: network_polarization,
        thresholds: thresholds,
        email: email
    }
    console.log(JSON.stringify(input));

    let result_response = ""
    console.log("CHIAMO");

    const logElement = document.getElementById("log-box");
    logElement.innerHTML = "";  // Clear previous logs

    const response = await fetch('/submit_test_1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(input) // Converti i dati in formato JSON
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
        const {value, done} = await reader.read();
        if (done) {
            break;
        }
        const text = decoder.decode(value, {stream: true})

        console.log("Testo corrente:")
        console.log(text)
        let log_message = JSON.parse(text);

        if (log_message.status === "in_progress") {
            let text_to_print = log_message.value.replace(/\n/g, "<br>");
            logElement.innerHTML += text_to_print + "<br>";
            logElement.scrollTop = logElement.scrollHeight; // Scrolla automaticamente alla fine
        } else if (log_message.status === "done") {
            result_response = log_message.value
        }
    }

    console.log("Fine funzione");

    console.log(result_response)

    sessionStorage.setItem("data", result_response["data_for_chart"]);
    sessionStorage.setItem("xLabel", "Pn (Network Polarization)");
    sessionStorage.setItem("yLabel", "Virality (Global Cascade fraction)");
    sessionStorage.setItem("dataLabel", "Threshold");
    sessionStorage.setItem("chart", result_response["img_chart"])
    sessionStorage.setItem("log", result_response["log_output"])
    enableButton();
    console.log("MANDO QUESTA RISPOSTA")
    console.log(response)
    location.href = '/results';
}

async function start_test_2() {

    if (!validateTest2()) {
        return;
    }
    disableButton();
    document.getElementById("loader-bar").style.display = "block";
    document.getElementById("log-box").style.display = "block";
    document.getElementById("info-box").style.display = "block";

    let ticks = document.getElementById("ticks").value;
    let iterations = document.getElementById("iterations").value;
    let opinion_polarization = document.getElementById("opinion_polarization").value;
    let network_polarization = document.getElementById("network_polarization").value;
    let thresholds = document.getElementById("thresholds").value;
    let nodes = document.getElementById("nodes").value;
    let email = document.getElementById("email").value;

    let input = {
        ticks: ticks,
        iterations: iterations,
        opinion_polarization: opinion_polarization,
        network_polarization: network_polarization,
        thresholds: thresholds,
        nodes: nodes,
        email: email
    }

    console.log(JSON.stringify(input));
    let result_response = ""
    console.log("CHIAMO");

    const logElement = document.getElementById("log-box");
    logElement.innerHTML = "";  // Clear previous logs

    const response = await fetch('/submit_test_2', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(input) // Converti i dati in formato JSON
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
        const {value, done} = await reader.read();
        if (done) {
            break;
        }
        const text = decoder.decode(value, {stream: true})
        let log_message = JSON.parse(text);

        if (log_message.status === "in_progress") {
            let text_to_print = log_message.value.replace(/\n/g, "<br>");
            logElement.innerHTML += text_to_print + "<br>";
            logElement.scrollTop = logElement.scrollHeight; // Scrolla automaticamente alla fine
        } else if (log_message.status === "done") {
            result_response = log_message.value
        }
    }

    console.log("Fine funzione");

    console.log(result_response)


    sessionStorage.setItem("data", result_response["data_for_chart"]);
    sessionStorage.setItem("xLabel", "Pn (Network Polarization)");
    sessionStorage.setItem("yLabel", "Virality (Global Cascade fraction)");
    sessionStorage.setItem("dataLabel", "Nodes");
    sessionStorage.setItem("chart", result_response["img_chart"])
    sessionStorage.setItem("log", result_response["log_output"])
    enableButton();
    location.href = '/results';
}


async function start_test_sa_1() {
    if (!validateTest1()) {
        return;
    }
    disableButton();
    document.getElementById("loader-bar").style.display = "block";
    document.getElementById("log-box").style.display = "block";


    let ticks = document.getElementById("ticks").value;
    let iterations = document.getElementById("iterations").value;
    let opinion_polarization = document.getElementById("opinion_polarization").value;
    let network_polarization = document.getElementById("network_polarization").value;
    let thresholds = document.getElementById("thresholds").value;
    let warning = document.getElementById("warning").checked;
    let node_range_static_b = document.getElementById("node-range-static-b").value;
    let node_range = document.getElementById("node-range").value;
    let choose_method = document.getElementById("choose-method").value;
    let warning_impact = document.getElementById("warning-impact").value;
    let warning_impact_neutral = document.getElementById("warning-impact-neutral").value;
    let sa_delay = document.getElementById("sa-delay").value;
    let email = document.getElementById("email").value;

    let input = {
        ticks: ticks,
        iterations: iterations,
        opinion_polarization: opinion_polarization,
        network_polarization: network_polarization,
        thresholds: thresholds,
        warning : warning,
        node_range_static_b : node_range_static_b,
        node_range : node_range,
        choose_method : choose_method,
        warning_impact : warning_impact,
        warning_impact_neutral : warning_impact_neutral,
        sa_delay : sa_delay,
        email: email
    }

    console.log(JSON.stringify(input));

    let result_response = ""
    console.log("CHIAMO");

    const logElement = document.getElementById("log-box");
    logElement.innerHTML = "";  // Clear previous logs

    const response = await fetch('/submit_test_sa_1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(input) // Converti i dati in formato JSON
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
        const {value, done} = await reader.read();
        if (done) {
            break;
        }
        const text = decoder.decode(value, {stream: true})
        console.log(text)
        let log_message = JSON.parse(text);

        if (log_message.status === "in_progress") {
            let text_to_print = log_message.value.replace(/\n/g, "<br>");
            logElement.innerHTML += text_to_print + "<br>";
            logElement.scrollTop = logElement.scrollHeight; // Scrolla automaticamente alla fine
        } else if (log_message.status === "done") {
            result_response = log_message.value
        }
    }

    console.log("Fine funzione");

    console.log(result_response)

    sessionStorage.setItem("data", result_response["data_for_chart"]);
    sessionStorage.setItem("xLabel", "Pn (Network Polarization)");
    sessionStorage.setItem("yLabel", "Virality (Global Cascade fraction)");
    sessionStorage.setItem("dataLabel", "Nodes");
    sessionStorage.setItem("chart", result_response["img_chart"])
    sessionStorage.setItem("log", result_response["log_output"])
    enableButton();
    location.href = '/results';
}

function goHome() {
    window.location.href = "home"
}