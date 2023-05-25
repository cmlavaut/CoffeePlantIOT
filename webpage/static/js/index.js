var intervalID = setInterval(peticionMqtt,2000);

function peticionMqtt()
{
  var dataMqtt = $.get('/dataMqtt/');
  var tm = dataMqtt.done(
    function(result){
        result = JSON.parse(result);
        $('.humMinima').text(result[1]);
        $('.tiempoRegado').text(result[0]);
        console.log("dato cargados: "+ result[1]+ ","+result[0]);
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

function posicion(){
    lugar = document.getElementById('opciones');
    console.log(lugar);
    document.cookie = "lugar=" + lugar.value;
    setTimeout(() => window.location.href = "/graficas", 1000);
}

function ver(){
    window.location.href = '/visualizar/3';
}

function back(){
    window.location.href = '/';
}

function enviarDatos(){
    timeselect = document.getElementById("tiempo");
    humselect = document.getElementById("hum");
    //document.cookie = "tiemposelect=" + timeselect.value;
    var dato = timeselect.value + "," + humselect.value
    console.log(dato)
    $.get("/enviarData/"+ dato);
    alert("Datos enviados " + dato);
}