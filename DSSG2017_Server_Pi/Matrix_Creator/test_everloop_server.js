// This is how we connect to the creator. IP and port.
// The IP is the IP I'm using and you need to edit it.
// By default, MALOS has its 0MQ ports open to the world.

// Every device is identified by a base port. Then the mapping works
// as follows:
// BasePort     => Configuration port. Used to config the device.
// BasePort + 1 => Keepalive port. Send pings to this port.
// BasePort + 2 => Error port. Receive errros from device.
// BasePort + 3 => Data port. Receive data from device.

var creator_ip= '127.0.0.1'
var creator_everloop_base_port = 20013 + 8 // port for Everloop driver.

var request = require("request");
var fs = require("fs");
var querystring = require('querystring');
var http = require('http');
var protoBuf = require("protobufjs");
var protoBuilder = protoBuf.loadProtoFile('../../protocol-buffers/malos/driver.proto')
var matrixMalosBuilder = protoBuilder.build("matrix_malos")

var zmq = require('zmq')

function getLedStatus() {
	
}

// To trigger an error message you can send an invalid configuration to the driver.
// For instance, set a number of leds != 35.
var errorSocket = zmq.socket('sub')
errorSocket.connect('tcp://' + creator_ip + ':' + (creator_everloop_base_port + 2))
errorSocket.subscribe('')
errorSocket.on('message', function(error_message) {
  process.stdout.write('Message received: Pressure error: ' + error_message.toString('utf8') + "\n")
});

var configSocket = zmq.socket('push')
configSocket.connect('tcp://' + creator_ip + ':' + creator_everloop_base_port /* config */)

var max_intensity = 50;
var min_intensity = 1;
var intensity_value = min_intensity;
var dir = 0;

function getData(callback) {

}

function setStatusLoop() {
	var values = [];
	var config = new matrixMalosBuilder.DriverConfig
        config.image = new matrixMalosBuilder.EverloopImage	
	
	var URL = 'http://0.0.0.0:5000/getstatus';
	request(URL, (error,response,body) => {
		if (!error && response.statusCode === 200) {
			values = JSON.parse(body)
			
	//console.log(values)
	for (var j = 0; j < 36; j++) {
      	var ledValue = new matrixMalosBuilder.LedValue;
	if(values[j]=='Z') 
	{
		
		ledValue.setRed(0);
		ledValue.setGreen(0);
		ledValue.setBlue(0);
		ledValue.setWhite(0);
		config.image.led.push(ledValue)
	}
	else if(values[j]=='W') 
	{
		ledValue.setRed(intensity_value);
		ledValue.setGreen(intensity_value);
		ledValue.setBlue(intensity_value);
		ledValue.setWhite(intensity_value);
		config.image.led.push(ledValue)
	}
	else if(values[j]=='R') 
	{
		ledValue.setRed(max_intensity);
		ledValue.setGreen(0);
		ledValue.setBlue(0);
		ledValue.setWhite(0);
		config.image.led.push(ledValue)
	}
	else if(values[j]=='G') 
	{
		ledValue.setRed(0);
		ledValue.setGreen(max_intensity);
		ledValue.setBlue(0);
		ledValue.setWhite(0);
		config.image.led.push(ledValue)
	}
	else if(values[j]=='B') 
	{
		ledValue.setRed(0);
		ledValue.setGreen(0);
		ledValue.setBlue(max_intensity);
		ledValue.setWhite(0);
		config.image.led.push(ledValue)
	}
		
    }
    configSocket.send(config.encode().toBuffer());
     //console.log(values);
    } else {
			console.log(error);
		}
	}); 
}

setStatusLoop(intensity_value);

setInterval(function() {
	if(dir==0) intensity_value += 1;
	if(dir==1) intensity_value -= 1;
  	if (intensity_value <= min_intensity) {
    		intensity_value = min_intensity;
  		dir = 0;
  	}
	if (intensity_value >= max_intensity) {
		intensity_value = max_intensity;
  		dir = 1;
	}
	setStatusLoop();
	}, 1000);
process.on('SIGINT', function(){
	console.log("Caught interrupt signal..");
	
	process.exit();
});
