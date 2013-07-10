function AddReceiptCtrl ($scope, $location, $http) {

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
    "taxRate": "",
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
      "taxRate": "",
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

}