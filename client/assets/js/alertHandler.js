var alerter = '<div class="alert alert-danger alert-dismissible fade in">'
              +'<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>'
              +'<strong>Error!</strong><p>';   //this is where the message goes and ends with a </p></div>

function raiseAlert(msg){
    $("#popCont").html($("#popCont").html()+alerter+msg+"</p></div>")
}