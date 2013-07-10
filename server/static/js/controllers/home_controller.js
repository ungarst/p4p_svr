function HomeCtrl ($scope, $location, $http) {
  
  // unload the background image
  $(document).ready(function(){
    $("body").css({
      "background-image":""
    });

    $('#addreceiptdatetimepicker').datetimepicker({
      language: 'en-US'
    });

  });

  $scope.create_receipt = function() {
    $location.path('/add_receipt');
  }

  $scope.receipts_url = "";

  var getReceipts = function() {
    $http.get($scope.receipts_url).success(function(data, status, headers, config) {
      $scope.user_receipts = data["receipts"];
      console.log($scope.user_receipts)
    });
  }

  // request to confirm login
  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    // console.log(data);
    if (!("user" in $scope.data)) {
      $location.path('/');
    }
    $scope.user = $scope.data["user"];
    $scope.$parent.logged_in = true;

    $scope.receipts_url = '/users/' + $scope.user.user_id + '/receipts';

    // request to get receipt data from the site
    getReceipts(); 
  });

  $scope.params = {"email_address": "", "password": ""};

  $scope.login = function() {
    $http.post('/login', $scope.params).success(function(data, status, headers, config) {
      $location.path('/home');
    });
  }

}