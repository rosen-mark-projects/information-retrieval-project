'use strict';
var express = require("express");
var bodyParser = require('body-parser');
var http = require('http');

var node_hostname = "localhost";
var http_port = "8001";

var initHttpServer = () => {
	var app = express();
	app.use(express.json())
	app.use(express.urlencoded({ extended: true }))
	app.use(express.static(__dirname));
    app.get('/',function(req,res){
	     res.sendFile(__dirname + '/index.html');
	});

	app.listen(http_port, () => console.log('Listening http on port ' + http_port));
}

initHttpServer();
