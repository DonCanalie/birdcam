var myapp = angular.module('birdcam', []);
var urlServer = 'http://93.129.36.184'
myapp.controller('ngBirdCam', function($scope, $http, $compile)
{
    $scope.title = 'BirdCam'
    $scope.act_webcam = 1
    $scope.led1 = true
    $scope.led1_text = 'ON'
    $scope.led2 = true
    $scope.led2_text = 'ON'
    $scope.Led1_Click = function(){Led1_Click($scope, $http)}
    $scope.Led2_Click = function(){Led2_Click($scope)}
    $scope.Webcam1_Click = function(){Webcam1_Click($scope)}
    $scope.Webcam2_Click = function(){Webcam2_Click($scope)}
})

function Led1_Click($scope, $http)
{
    $scope.led1 = !$scope.led1
    $scope.led1_text = ($scope.led1 == true) ? 'ON' : 'OFF'

    $http(
    {
         url     : urlServer
        ,method  : "POST"
        ,data    : {
                          btn : 'btnLed0Off'
                   }
    }
    ).then
    (
        function successCallback(response)
        {
            console.log('Klappt')

        },
        function errorCallback(response)
        {
            console.log('Klappt nicht')
        }
    );
}

function Led2_Click($scope)
{
    $scope.led2 = !$scope.led2
    $scope.led2_text = ($scope.led2 == true) ? 'ON' : 'OFF'
}

function Webcam1_Click($scope)
{
    $scope.act_webcam = 1
}

function Webcam2_Click($scope)
{
    $scope.act_webcam = 2
}