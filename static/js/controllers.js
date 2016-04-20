/* Sample Controller */
var mc = angular.module('mc', ['ngRoute']);

var info = "";
var userName = "";
var lat;
var long;
var heatdata;
var tempLat;
var tempLong;
var recommended = "";

mc.controller('hc', ['$scope', '$http', '$location', function($scope, $http, $location){

}]);

mc.controller('hmc', ['$scope', '$http', '$location', function($scope, $http, $location){
    $scope.userName = localStorage.getItem("UID");
    if($scope.userName != null) {
        $scope.if_loggedIn = true;
    }
    var map, heatmap;
    //var tempLat = 37.774546;
    //var tempLong = -122.433523;
    //function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: {lat: tempLat, lng: tempLong},
        mapTypeId: google.maps.MapTypeId.SATELLITE
    });

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatdata,
        map: map
    });

    heatmap.setMap(map);

    //}
}]);

mc.controller('loginc', ['$scope', '$http', '$location', function($scope, $http, $location){
    $scope.SendLoginData = function(){
        var data = {
            UserName : $scope.user.username,
            Password : $scope.user.password
        };
        localStorage.setItem("UID", $scope.user.username);

        $http.post('/loginUser', data)
            .success(function (data, status, headers, config) {
                if(data[0] == "OK") {
                    console.log("User logged in!" +data);
                    userName = data[2];
                    $location.path('/list');
                }
                else{
                    /*
                     TODO: ERROR!
                     */
                }
            })
            .error(function (data, status, header, config) {
            });
    };
}]);

mc.controller('signupc', ['$scope', '$http', '$location', function($scope, $http, $location){
    $scope.SendSignUpData = function(){
        var data = {
            UserName : $scope.user.username,
            EmailID : $scope.user.email,
            FullName : $scope.user.fullname,
            Password : $scope.user.password,
            PhoneNumber : $scope.user.number
        };
        localStorage.setItem("UID", $scope.user.username);
        $http.post('/signup', data)
            .success(function (data, status, headers, config) {
                console.log(data);
                //$scope.signup = data;
                userName = data[2];
                $location.path('/list');
            })
            .error(function (data, status, header, config) {
            });
    }
}]);

mc.controller('mpc', ['$scope', '$http', '$location', function($scope, $http, $location){
    //userName = "Priya";    //Have to remove this
    $scope.userName = localStorage.getItem("UID");
    //$scope.userName = userName;

    var data = {
        "UserID": $scope.userName
    }

    $http.post('/myPosts', data)
        .success(function(data) {
            $scope.locations = data;
        });

    var Post_ID = "";

    $scope.SendDeleteData = function(x){
        Post_ID = x;

        var data = {
            PostID : Post_ID
        };

        $http.post('/deletePost', data)
            .success(function (data, status, headers, config) {
                location.reload();
            });
    };

    $scope.SendUpdateID = function(x){
        PostUpdateID = x;
    };

    $scope.SignOut = function(){
        localStorage.removeItem("UID");
    };

}]);

mc.controller('lc', ['$scope', '$http', '$location', function($scope, $http, $location){
    var input = document.getElementById('searchTextField');
    var options = {
    };
    autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.addListener('place_changed', getPlaceData);

    //userName = "Priya" ;//Have to remove this
    //$scope.userName = userName;
    $scope.userName = localStorage.getItem("UID");
    if($scope.userName != null) {
        $scope.if_loggedIn = true;
    }

    function getPlaceData(){
        var location = autocomplete.getPlace().geometry.location;
        var latitude = location.lat();
        var longitude = location.lng();
        lat = latitude;
        long = longitude;
        var name = autocomplete.getPlace().name;
        var tags = autocomplete.getPlace().types;
        var data = {
            LocationName : name,
            Latitude : latitude,
            Longitude : longitude,
            Tags: tags
        };

        $http.post('/search', data)
            .success(function (data, status, headers, config) {
                console.log("Got search data! Hey" + JSON.stringify(data));
                info = data[0];
                recommended = data[1];
                $location.path('/main');
            })
    }

    $scope.SignOut = function(){
        localStorage.removeItem("UID");
    };

}]);

