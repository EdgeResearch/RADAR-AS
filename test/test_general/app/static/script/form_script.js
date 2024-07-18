const ticks_regex = /^[1-9]\d*$/;
const decimal_regex = /^(?!$)(?:0*(?:\.\d+)?|1(\.0*)?)$/;
const decimal_list_regex = /^(0(\.\d+)?|1)(,(0(\.\d+)?|1))*$/;
const integer_list_regex = /^\d+(,\d+)*$/;


console.log("Caricato Il file!")
document.addEventListener("DOMContentLoaded", function () {
    const jqueryScript = document.createElement('script');
    jqueryScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.js';
    jqueryScript.onload = function () {
        $(document).ready(function () {
            $("#iterations-info-icon").click(function(){
                $("#iterations-info").slideToggle();
            });
            $("#ticks-info-icon").click(function(){
                $("#ticks-info").slideToggle();
            });
            $("#opinion-polarization-info-icon").click(function(){
                $("#opinion-polarization-info").slideToggle();
            });
            $("#network-polarization-info-icon").click(function(){
                $("#network-polarization-info").slideToggle();
            });
            $("#thresholds-info-icon").click(function (){
                $("#thresholds-info").slideToggle();
            })
            $("#nodes-info-icon").click(function (){
                $("#nodes-info").slideToggle();
            })
        });
    };
    document.head.appendChild(jqueryScript);
});

function validateTicks(){
    let ticks = document.getElementById("ticks").value;
    if (ticks_regex.test(ticks)) {
        $("#ticks").css("border-color", "#003049");
        $("#ticks-info").slideUp();
        return true;
    }
    else {
        $("#ticks").css("border-color", "#C1111F");
        $("#ticks-info").slideDown();
        return false;
    }
}

function validateIterations(){
    let iterations = document.getElementById("iterations").value;
    if (ticks_regex.test(iterations)) {
        $("#iterations").css("border-color", "#003049");
        $("#iterations-info").slideUp();
        return true;
    }
    else {
        $("#iterations").css("border-color", "#C1111F");
        $("#iterations-info").slideDown();
        return false;
    }
}

function validateOpionionPol(){
    let opinion_polarization = document.getElementById("opinion_polarization").value;
    if (decimal_regex.test(opinion_polarization)) {
        $("#opinion_polarization").css("border-color", "#003049");
        $("#opinion-polarization-info").slideUp();
        return true;
    }
    else {
        $("#opinion_polarization").css("border-color", "#C1111F");
        $("#opinion_polarization-info").slideDown();
        return false;
    }
}

function validateNetworkPol(){
    if(document.getElementById("network_polarization") === undefined){
        return true
    }
    let network_polarization = document.getElementById("network_polarization").value;
    if (decimal_list_regex.test(network_polarization)) {
        $("#network_polarization").css("border-color", "#003049");
        $("#network-polarization-info").slideUp();
        return true;
    }
    else {
        $("#network_polarization").css("border-color", "#C1111F");
        $("#network-polarization-info").slideDown();
        return false;
    }
}

function validateThresholds(){
        if(document.getElementById("thresholds") === undefined){
        return true
    }
    let thresholds = document.getElementById("thresholds").value;
    if (decimal_list_regex.test(thresholds)) {
        $("#thresholds").css("border-color", "#003049");
        $("#thresholds-info").slideUp();
        return true;
    }
    else {
        $("#thresholds").css("border-color", "#C1111F");
        $("#thresholds-info").slideDown();
        return false;
    }
}

function validateThreshold(){
        if(document.getElementById("thresholds") === undefined){
        return true
    }
    let thresholds = document.getElementById("thresholds").value;
    if (decimal_regex.test(thresholds)) {
        $("#thresholds").css("border-color", "#003049");
        $("#thresholds-info").slideUp();
        return true;
    }
    else {
        $("#thresholds").css("border-color", "#C1111F");
        $("#thresholds-info").slideDown();
        return false;
    }
}

function validateNodes(){
        if(document.getElementById("nodes") === undefined){
        return true
    }
    let nodes = document.getElementById("nodes").value;
    if (integer_list_regex.test(nodes)) {
        $("#nodes").css("border-color", "#003049");
        $("#nodes-info").slideUp();
        return true;
    }
    else {
        $("#nodes").css("border-color", "#C1111F");
        $("#nodes-info").slideDown();
        return false;
    }
}

function validateTest1(){
    return (validateTicks() & validateIterations() & validateOpionionPol() &
        validateNetworkPol() & validateThresholds())
}

function validateTest2(){
    return (validateTicks() & validateIterations() & validateOpionionPol() &
        validateNetworkPol() & validateThreshold() & validateNodes())
}