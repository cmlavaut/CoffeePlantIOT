var variable = document.getElementById("variable");
var fecha = document.getElementById("fecha");
var titulo = ""


function regresar(){
    window.location.href = "/";
  }

  function graficar(){
    grafico = variable.value.toString()+","+fecha.value.toString()
    $.get("/graficar/" + grafico);
    let textoVariable = variable.value.toString().replace(/\s+/g,"")
    let textofecha = fecha.value.toString().replace(/\s+/g,"")
    titulo = "Sensor"+textoVariable+"Fecha"+textofecha;
    setTimeout(
      ' document.getElementById("grafica").src = "../static/graficos/"+ titulo +".png";',
      1000);
     
  }