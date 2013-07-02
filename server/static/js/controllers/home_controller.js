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

  Date.prototype.today = function(){ 
    return ((this.getDate() < 10)?"0":"") + this.getDate() +"/"+(((this.getMonth()+1) < 10)?"0":"") + (this.getMonth()+1) +"/"+ this.getFullYear();
  };

  Date.prototype.timeNow = function(){
    return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
  };

  var date = new Date();
  var currentDateTime = String(date.today() + " " + date.timeNow());

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

  $scope.price_example = 20;

  $scope.new_receipt = {
    "store_name":"",
    "tax_rate" : "",
    "total_transaction" : "",
    "date_time": currentDateTime
  };

  $scope.clearReceipt = function() {
    $scope.new_receipt = {
      "store_name":"",
      "tax_rate" : "",
      "total_transaction" : "",
      "date_time": currentDateTime
    };
  }
}