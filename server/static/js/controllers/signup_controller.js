function SignUpCtrl ($scope, $location, $http) {

  $scope.params = {
    "first_name": "",
    "last_name": "",
    "email_address": "",
    "password": "",
    "confirm": ""
  };

  $scope.signup = function() {
    if($scope.params.confirm == $scope.params.password && $scope.params.password != ""){
      $http.post('/signup', $scope.params).success(function(data, status, headers, config) {
        $location.path('/home');
      });
    } else {
      alert("Passwords do not match.");
      $scope.params.password = "";
      $scope.params.confirm = "";
    }
  }

  console.log("In the sign up controller");
}