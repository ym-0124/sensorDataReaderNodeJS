var http = require('http');
var WebSocketServer = require('websocket').server;
var WebSocketClient = require('websocket').client;
var fs = require('fs');

//clientのnew
var client = new WebSocketClient();

//connect
client.connect('ws://localhost:8080/', 'echo-protocol');

// connection failed
client.on('connectFailed', function(error){
	console.log("connection error: " + error.toString());
    });
//connected
client.on('connect', function(connect){
	console.log("WebSocekt client Connected!!");
	connect.on('error', function(error){// connect error
		console.log("Connection Error " + error.toString());
	    });
	connect.on('close', function(){// closed
		console.log("WebSocket Connection Closed");
	    });

	connect.on('message', function(data){// receive a message
		console.log("Received: " + data);
	    });
    });
