function AddReceiptCtrl ($scope, $location, $http) {

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

  $scope.receipt = {
    "storeName": "",
    "totalTransaction": "",
    "dateTime": currentDateTime,
    "items": [
      {
        "name": "",
        "quantity": "",
        "pricePerItem": ""
      }
    ]
  }

  $scope.clearData = function() {
    $scope.receipt = {
      "storeName": "",
      "totalTransaction": "",
      "dateTime": currentDateTime,
      "items": [
        {
          "name": "",
          "quantity": "",
          "pricePerItem": ""
        }
      ]
    }
  };

  $scope.cancel = function() {
    $location.path('/home');
  }

  $scope.addItem = function() {
    for (var i = 0 ; i < $scope.receipt.items.length ; i++) {
      if ($scope.receipt.items[i].name === "" || 
                $scope.receipt.items[i].quantity === "" || 
                $scope.receipt.items[i].pricePerItem === "") {
        toastr.error("Please finish editing your current item before adding another one!")
        console.log("Please finish and then add an item");
        return
      }
    }
    $scope.receipt.items.push({"name": "", "quantity": "", "pricePerItem": ""});
  };

  $scope.removeItem = function(item) {
    var index = $scope.receipt.items.indexOf(item);
    $scope.receipt.items.splice(index, 1);
  };

  $scope.submitReceipt = function() {
    $scope.receipt.totalTransaction = Number($scope.receipt.totalTransaction.
      replace(/[^0-9\.]+/g,""));
    for (var i = 0 ; i < $scope.receipt.items.length ; i++) {
      $scope.receipt.items[i].quantity = Number($scope.receipt.items[i].quantity.
      replace(/[^0-9\.]+/g,""));
      $scope.receipt.items[i].pricePerItem = Number($scope.receipt.items[i].pricePerItem.
      replace(/[^0-9\.]+/g,""));
    }
    $http.post($scope.receipts_url, $scope.receipt).success(function(data, status, headers, config) {
      $location.path('/home');
    });
  }  

}