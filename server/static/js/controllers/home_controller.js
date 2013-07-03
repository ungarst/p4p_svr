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

  // prototyping functions to get todays date as dd/MM/yyyy and time as hh:mm:ss
  Date.prototype.today = function(){ 
    return ((this.getDate() < 10)?"0":"") + this.getDate() +"/"+(((this.getMonth()+1) < 10)?"0":"") + (this.getMonth()+1) +"/"+ this.getFullYear();
  };

  Date.prototype.timeNow = function(){
    return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
  };

  var date = new Date();
  var currentDateTime = String(date.today() + " " + date.timeNow());

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

  // this is just used so that the correct currency locale can be generated 
  // for a place holder
  $scope.price_example = 20;

  //default receipt
  $scope.new_receipt = {
    "storeName": "",
    "taxRate": "",
    "totalTransaction": "",
    "dateTime": currentDateTime,
    "category" : "",
    "items": [{"item":{"title":"Shirt","price":200},"itemQuantity":1}]
  };

  $scope.clearReceipt = function() {
    $scope.new_receipt = {
      "storeName":"",
      "taxRate" : "",
      "totalTransaction" : "",
      "category" : "",
      "dateTime": currentDateTime,
      "items": [{"item":{"title":"Shirt","price":200},"itemQuantity":1}]
    };
  }

  $scope.saveReceipt = function() {
    $scope.new_receipt.totalTransaction = Number($scope.new_receipt.totalTransaction.
      replace(/[^0-9\.]+/g,""));
    $scope.new_receipt.taxRate = Number($scope.new_receipt.taxRate.
      replace(/[^0-9\.]+/g,""));

    $http.post($scope.receipts_url, $scope.new_receipt).success(function(data, status, headers, config) {
      $('#addReceiptModal').modal('hide');
      // request to get receipt data from the site
      getReceipts(); 
      $scope.clearReceipt(); 
      $location.path('/home');
    });
  }
}