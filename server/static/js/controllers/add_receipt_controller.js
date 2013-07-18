function AddReceiptCtrl ($scope, $location, $http) {

  $scope.receiptTotal = 0.0;

  // unload the background image
  $(document).ready(function(){
    $("body").css({
      "background-image":""
    });

    $('#addreceiptdatetimepicker').datetimepicker({
      language: 'en-US'
    });

  });

  // this is just used so that the correct currency locale can be generated 
  // for a place holder
  $scope.price_example = 20;

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
    "store_name": "",
    //"totalTransaction": "",
    "date_time": currentDateTime,
    "items": [
      {
        "name": "",
        "quantity": "",
        "price_per_item": ""
      }
    ]
  }

  $scope.clearData = function() {
    $scope.receipt = {
      "store_name": "",
      //"totalTransaction": "",
      "date_time": currentDateTime,
      "items": [
        {
          "name": "",
          "quantity": "",
          "price_per_item": ""
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
                $scope.receipt.items[i].price_per_item === "") {
        toastr.error("Please finish editing your current item before adding another one!")
        // console.log("Please finish and then add an item");
        return
      }
    }
    $scope.receipt.items.push({"name": "", "quantity": "", "price_per_item": ""});
  };

  $scope.removeItem = function(item) {
    var index = $scope.receipt.items.indexOf(item);
    $scope.receipt.items.splice(index, 1);
    $scope.calculateTotal();
  };

  $scope.submitReceipt = function() {
    $scope.receipt.total_transaction = $scope.receiptTotal;
    console.log($scope.receipt);
      // replace(/[^0-9\.]+/g,""));
    for (var i = 0 ; i < $scope.receipt.items.length ; i++) {
      $scope.receipt.items[i].quantity = Number($scope.receipt.items[i].quantity.
      replace(/[^0-9\.]+/g,""));
      $scope.receipt.items[i].price_per_item = Number($scope.receipt.items[i].price_per_item.
      replace(/[^0-9\.]+/g,""));
    }

    $http.post($scope.receipts_url, $scope.receipt).success(function(data, status, headers, config) {
      $location.path('/home');
    });
  }  

  $scope.calculateTotal = function() {
    var total = 0.0

    // console.log("here");
    for (var i = 0; i < $scope.receipt.items.length ; i++) {
      item = $scope.receipt.items[i];

      // console.log(item.quantity + " " + item.pricePerItem);
      var numQuantity = parseInt(item.quantity);
      var numPricePerItem = parseFloat(item.price_per_item);

      // console.log(numQuantity + " " + numPricePerItem);

      if (isNaN(numQuantity) || isNaN(numPricePerItem)) {
        // console.log("One is nan");
      } else {
        total += (numPricePerItem * numQuantity);
      }

      
    }

    // for (item in $scope.receipt.items) {
    //   console.log(item);
    //   console.log(item.quantity + " " + item.pricePerItem);
    //   var numQuantity = parseInt(item.quantity);
    //   var numPricePerItem = parseInt(item.pricePerItem);

    //   console.log(numQuantity + " " + numPricePerItem);

    //   if (isNaN(numQuantity) || isNaN(numPricePerItem)) {
    //     console.log("One is nan");
    //   } else {
    //     total += (numPricePerItem * numQuantity);
    //   }

    // }
    // console.log("setting total to " + total);
    $scope.receiptTotal = total;
  };

}