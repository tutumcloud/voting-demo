var app = angular.module('catsvsdogs', []);
var socket = io.connect("http://192.168.99.100:5002");

var bg1 = document.getElementById('background-stats-1');
var bg2 = document.getElementById('background-stats-2');

app.controller('statsCtrl', function($scope){
  var randomColor = function(){
    var r = (Math.round(Math.random()* 127) + 127).toString(16);
    var g = (Math.round(Math.random()* 127) + 127).toString(16);
    var b = (Math.round(Math.random()* 127) + 127).toString(16);
    return '#' + r + g + b;
  };
  var animateStats = function(a,b){
    var percentA = a/(a+b)*100;
    var percentB = 100-percentA;
    bg1.style.width= percentA+"%";
    bg2.style.width = percentB+"%";
  };

  var updateScores = function(){
    socket.on('scores', function (data) {
       data = JSON.parse(data);
       animateStats(data.cats, data.dogs);
    });
  };

  var init = function(){
    document.body.style.opacity=1;
    updateScores();
    $scope.$apply(function(){
      $scope.color = [];
      $scope.color[0] = randomColor();
      $scope.color[1] = randomColor();
    });
  };
  socket.on('message',function(data){
    init();
  });
});
