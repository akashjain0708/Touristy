/* Sample Controller */
var mc = angular.module('mc', ['ngRoute']);
var info="";
var PostUpdateID = "";

mc.controller('lc', ['$scope', '$http', '$location', function($scope, $http, $location){
    var input = document.getElementById('searchTextField');
    var options = {
        types: ['establishment']
    };
    autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.addListener('place_changed', getPlaceData);

    function getPlaceData(){
        var location = autocomplete.getPlace().geometry.location;
        var latitude = location.lat();
        var longitude = location.lng();
        var name = autocomplete.getPlace().name;
        var data = JSON.stringify({
            LocationName : name,
            Latitude : latitude,
            Longitude : longitude,
        });

        console.log(data);

        $http.post('/search', data, {headers:{'Content-Type':'application/json'}})
            .success(function (data, status, headers, config) {
                info = data;
                $location.path('/main');
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    };
}]);

mc.controller('loginc', ['$scope', '$http', function($scope, $http){
    $scope.SendLoginData = function(){
        var data = {
            UserName : $scope.user.username,
            Password : $scope.user.password
        };

        $http.post('/ServerRequest/login', data)
            .success(function (data, status, headers, config) {
                $scope.login = data;
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    };
}]);

mc.controller('signupc', ['$scope', '$http', function($scope, $http){
    $scope.SendSignUpData = function(){
        var data = {
            UserName : $scope.user.username,
            EmailID : $scope.user.email,
            FullName : $scope.user.fullname,
            Password : $scope.user.password,
            PhoneNumber : $scope.user.number
        };

        $http.post('/ServerRequest/signup', data)
            .success(function (data, status, headers, config) {
                $scope.signup = data;
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    }
}]);

mc.controller('mainc', ['$scope', '$http', '$routeParams', '$location', function($scope, $http, $routeParams, $location){
    var Post_ID = "";
    $scope.locations = info;
    console.log($scope.locations)

    /*$http.get('./data/touristy.json').success(function(data){
     $scope.locations = data;
     });*/

    $scope.SendUpdateID = function(x){
        PostUpdateID = x;
        console.log("PostUpdatedID:" +PostUpdateID);
    };

    var input = document.getElementById('searchTextField');
    var options = {
        types: ['establishment']
    };
    autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.addListener('place_changed', getPlaceData);

    var location = "";
    var latitude = "";
    var longitude = "";
    var name = "";

    function getPlaceData(){
        location = autocomplete.getPlace().geometry.location;
        latitude = location.lat();
        longitude = location.lng();
        name = autocomplete.getPlace().name;

        var data = {
            LocationName : name,
            Latitude : latitude,
            Longitude : longitude,
        }

        console.log(data);

        $http.post('/search', data)
            .success(function (data, status, headers, config) {
                $scope.locations = data;
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    }

    $scope.SendDeleteData = function(x){
        Post_ID = x;

        var data = {
            PostID : Post_ID
        };
        console.log("Deleting")
        console.log(data)
        $http.post('/deletePost', data)
            .success(function (data, status, headers, config) {
                $location.path('/list');

            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    };

    $scope.SendFilterData = function(){
        var data = {
            LocationName : name,
            Latitude : latitude,
            Longitude : longitude,
            Time : $scope.attraction.tym,
            Price : $scope.attraction.price,
            Distance : $scope.attraction.distance,
            Rating : $scope.attraction.rating
        };

        console.log(data);

        $http.post('/search/filters', data)
            .success(function (data, status, headers, config) {
                $scope.locations = data;
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    };
}]);

mc.controller('detailc', ['$scope', '$http', function($scope, $http){
    var input = document.getElementById('searchTextField');
    var options = {
        types: ['establishment']
    };
    autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.addListener('place_changed', getPlaceData);

    var location = "";
    var latitude = "";
    var longitude = "";
    var name = "";

    function getPlaceData(){
        location = autocomplete.getPlace().geometry.location;
        latitude = location.lat();
        longitude = location.lng();
        name = autocomplete.getPlace().name;
    }

    $scope.SendDetailData = function(){
        var data = {
            LocationName : name,
            Latitude : latitude,
            Longitude : longitude,
            Description : $scope.attraction.describe,
            Price : $scope.attraction.price,
            Time : $scope.attraction.tym,
            Rating : $scope.attraction.rating
        };

        console.log(data);

        $http.post('/createPost', data)
            .success(function (data, status, headers, config) {
                // $scope.detail = data;
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    };
}]);

mc.controller('updatec', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams){
    $scope.SendUpdateData = function(){
        console.log(PostUpdateID);
        var data = {
            PostID : PostUpdateID,
            Description : $scope.attraction.describe,
            Price : $scope.attraction.price,
            Time : $scope.attraction.tym,
            Rating : $scope.attraction.rating
        };

        $http.post('/editPost', data)
            .success(function (data, status, headers, config) {
                // $scope.update = data;
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    };
}]);