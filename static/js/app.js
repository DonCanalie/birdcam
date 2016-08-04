var myapp = angular.module('birdcam', []);
var urlServer = 'http://localhost:8080/'
myapp.controller('ngBirdCam', function($scope, $http, $compile)
{
    $scope.title = 'BirdCam'
    $scope.led_Click = function(light){led_Click($scope, $http, light)}
    $scope.webcam_Click = function(cam){webcam_Click($scope, $http, cam)}

    $scope.load_sensor = function(){load_sensor($scope, $http, 1);}
    load_sensor($scope, $http, 0);
    load_cams($scope, $http);
    load_leds($scope, $http);
})

function load_sensor($scope, $http, db)
{
    console.log('Lade Daten ...')
    $http(
    {
         url     : urlServer + 'sensor'
        ,method  : "GET"
        ,params  : {"refresh": db}
    }
    ).then
    (
        function successCallback(response)
        {
            console.log('Daten angekommen!')
            statuscode = response.status;
            if(statuscode == '200')
            {
                $scope.txtTemperature = response.data["temp"]
                $scope.txtHumidity = response.data["hum"]
                $scope.txtRecordedAT = response.data["rec"]
                console.log('txtTemperature' + $scope.txtTemperature)
                console.log('txtHumidity' + $scope.txtHumidity)
                console.log('txtRecordedAT' + $scope.txtRecordedAT)
            }
        },
        function errorCallback(response)
        {
            console.log('Klappt nicht')
        }
    );
}


function load_cams($scope, $http)
{
    console.log('Lade Cams ...')
    $http(
    {
         url     : urlServer + 'cams'
        ,method  : "GET"
        ,params  : {}
    }
    ).then
    (
        function successCallback(response)
        {
            console.log('Cams geladen!')
            statuscode = response.status;
            if(statuscode == '200')
            {
                $scope.act_webcam = response.data["act_cam"]

                console.log('act_webcam' + $scope.act_webcam)
            }
        },
        function errorCallback(response)
        {
            console.log('Klappt nicht')
        }
    );
}


function load_leds($scope, $http)
{
    console.log('Lade LEDs ...')
    $http(
    {
         url     : urlServer + 'leds'
        ,method  : "GET"
        ,params  : {}
    }
    ).then
    (
        function successCallback(response)
        {
            console.log('LEDs geladen!')
            statuscode = response.status;
            if(statuscode == '200')
            {
                $scope.led1 = response.data["inner"]
                $scope.led2 = response.data["outer"]

                console.log('led1' + $scope.led1)
                console.log('led2' + $scope.led2)
            }
        },
        function errorCallback(response)
        {
            console.log('Klappt nicht')
        }
    );
}


function led_Click($scope, $http, light)
{
    $http(
    {
         url     : urlServer + 'leds'
        ,method  : "POST"
        ,data    : {
                          'light' : light
                   }
    }
    ).then
    (
        function successCallback(response)
        {
            console.log('Klappt')
            load_leds($scope, $http);

        },
        function errorCallback(response)
        {
            console.log('Klappt nicht')
        }
    );
}

function webcam_Click($scope, $http, cam)
{
    $http(
    {
         url     : urlServer + 'cams'
        ,method  : "POST"
        ,data    : {
                          'cam' : cam
                   }
    }
    ).then
    (
        function successCallback(response)
        {
            console.log('Klappt')
            load_cams($scope, $http);

        },
        function errorCallback(response)
        {
            console.log('Klappt nicht')
        }
    );
}

