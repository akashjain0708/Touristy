var app = angular.module('mp3',['ngRoute', 'mc']);

app.config(function ($routeProvider) {
	$routeProvider.when('/home', {
		templateUrl: '/static/partials/home.html',
		controller: 'hc'
	}).when('/list', {
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
	}).when('/mypost', {
		templateUrl: '/static/partials/mypost.html',
		controller: 'mpc'
	}).when('/hm', {
		templateUrl: '/static/partials/hm.html',
		controller: 'hmc'
	}).when('/details', {
		templateUrl: '/static/partials/details.html',
		controller: 'detailc'
	}).when('/update/:itemID', {
		templateUrl: '/static/partials/update.html',
		controller: 'updatec'
	}).otherwise({redirectTo: '/home'});
});
