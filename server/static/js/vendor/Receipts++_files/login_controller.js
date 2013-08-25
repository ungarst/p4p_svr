function LogInCtrl ($scope, $location, $http, $location) {

  $scope.params = {"email_address": "dave@ungarst.com", "password": "dave"};

  $scope.login = function() {
    $http.post('/login', $scope.params).success(function(data, status, headers, config) {
      $location.path('/home');
    });
  }

  console.log("In the login controller");

}