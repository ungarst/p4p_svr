// This will just be the basic screen where users come when
// they aren't logged in.
function RootCtrl ($scope, $location, $http) {

  // if logged in then redirect them to the home page

  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    if ("user" in $scope.data) {
      $location.path('/home');
    }
  });

}
