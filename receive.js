var WebSocket = require('ws');

var HOST = '127.0.0.1';
var PORT = '8080';

var ws = new WebSocket('ws://' + HOST + ':' + PORT + '/');

ws.on('open', function(){   
	console.log("Connection Opened!");
    });

ws.on('message', function(data){
	var buf = JSON.parse(data);
	if(buf.data.length !== 0){
	    for(var i = 0; i < buf.data.length; i++){
		console.log("******************");
		console.log("dateTime: " + buf.data[i][0]);
		console.log("ID: " + buf.data[i][1]);
		console.log("temp: " + buf.data[i][2]);
		console.log("lks: " + buf.data[i][3]);
		console.log("but: " + buf.data[i][4]);
		console.log("ax: " + buf.data[i][5]);
		console.log("ay: " + buf.data[i][6]);
		console.log("az: " + buf.data[i][7]);
		console.log("******************");
	    }
	    
	}
    });

ws.on('close', function(){
	       console.log("Connection closed!");
	   });
  
