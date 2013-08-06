function BudgetingCtrl ($scope, $location, $http) {

  var currDate = new Date();

  $scope.month = (currDate.getMonth()+1).toString();
  $scope.year = currDate.getFullYear().toString();

  // request to confirm login
  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    // console.log(data);
    if (!("user" in $scope.data)) {
      $location.path('/');
    }
    $scope.user = $scope.data["user"];
    $scope.$parent.logged_in = true;

    if ($scope.user.other_monthly_allowance == null) {
      console.log("here");
      $scope.catch_all_not_set = true;
    } else {
      $scope.not_editing_catch_all = true;
      console.log("here2");
    }

    $scope.spending_categories_route = '/users/' + $scope.user.user_id + '/budgeting_report';

    $scope.refreshData();
  });

  $scope.changeBudgetedAmount = function(spending_category) {
  	alert(spending_category.category_name)
  }

  $scope.enableEditing = function(spending_category) {
    spending_category.editing = true;
    // alert("going to edit " + spending_category.category_name);
  }

  $scope.updateAllowance = function(spending_category) {
    console.log(spending_category.monthly_allowance);
    var url = "/users/" + $scope.user.user_id + "/spending_categories/" + spending_category.spending_category_id;
    var data = {"monthly_allowance": parseFloat(spending_category.monthly_allowance)};
    console.log(url);
    
    $http.put(url, data).success(function(data, status, headers, config) {
      console.log(data);    
      spending_category.editing = false;  
    });
    
  }

  $scope.editCatchAll = function() {
    $scope.catch_all_not_set = false;
    $scope.not_editing_catch_all = false;
    $scope.editing_catch_all = true;
  }

  $scope.saveCatchAll = function() {
    var url = "/users/" + $scope.user.user_id;
    var data = {"other_monthly_allowance": $scope.user.other_monthly_allowance }
    $http.put(url, data).success(function(data, status, headers, config) {
      $scope.not_editing_catch_all = true;
      $scope.editing_catch_all = false;
    });
  }

  $scope.refreshData = function() {
    var url = $scope.spending_categories_route + "?month=" + $scope.month + "&year=" + $scope.year;
    $http.get(url).success(function(data, status, headers, config) {
      $scope.other = data.other;
      $scope.spending_categories = [];
      for (var i = 0 ; i < data.spending_categories.length ; i++) {
        if (!$scope.spending_categories[Math.floor(i/3)]) {
          $scope.spending_categories[Math.floor(i/3)] = [];
        }
        data.spending_categories[i].editing = false;
        data.spending_categories[i].ratio = (100 * data.spending_categories[i].monthly_spend / data.spending_categories[i].monthly_allowance).toFixed(2);
        $scope.spending_categories[Math.floor(i/3)].push(data.spending_categories[i])
        // $scope.spending_categories[Math.floor(i/3)][i%3].editing = false;
      }
      console.log($scope.spending_categories);
    });    
  };

  $scope.seriousness = function(ratio) {
    if (ratio < 80) {
      return "seriousness-okay";
    } else if (ratio < 100) {
      return "seriousness-warning";
    } else {
      return "seriousness-danger";
    }
  };

}