mc.controller('mainc', ['$scope', '$http', '$routeParams', '$location', function($scope, $http, $routeParams, $location){
    var Post_ID = "";
    $scope.locations = info;
    $scope.recommended_posts = recommended;

    var input = document.getElementById('searchTextField');
    var options = {

    };
    autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.addListener('place_changed', getPlaceData);

    //userName = "Priya"   //Have to remove this
    //$scope.userName = userName;
    $scope.userName = localStorage.getItem("UID");
    if($scope.userName != null) {
        $scope.if_loggedIn = true;
    }
    var location = "";
    var latitude = "";
    var longitude = "";
    var name = "";
    var tags;

    function getPlaceData(){
        location = autocomplete.getPlace().geometry.location;
        latitude = location.lat();
        longitude = location.lng();
        name = autocomplete.getPlace().name;
        tags = autocomplete.getPlace().types;
        lat = latitude;
        long = longitude;

        var data = {
            LocationName : name,
            Latitude : latitude,
            Longitude : longitude,
            Tags: tags
        };

        $http.post('/search', data)
            .success(function (data, status, headers, config) {
                console.log("Did a post!" + JSON.stringify(data));
                $scope.locations = data[0];
                console.log(JSON.stringify(data[1]));
                $scope.recommended_posts = data[1];
                console.log(JSON.stringify($scope.recommended_posts[0]["LocationName"]));
            })
            .error(function (data, status, header, config) {
            });
    }

    console.log("Lat/Lon: "+lat);

    $scope.sendHeatMapData= function(){
        var data = {
            Latitude : lat,
            Longitude : long
        };
        console.log("Lat/Lon: "+lat+","+long);
        $http.post('/heatMapData', data).success(function(data){
            console.log("Returned with: " +JSON.stringify(data));
            var heat_data = [];
            for (entry in data){
                console.log(JSON.stringify(data[entry]));
                var each_heat = {"location": new google.maps.LatLng(data[entry][0], data[entry][1]), weight: data[entry][2]};
                heat_data.push(each_heat);
            }
            //print("Heat data:" +JSON.stringify(heat_data));
            data = [{"location": new google.maps.LatLng(37.782, -122.447), weight: 0.5},
                {location: new google.maps.LatLng(37.782, -122.443), weight: 2},
                {location: new google.maps.LatLng(37.782, -122.441), weight: 3},
                {location: new google.maps.LatLng(37.782, -122.439), weight: 2},
                {location: new google.maps.LatLng(37.782, -122.435), weight: 0.5},

                {location: new google.maps.LatLng(37.785, -122.447), weight: 3},
                {location: new google.maps.LatLng(37.785, -122.445), weight: 2},
                {location: new google.maps.LatLng(37.785, -122.441), weight: 0.5},
                {location: new google.maps.LatLng(37.785, -122.437), weight: 2},
                {location: new google.maps.LatLng(37.785, -122.435), weight: 3}];
            heatdata = heat_data;
            tempLat = lat;
            tempLong = long;
            console.log("Temperature:" + tempLat, tempLong);
            $location.path('/hm');
        });
    };

    $scope.SendDeleteData = function(x){
        Post_ID = x;

        var data = {
            PostID : Post_ID
        };

        $http.post('/deletePost', data)
            .success(function (data, status, headers, config) {
                $scope.locations = data;
            })
            .error(function (data, status, header, config) {
                $scope.locations = [{
                    "UserName": "abc",
                    "LocationName": "The Chicago Bean",
                    "Latitude": "15",
                    "Longitude": "10",
                    "Description": "Awesome",
                    "Rating": "5",
                    "UpVotes": "142",
                    "DownVotes": "20",
                    "Price": "30",
                    "Time": "20",
                    "PostID": "tt0111161"
                }];
            });
    };

    $scope.SendFilterData = function(){
        var data = {
            LocationName : name,
            Latitude : lat,
            Longitude : long,
            Time : $scope.attraction.tym,
            Price : $scope.attraction.price,
            Distance : $scope.attraction.distance,
            Rating : $scope.attraction.rating,
            Tags: tags
        };
        console.log("Lat/Lon: "+lat+","+long);
        $http.post('/search/filters', data)
            .success(function (data, status, headers, config) {
                $scope.locations = data;
            })
            .error(function (data, status, header, config) {
            });
    };

    $scope.SendUpdateID = function(x){
        PostUpdateID = x;
        console.log(PostUpdateID);
    };

    $scope.SignOut = function(){
        localStorage.removeItem("UID");
    };

    var voted = new Array();

    $scope.votes = function(y,z){
        if(voted[z] == undefined && localStorage.getItem("UID")!= null)
        {
            voted[z] = 1;
            if(y ==1){
                $scope.locations[z].UpVotes += y;
                var data = {
                    PostID : $scope.locations[z].PostID,
                    UpVotes : $scope.locations[z].UpVotes,
                    DownVotes : $scope.locations[z].DownVotes
                };
            }
            else {
                $scope.locations[z].DownVotes -= y;
                var data = {
                    PostID : $scope.locations[z].PostID,
                    UpVotes : $scope.locations[z].UpVotes,
                    DownVotes : $scope.locations[z].DownVotes
                };
            }

            $http.post('/updateVote', $scope.locations[z])
                .success(function (data, status, headers, config) {
                    console.log("Done");
                });
        }

        console.log(data);
    };

}]);

mc.controller('detailc', ['$scope', '$http', '$location', function($scope, $http, $location){
    var input = document.getElementById('searchTextField');
    var options = {

    };
    autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.addListener('place_changed', getPlaceData);

    //userName = "Priya"   //Have to remove this
    //$scope.userName = userName;
    $scope.userName = localStorage.getItem("UID");

    var location = "";
    var latitude = "";
    var longitude = "";
    var name = "";

    function getPlaceData(){
        location = autocomplete.getPlace().geometry.location;
        latitude = location.lat();
        longitude = location.lng();
        name = autocomplete.getPlace().name;
        tags =  autocomplete.getPlace().types;
    }

    $scope.SendDetailData = function(){
        var data = {
            UserName: localStorage.getItem("UID"),
            LocationName : name,
            Latitude : latitude,
            Longitude : longitude,
            Description : $scope.attraction.describe,
            Price : $scope.attraction.price,
            Time : $scope.attraction.tym,
            Rating : $scope.attraction.rating,
            Tags : tags
        };

        $http.post('/createPost', data)
            .success(function (data, status, headers, config) {
                $location.path('/mypost');
                // $scope.detail = data;
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    };
    $scope.SignOut = function(){
        localStorage.removeItem("UID");
    };
}]);

mc.controller('updatec', ['$scope', '$http', '$routeParams', '$location', function($scope, $http, $routeParams, $location){
    //userName = "Priya";
    //$scope.userName = userName;
    $scope.userName = localStorage.getItem("UID");
    $scope.SendUpdateData = function(){
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
                console.log("Returns from update post");
                $location.path('/mypost');
            })
            .error(function (data, status, header, config) {
                console.log("Returns from update post in error");
                $location.path('/mypost');
                $scope.ResponseDetails = "Data: " + data +
                    "<hr />status: " + status +
                    "<hr />headers: " + header;
            });
    };

    $scope.SignOut = function() {
        localStorage.removeItem("UID");
    };
}]);