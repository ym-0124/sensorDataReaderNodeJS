var fs = require('fs');
var WsClient = require('ws');
var WsServer = require('ws').Server;

var SENSOR_HOST = '192.168.1.3';
var SENSOR_PORT = '8000';
var NODE_HOST = '192.168.1.4';
var NODE_PORT = '8080';

var http = require('http').createServer(function(req, res){
    fs.readFile(__dirname + '/index.html', function(err, data){
	if(err){
	    res.writeHead(500);
	    console.log("Internal Server Error");
	} else {
	    try {
		res.writeHead(200);
		res.end(data);
	    } catch(e){
		console.log("Internal Server Error");
		res.end("Internal Server Error");
	    }
	}
    });
}).listen(NODE_PORT, function(){
    console.log((new Date()) + ": httpServer is Listening @" + NODE_HOST + " on port " + NODE_PORT + ". ");
});

var wsClient = new WsClient('ws://' + SENSOR_HOST + ':' + SENSOR_PORT + '/'); // node - sensorServer : new
var wsServer = new WsServer({host:NODE_HOST, port:NODE_PORT}); // client - node : new

wsServer.on('connection', function(ws){ // client - node : connect
    ws.on('message', function(message){
	// do something when client send some msg.
    });

    ws.on('close', function(){
	// do something when client - node is closed.
    });
});

wsClient.on('open',function(){ // node - sensorServer : open
    console.log("node is connected to sensorServer");
    wsClient.send('node is connected to sensorServer', {mask:true});
});

var counter = 0;
wsClient.on('message', function(data){ // node - sensorServer : message
    var buf = JSON.parse(data); 
    console.log("<><><><><><><><><><><><>:" + counter);
    counter++; // for Debug
    if(buf.data.length !== 0){
	for(var i = 0; i < buf.data.length; i++){
	    if(4031 == buf.data[i][1]){ // ID authentification
		/*
		console.log("******************");
		console.log("dateTime: " + buf.data[i][0]);
		console.log("ID: " + buf.data[i][1]);
		console.log("temp: " + buf.data[i][2]);
		console.log("lks: " + buf.data[i][3]);
		console.log("but: " + buf.data[i][4]);
		console.log("ax: " + buf.data[i][5]);
		console.log("ay: " + buf.data[i][6]);
		console.log("az: " + buf.data[i][7]);
		*/
		counter = 0;
	    }
	}	    
    }    
});

// node - sensorServer : close
wsClient.on('close', function(){
    console.log("Connection closed!");
});
  
