// Declares the modules that our app is going to use
var rppApp = angular.module('rppApp', ['ngCookies', 'ngResource', 'ui.utils']);

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
        templateUrl: 'static/partials/home.html',
        controller: 'HomeCtrl'
      })
      .otherwise(
      {
        redirectTo: "/"
      });
});
