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
    });
  }

  var getSpendingReport = function() {
    $http.get('/users/' + $scope.user.user_id + '/spending_report').success(function(data, status, headers, config) {
      //console.log(data);
      $scope.spending_categories = data.spending_categories;
      $scope.daily_spends = data.daily_spends;
      $scope.weeks_spending = 0.0
      for (var i = 0 ; i < $scope.daily_spends.length ; i++) {
        $scope.weeks_spending += $scope.daily_spends[i].total_spend;
      }
      $scope.weeks_spending = $scope.weeks_spending.toFixed(2);
    });
  };

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
    // getSpendingReport(); 
  });



  $scope.params = {"email_address": "", "password": ""};

  $scope.login = function() {
    $http.post('/login', $scope.params).success(function(data, status, headers, config) {
      $location.path('/home');
    });
  }

  // this is just used so that the correct currency locale can be generated 
  // for a place holder
  $scope.price_example = 20;

  $scope.goToReceipt = function(receipt) {
    $location.path("/receipt/"+receipt.receipt_id);
  }

}