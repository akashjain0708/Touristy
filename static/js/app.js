var app = angular.module('mp3',['ngRoute', 'mc']);

app.config(function ($routeProvider) {
	$routeProvider.when('/', {
		templateUrl: '/static/partials/list.html',
		controller: 'lc'
	}).when('/login', {
		templateUrl: '/static/partials/login.html',
		controller: 'loginc'
	}).when('/signup', {
		templateUrl: '/static/partials/signup.html',
		controller: 'signupc'
	}).when('/main', {
		templateUrl: '/static/partials/main.html',
		controller: 'mainc'
	}).when('/details', {
		templateUrl: '/static/partials/details.html',
		controller: 'detailc'
	}).when('/update/:itemID', {
		templateUrl: '/static/partials/update.html',
		controller: 'updatec'
	}).otherwise({redirectTo: '/'});
});
