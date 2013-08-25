function ReceiptCtrl ($scope, $routeParams,$location, $http) {
  
  // unload the background image
  $(document).ready(function(){
    $("body").css({
      "background-image":""
    });
  });

  // request to confirm login
  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    if (!("user" in $scope.data)) {
      $location.path('/');
    }
    $scope.user = $scope.data["user"];
    $scope.$parent.logged_in = true;
    $scope.receipt_url = '/users/' + $scope.user.user_id + '/receipts/' + $routeParams.receiptId;
    $http.get($scope.receipt_url).success(function(data, status, headers, config) {
      $scope.receipt = data["receipt"];
    });
  }); 
}