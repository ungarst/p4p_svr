function HomeCtrl ($scope, $location, $http) {
  
  // request to confirm login
  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    console.log(data);
    if (!("user" in $scope.data)) {
      $location.path('/');
    }
    $scope.user = $scope.data["user"];
    $scope.$parent.logged_in = true;

    var receipts_url = '/users/' + $scope.user.user_id + '/receipts';

    // request to get receipt data from the site
    $http.get(receipts_url).success(function(data, status, headers, config) {
      $scope.user_receipts = data["receipts"];
    });  
  });

  $scope.params = {"email_address": "", "password": ""};

  $scope.login = function() {
    $http.post('/login', $scope.params).success(function(data, status, headers, config) {
      $location.path('/home');
    });
  }
}