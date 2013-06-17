function SignUpCtrl ($scope, $location, $http) {

  $scope.params = {
    "first_name": "",
    "last_name": "",
    "email_address": "",
    "password": ""
  };

  $scope.signup = function() {
    $http.post('/signup', $scope.params).success(function(data, status, headers, config) {
      $location.path('/home');
    });
  }

  console.log("In the sign up controller");
}