var express = require('express'),
    redis = require("redis"),
    cookieParser = require('cookie-parser'),
    bodyParser = require('body-parser'),
    methodOverride = require('method-override'),
    app = express();

var port = process.env.PORT || 4000;
var password = process.env.REDIS_ENV_REDIS_PASS;
var options = {
  "host": "redis",
  "port":"6379",
  "auth_pass": password
};

var client = redis.createClient(options);

client.on("error", function (err) {
    console.log("Error " + err);
});

client.subscribe("pubsub");
client.on("message", function(){
  console.log("Update");
});

app.use(cookieParser());
app.use(bodyParser());
app.use(methodOverride('X-HTTP-Method-Override'));
app.use(express.static(__dirname + '/views'));

app.get('/', function (req, res) {
  res.sendFile(path.resolve(__dirname + '/views/index.html'));
});

var server = app.listen(port, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Example app listening at http://%s:%s', host, port);
});
