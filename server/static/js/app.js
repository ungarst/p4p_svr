// Declares the modules that our app is going to use
var rppApp = angular.module('rppApp', ['ngCookies', 'ngResource', 'ui.utils', 'ui.bootstrap']);

// Need to use different symbols as flask uses {{ and }}
rppApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('<[');
    $interpolateProvider.endSymbol(']>');
});

// Routes for our application
rppApp.config(function($routeProvider) {
  $routeProvider
      .when('/',
      {
        templateUrl: 'static/partials/root.html',
        controller: 'RootCtrl'
      })
      .when ('/receipt/:receiptId',
      {
        templateUrl: 'static/partials/receipt.html',
        controller: 'ReceiptCtrl'
      })
      .when('/home',
      {
        templateUrl: 'static/partials/home.html',
        controller: 'HomeCtrl'
      })
      .when ('/signup',
      {
        templateUrl: 'static/partials/signup.html',
        controller: 'SignUpCtrl'
      })
      .when('/login',
      {
        templateUrl: 'static/partials/login.html',
        controller: 'LogInCtrl'
      })
      .when('/add_receipt',
      {
        templateUrl: 'static/partials/add_receipt.html',
        controller: 'AddReceiptCtrl'
      })
      .otherwise(
      {
        redirectTo: "/"
      });
});
