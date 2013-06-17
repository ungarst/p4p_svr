function LogInCtrl ($scope, $location, $http, $location) {

  $scope.params = {"email_address": "dave@ungarst.com", "password": "dave"};

  $scope.login = function() {
    $http.post('/login', {"cats":"dogs"}).success(function() {
      $location.path('/');
    });
  }



  console.log("In the login controller");

}