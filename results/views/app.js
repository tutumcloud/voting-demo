var app = angular.module('catsvsdogs', []);
var socket = io.connect({transports:['polling']});

var bg1 = document.getElementById('background-stats-1');
var bg2 = document.getElementById('background-stats-2');

app.controller('statsCtrl', function($scope, $http){

  $scope.optionA = "";
  $scope.optionB = "";

  $scope.show = false;

  var animateStats = function(a,b){
    if(a+b>0){
      var percentA = a/(a+b)*100;
      var percentB = 100-percentA;
      bg1.style.width= percentA+"%";
      bg2.style.width = percentB+"%";
    }
  };

  $scope.catPercent = 50;
  $scope.dogPercent = 50;

  var updateScores = function(){
    socket.on('scores', function (data) {
       data = JSON.parse(data);

       optionA=Object.keys(data)[0];
       optionB=Object.keys(data)[1];

       animateStats(data[optionA], data[optionB]);
       $scope.$apply(function() {
         if(data[optionA] + data[optionB] > 0){
           $scope.catPercent = data[optionA]/(data[optionA]+data[optionB]) * 100;
           $scope.dogPercent = data[optionB]/(data[optionA]+data[optionB]) * 100;
           $scope.total = data[optionA] + data[optionB];
           $scope.optionA = optionA;
           $scope.optionB = optionB;
           $scope.show = true;
         }
      });
    });
  };

  var init = function(){
    document.body.style.opacity=1;
    updateScores();
  };

  socket.on('message',function(data){
    init();
  });
});
