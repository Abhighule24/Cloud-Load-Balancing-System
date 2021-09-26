ip ="";
port = "";
$(document).ready( function(){
    kl = new URLSearchParams(document.URL.split('?')[1]);
    document.getElementById("hpd1").innerHTML = '<b>Connected to: </b>'+kl.get('ip')+'</b><br><b>On Port: </b>'+kl.get('port');
    ip = kl.get('ip');
    port = kl.get('port');
});
