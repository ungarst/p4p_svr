// This will just be the basic screen where users come when
// they aren't logged in.
function RootCtrl ($scope, $location, $http) {

  $(document).ready(function(){
    $("body").css({
      "background-image":"url(static/img/halfBeach1080.png)",
      "background-position":"center",
      "background-repeat":"no-repeat"
    });
  });

  // if logged in then redirect them to the home page

  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    if ("user" in $scope.data) {
      $location.path('/home');
    }
  });

  $scope.params = {"email_address": "", "password": ""};

  $scope.login = function() {
    $http.post('/login', $scope.params).success(function(data, status, headers, config) {
      $location.path('/home');
    });
  }
}
