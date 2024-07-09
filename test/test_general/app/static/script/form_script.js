
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
        });
    };
    document.head.appendChild(jqueryScript);
});