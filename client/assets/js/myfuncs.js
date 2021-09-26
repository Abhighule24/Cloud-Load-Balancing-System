var valHldr ="";
resholder ="";

function getPing(ele){
    ms = Date.now();
    rms = 0; 
    $.ajax(
        {
                
            url: "http://"+ele.children[1].innerText+":"+ele.children[2].innerText, 
            data: "func=ping&params="+"hellohowarekhanakhakejanaha",
            success: function(result){
                            resholder= result.split("'").join('"');
                            console.log(result)
                            if (result=='{ "status": "success","output": "hellohowarekhanakhakejanaha"}') rms =  Date.now() - ms;
                            else rms=99999;
                            //$("#well1").html(resholder);
                            ele.children[5].innerText=rms+" ms";
                        },
            error: function(result){
                            //$("#well1").html("Something wrong, please try later");
                            rms="error";
                            ele.children[5].innerText=rms;
                        }
        });
    
}

function getScrCard(){
    if(valHldr != "" && $("#t1").val() != ""){
        $.ajax(
            {
					
				url: "http://"+$("#agntSrv").val()+":"+$("#t1").val(), 
                data: "func=Card&params="+valHldr,
                success: function(result){
								resholder= result.split("'").join('"');
                                //$("#well1").html(resholder);
								$("#well1").html(makeTableJ(JSON.parse(resholder)));
                                valHldr = '{"values":['+vald.values+']}';
                            },
                error: function(result){
                                $("#well1").html("Something wrong, please try later");
                            }
            });
    }
    else{
        if(valHldr == "") raiseAlert("Please select the desired functions");
		if($("#t1").val() == "") raiseAlert("Please set a PORT number");
    }
}
function setfuncVals(){
    
    vald = {"values":['"ping"']};
    cnt=0;
    $.each($(".funcs"),function(i,v){
        if(v.checked==true ) {
                vald.values.push(v.value);
                cnt++
        }
    });
    if(cnt>0){
        valHldr = '{"values":['+vald.values+']}';
        $("#t2").val('{"values":['+vald.values+']}');
    }
    else{
        valHldr = "";
        $("#t2").val("");
    }
}
$(".funcs").on("change",
               function (){
                    setfuncVals();
                });

function makeTableJ(dgd){
    var srvn=0;
	var tbl= '<table class="table-responsive table-striped">';
	tbl+="<thead><tr><th>Server</th><th>Address</th><th>Port</th><th>Allocation</th><th>Functions</th><th>Ping</th></tr></thead>";
	tbl+="<tbody>";
	$.each(dgd.Report_card , function(key, value) {
        console.log(value);
	  tbl+='<tr id="srv'+srvn+'" onclick="setLocX(\''+value.ip+'\','+value.port+');">';
	  tbl+="<td>"+key+"</td>";
		$.each(value, function(keyz, valuez) {
		  tbl+="<td>"+valuez+"</td>";
        });
      tbl+='<th> Pinging... </th>';
      srvn++;
	  tbl+='</tr>';
	});
    tbl +="</tbody></table>";
    tbl +="<script>";
    tbl +="for (sr=0;sr<"+srvn+";sr++)";
    tbl +="getPing(document.getElementById('srv'+sr));";
    tbl +="</script>";
	return tbl;
}



function setLocX(ip,port){
    document.location.href="functions.html"+"?ip="+ip+"&port="+port;
    //document.location.pathname="/functions.html";
}
var funcresults;

function getServOutput(funcname,ip,port,params){
    $.ajax(
        {
			url: "http://"+ip+":"+port, 
            data: "func="+funcname+'&params={"values":['+params+"]}",
            success: function(result){
                $("#outdiv").html(result);
                //funcresults = result;
                funcresults = JSON.parse(result);
                funcresults = JSON.parse(funcresults.output.replaceAll("'",'"'));
                },
            error: function(result){
                $("#outdiv").html("Something wrong, please try later");
                funcresults={};
                }
        });
}