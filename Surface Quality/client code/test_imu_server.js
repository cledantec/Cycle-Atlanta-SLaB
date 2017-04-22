// This is how we connect to the creator. IP and port.
// The IP is the IP I'm using and you need to edit it.
// By default, MALOS has its 0MQ ports open to the world.

// Every device is identified by a base port. Then the mapping works
// as follows:
// BasePort     => Configuration port. Used to config the device.
// BasePort + 1 => Keepalive port. Send pings to this port.
// BasePort + 2 => Error port. Receive errros from device.
// BasePort + 3 => Data port. Receive data from device.

var creator_ip = '127.0.0.1'
var creator_imu_base_port = 20013

var protoBuf = require("protobufjs");
var request = require("request");
// var fs = require("fs");
// var querystring = require('querystring');
var http = require('http');

// Parse proto file
var protoBuilder = protoBuf.loadProtoFile('../../protocol-buffers/malos/driver.proto')
// Parse matrix_malos package (namespace).
var matrixMalosBuilder = protoBuilder.build("matrix_malos")

var zmq = require('zmq')

function PostCode(codestring) {
  
  // An object of options to indicate where to post to
  var post_options = {
      host: '0.0.0.0',
      port: '5000',
      path: '/inertial',
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(codestring)
      }
  };

  // Set up the request
  var post_req = http.request(post_options, function(res) {
      res.setEncoding('utf8');
      res.on('data', function (chunk) {
          // console.log('Response: ' + chunk);
      });
  });

  // post the data
  post_req.write(codestring);
  post_req.end(codestring);

}

// ********** Start error management.
var errorSocket = zmq.socket('sub')
errorSocket.connect('tcp://' + creator_ip + ':' + (creator_imu_base_port + 2))
errorSocket.subscribe('')
errorSocket.on('message', function(error_message) {
  process.stdout.write('Message received: IMU error: ' + error_message.toString('utf8') + "\n")
});
// ********** End error management.


// ********** Start configuration.
var configSocket = zmq.socket('push')
configSocket.connect('tcp://' + creator_ip + ':' + creator_imu_base_port)
// Now prepare valid configuration and send it.
var driverConfigProto = new matrixMalosBuilder.DriverConfig
// 0.05 seconds between updates.
driverConfigProto.delay_between_updates = 0.05
// Stop sending updates 10 seconds after pings.
driverConfigProto.timeout_after_last_ping = 10.0
configSocket.send(driverConfigProto.encode().toBuffer())
// ********** End configuration.

// ********** Start updates - Here is where they are received.
var updateSocket = zmq.socket('sub')
updateSocket.connect('tcp://' + creator_ip + ':' + (creator_imu_base_port + 3))
updateSocket.subscribe('')
updateSocket.on('message', function(imu_buffer) {
  var imuData = new matrixMalosBuilder.Imu.decode(imu_buffer)
  PostCode(JSON.stringify(imuData));
});
// ********** End updates

// ********** Ping the driver
var pingSocket = zmq.socket('push')
pingSocket.connect('tcp://' + creator_ip + ':' + (creator_imu_base_port + 1))
process.stdout.write("Sending pings every .5 seconds");
pingSocket.send(''); // Ping the first time.
setInterval(function(){
  pingSocket.send('');
}, 50);
// ********** Ping the driver ends



