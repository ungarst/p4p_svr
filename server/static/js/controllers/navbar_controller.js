function NavBarCtrl ($scope, $location, $http) {
  
  $scope.logged_in = false;

  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    if ("user" in $scope.data) {
      $scope.logged_in = true;
    }
  });

  $scope.logOut = function() {
    $http.get('/logout').success(function(data, status, headers, config) {
      $scope.logged_in = false;
      $location.path('/');
    });
  }
  
}

