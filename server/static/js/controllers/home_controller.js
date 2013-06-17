// This will just be the basic screen where users come when
// they aren't logged in.
function HomeCtrl ($scope, $location, $http) {

  // if logged in then redirect them to the home page



  $scope.fullname = "Dave Carpenter";

  $http.get('/login').success(function(data, status, headers, config) {
    $scope.user = data
  });

}