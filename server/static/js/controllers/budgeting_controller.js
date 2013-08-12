function BudgetingCtrl ($scope, $location, $http) {

  var currDate = new Date();

  $scope.month = (currDate.getMonth()+1).toString();
  $scope.year = currDate.getFullYear().toString();

  $scope.dataIsLoaded = false;

  $scope.tabs = [
    {
      "title": "Overview",
      "page" : "static/partials/budgeting/overview.html"
    },
    {
      "title": "Graphs",
      "page": "static/partials/budgeting/graphs.html"
    },
    {
      "title": "Add/Edit Categories",
      "page": "static/partials/budgeting/edit.html"
    }
  ];
  $scope.tabs.activeTab = 0;

  

  // request to confirm login
  $http.get('/login').success(function(data, status, headers, config) {
    if (!("user" in data)) {
      $location.path('/');
    }
    $scope.user = data["user"];
    $scope.$parent.logged_in = true;

    // if ($scope.user.other_monthly_allowance === null) {
    //   $scope.catch_all_not_set = true;
    // } else {
    //   $scope.not_editing_catch_all = true;
    // }

    $scope.spending_categories_route = '/users/' + $scope.user.user_id + '/budgeting_report';
    $scope.refreshData();
  });


  $scope.enableEditing = function(spending_category) {
    spending_category.editing = true;
  };

  $scope.updateAllowance = function(spending_category) {
    console.log(spending_category.monthly_allowance);
    var url = "/users/" + $scope.user.user_id + "/spending_categories/" + spending_category.spending_category_id;
    var data = {"monthly_allowance": parseFloat(spending_category.monthly_allowance)};
    console.log(url);
    
    $http.put(url, data).success(function(data, status, headers, config) {
      console.log(data);
      spending_category.editing = false;
    });
    
  };

  $scope.editCatchAll = function() {
    $scope.catch_all_not_set = false;
    $scope.not_editing_catch_all = false;
    $scope.editing_catch_all = true;
  };

  $scope.saveCatchAll = function() {
    var url = "/users/" + $scope.user.user_id;
    var data = {"other_monthly_allowance": $scope.user.other_monthly_allowance };
    $http.put(url, data).success(function(data, status, headers, config) {
      $scope.not_editing_catch_all = true;
      $scope.editing_catch_all = false;
    });
  };

  $scope.refreshData = function() {
    var url = $scope.spending_categories_route + "?month=" + $scope.month + "&year=" + $scope.year;
    $http.get(url).success(function(data, status, headers, config) {
      $scope.other = data.other;
      $scope.spending_categories = data.spending_categories;

      $scope.dataIsLoaded = true;
      $scope.$broadcast('SpendingCategoriesLoaded');
      // console.log($scope.spending_categories);
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