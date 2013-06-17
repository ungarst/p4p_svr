function HomeCtrl ($scope, $location, $http) {
  
  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    if (!("user" in $scope.data)) {
      $location.path('/');
    }
    $scope.user = $scope.data["user"];
  });


}