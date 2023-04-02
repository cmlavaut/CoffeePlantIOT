var slider = document.getElementById("sensor");
var output = document.getElementById("humedadMinima");
var intervalID = setInterval(peticionMqtt,2000);
var humedadSelecionada = document.getElementById("sensor");
var tiempoSelecionado = document.getElementById("tiempo");

output.innerHTML = slider.value;
  slider.oninput = function() {
  output.innerHTML = this.value;
}

function enviarDatos(){
  var mqttDatos = humedadSelecionada.value.toString() + "," + tiempoSelecionado.value.toString();
  console.log(mqttDatos);
  $.get("/enviarData/" + mqttDatos);
  alert("Datos enviados");
}


function peticionMqtt()
{
  var dataMqtt = $.get('/dataMqtt');
  var tm = dataMqtt.done(
    function(result){
      if (result[3])
      {
        document.getElementById("aguaID").src = "../static/images/agua.png";
        $('.textoAgua').text("Hay agua en el tanque");
      }
      else
      {
        document.getElementById("aguaID").src = "../static/images/no_agua.png";
        $('.textoAgua').text("No hay agua en el tanque");
      }
      $('.humedadMinima').text(result[4]);
      $('.tiempoRegado').text(result[5]);
      var plotearHum = JSON.parse(result[0]);
      var plotearTemp = JSON.parse(result[1]);;
      var plotearHumSuelo = JSON.parse(result[2]);;
        var plot_data = plotearHum;
        var plot = Plotly.newPlot('hum', plot_data.data, plot_data.layout);
        plot_data = plotearTemp;
        plot =  Plotly.newPlot('temp', plot_data.data, plot_data.layout);
        plot_data = plotearHumSuelo;
        plot =  Plotly.newPlot('hum_suelo', plot_data.data, plot_data.layout);
    }
  )
}
function historial(){
  window.location.href = "/historial";
}
/* var script = document.querySelector('script[src="../static/js/scripts.js"]');
var plotearHum = JSON.parse(script.getAttribute('humedad'));
var plotearTemp = JSON.parse(script.getAttribute('temp'));
var plotearHumSuelo = JSON.parse(script.getAttribute('humedad_suelo'));
        var plot_data = plotearHum;
        var plot = Plotly.newPlot('hum', plot_data.data, plot_data.layout);
        plot_data = plotearTemp;
        plot =  Plotly.newPlot('temp', plot_data.data, plot_data.layout);
        plot_data = plotearHumSuelo;
        plot =  Plotly.newPlot('hum_suelo', plot_data.data, plot_data.layout); */