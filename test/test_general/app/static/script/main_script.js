async function start_test_1() {
    document.getElementById("loader-bar").style.display = "block";

    let ticks = document.getElementById("ticks").value;
    let iterations = document.getElementById("iterations").value;
    let opinion_polarization = document.getElementById("opinion_polarization").value;
    let network_polarization = document.getElementById("network_polarization").value;
    let thresholds = document.getElementById("thresholds").value;

    let input = {
        ticks : ticks,
        iterations : iterations,
        opinion_polarization : opinion_polarization,
        network_polarization : network_polarization,
        thresholds : thresholds
    }

    let jsonResponse = await eel.submit(JSON.stringify(input))();

    sessionStorage.setItem("data", jsonResponse);
    sessionStorage.setItem("xLabel", "Pn (Network Polarization)");
    sessionStorage.setItem("yLabel", "Virality (Global Cascade fraction)");
    sessionStorage.setItem("dataLabel", "Threshold");
    window.location.href = 'result-page.html';
}

function goHome(){
    window.location.href = "homepage.html"
}
async function  startSimpleTest(){
    let jsonResponse = await eel.startTest()();
    let response = JSON.parse(jsonResponse);
    console.log(response);
}