function LogOutCtrl ($scope, $location, $http) {

  $http.get('/logout').success(function(data, status, headers, config) {
    $location.path('/');
  });
}