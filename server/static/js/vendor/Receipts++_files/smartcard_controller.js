function SmartcardCtrl ($scope, $http, $location) {

  $scope.name = "World!"

  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    if (!("user" in $scope.data)) {
      $location.path('/');
    }
    $scope.user = $scope.data["user"];
    $scope.$parent.logged_in = true;
    
    // Make requests for data here

    $http.get('/users/' + $scope.user.user_id + '/smartcard').success(function(data, status, headers, config) {
      $scope.smartcard = data;
      if ("smartcard_number" in $scope.smartcard) {
        $scope.has_smartcard = true;
        if ($scope.smartcard.enabled) {
          $scope.smartcard.status = "Enabled";
        } else {
          $scope.smartcard.status = "Disabled";
        }
      } else {
        $scope.has_smartcard = false;
      }
    });
  }); 

  $scope.changeCardStatus = function() {
    var new_status = !($scope.smartcard.enabled)
    var req = {"enabled" : new_status}
    console.log(req)
    $http.put('/users/' + $scope.user.user_id + '/smartcard', req).success(function(data, status, headers, config) {
      $scope.smartcard = data;
      if ("smartcard_number" in $scope.smartcard) {
        $scope.has_smartcard = true;
        if ($scope.smartcard.enabled) {
          $scope.smartcard.status = "Enabled";
        } else {
          $scope.smartcard.status = "Disabled";
        }
      } else {
        $scope.has_smartcard = false;
      }
    });
  }

  $scope.deleteCard = function() {
    
    $http({method: 'DELETE', url: '/users/' + $scope.user.user_id + '/smartcard'}).success(function(data, status, headers, config) {
      $scope.smartcard = data;
      if ("smartcard_number" in $scope.smartcard) {
        $scope.has_smartcard = true;
        if ($scope.smartcard.enabled) {
          $scope.smartcard.status = "Enabled";
        } else {
          $scope.smartcard.status = "Disabled";
        }
      } else {
        $scope.has_smartcard = false;
      }
    });
  }
}