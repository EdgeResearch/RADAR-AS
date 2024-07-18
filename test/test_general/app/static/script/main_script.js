async function start_test_1() {

    if(!validateTest1()){
        return;
    }

    document.getElementById("loader-bar").style.display = "block";

    let ticks = document.getElementById("ticks").value;
    let iterations = document.getElementById("iterations").value;
    let opinion_polarization = document.getElementById("opinion_polarization").value;
    let network_polarization = document.getElementById("network_polarization").value;
    let thresholds = document.getElementById("thresholds").value;

    let input = {
        ticks: ticks,
        iterations: iterations,
        opinion_polarization: opinion_polarization,
        network_polarization: network_polarization,
        thresholds: thresholds
    }

    let jsonResponse = await eel.submit_test_1(JSON.stringify(input))();

    let response = JSON.parse(jsonResponse)


    sessionStorage.setItem("data", response["data_for_chart"]);
    sessionStorage.setItem("xLabel", "Pn (Network Polarization)");
    sessionStorage.setItem("yLabel", "Virality (Global Cascade fraction)");
    sessionStorage.setItem("dataLabel", "Threshold");
    sessionStorage.setItem("chart", response["img_chart"])
    sessionStorage.setItem("log", response["log_output"])
    window.location.href = 'result-page.html';
}

async function start_test_2(){

    if(!validateTest2()){
        return;
    }

    document.getElementById("loader-bar").style.display = "block";
    let ticks = document.getElementById("ticks").value;
    let iterations = document.getElementById("iterations").value;
    let opinion_polarization = document.getElementById("opinion_polarization").value;
    let network_polarization = document.getElementById("network_polarization").value;
    let thresholds = document.getElementById("thresholds").value;
    let nodes = document.getElementById("nodes").value;

    let input = {
        ticks: ticks,
        iterations: iterations,
        opinion_polarization: opinion_polarization,
        network_polarization: network_polarization,
        thresholds: thresholds,
        nodes : nodes
    }

    console.log(JSON.stringify(input));
    let jsonResponse = await eel.submit_test_2(JSON.stringify(input))();

    let response = JSON.parse(jsonResponse)


    sessionStorage.setItem("data", response["data_for_chart"]);
    sessionStorage.setItem("xLabel", "Pn (Network Polarization)");
    sessionStorage.setItem("yLabel", "Virality (Global Cascade fraction)");
    sessionStorage.setItem("dataLabel", "Nodes");
    sessionStorage.setItem("chart", response["img_chart"])
    sessionStorage.setItem("log", response["log_output"])
    window.location.href = 'result-page.html';
}

function goHome() {
    window.location.href = "homepage.html"
}

async function startSimpleTest() {
    let jsonResponse = await eel.startTest()();
    let response = JSON.parse(jsonResponse);
    console.log(response);
}