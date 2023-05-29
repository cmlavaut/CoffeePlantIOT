var intervalID = setInterval(peticionMqtt,2000);
var script = document.querySelector('script[src="../static/js/index.js"]');


function peticionMqtt()
{
  var dataMqtt = $.get('/dataMqtt/');
  var tm = dataMqtt.done(
    function(result){
        result = JSON.parse(result);
        $('.tiempoRegado').text(result[3]);
        $('.humMinima').text(result[2]);
        $('.hum').text(result[4]);
        $('.hum_suelo').text(result[1]);
        $('.temp').text(result[5]);
        $('.id').text(result[0]);
        $('.aguastatus').text(result[6]);
        console.log("dato cargados: "+ result[0]+ ","+result[1]+ ","+result[2]+ ","+result[3]+ ","+result[4]+ ","+result[5] + ","+ result[6]);
    }
  )
}

function graficar(){
    parametro = document.getElementById("parametro");
    fecha = document.getElementById("fecha");
    document.cookie = "parametro=" + parametro.value;
    document.cookie = "fecha=" + fecha.value;
    console.log(document.cookie);
    setTimeout(() => $.get('/datos'), 1000);
    imagen = document.getElementById("grafica");
    Fecha = "Fecha" + fecha.value.replace(/\s+/g, '');
    pathImagen = "../static/graficos/Sensor"+parametro.value.replace(/\s+/g, '') + Fecha + ".png";
    setTimeout(() => imagen.src=pathImagen, 4000);
}

function back(){
    window.location.href = '/';
}

function enviarDatos(){
    timeselect = document.getElementById("tiempo");
    humselect = document.getElementById("hum");
    var dato = humselect.value + "," + timeselect.value  
    console.log(dato)
    $.get("/enviarData/" + dato);
    alert("Datos enviados ");
}