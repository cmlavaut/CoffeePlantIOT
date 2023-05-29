function posicion(){
    lugar = document.getElementById('opciones');
    console.log(lugar);
    document.cookie = "lugar=" + lugar.value;
    setTimeout(() => window.location.href = "/graficas", 1000);
}

function ver(){
    var numeracion = document.getElementById('opciones');
    console.log(numeracion);
    document.cookie = "numeracion=" + numeracion.value;
    window.location.href = '/visualizar/';
 }
