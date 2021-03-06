function BudgetingOverviewCtrl ($scope) {

  $scope.onDataLoad = function() {
    $scope.spending_categories_matrix = [];

    for (var i = 0 ; i < $scope.spending_categories.length ; i++) {
      if (!$scope.spending_categories_matrix[Math.floor(i/3)]) {
        $scope.spending_categories_matrix.push([]);
      }
      $scope.spending_categories[i].ratio = (100 * $scope.spending_categories[i].monthly_spend / $scope.spending_categories[i].monthly_allowance).toFixed(2);
      $scope.spending_categories_matrix[Math.floor(i/3)].push($scope.spending_categories[i]);
    }

    $scope.user_other_ratio = (100 * $scope.other / $scope.user.other_monthly_allowance).toFixed(2);

  };

  $scope.$on('SpendingCategoriesLoaded', $scope.onDataLoad);

  if ($scope.dataIsLoaded) {
    $scope.onDataLoad();
  }
}

function BudgetingGraphsCtrl ($scope, $http) {

  $scope.shouldShowPieChart = function() {
    return $scope.spending_categories.length !== 0;
  };

  var createGTableSpendingCategorySpends = function() {
    var dataList = [];

    for (var i = 0; i < $scope.spending_categories.length; i++) {
      var spendingCategory = $scope.spending_categories[i];
      var spendingCategoryAsList = [spendingCategory.category_name, spendingCategory.monthly_spend];
      dataList.push(spendingCategoryAsList);
    }
    dataList.push(["Other", $scope.other]);

    return dataList;
  };

  var getDailySpendTotals = function() {
    var url = '/users/' + $scope.user.user_id + "/daily_spends_in_month" + "?month=" + $scope.month + "&year=" + $scope.year;
    $http.get(url).success(function(data, status, headers, config) {
      $scope.gTableDailySpendTotals = data;
      // console.log($scope.gTableDailySpendTotals);
    });
  };

  $scope.onDataLoad = function() {
    $scope.gTableSpendingCategorySpends = createGTableSpendingCategorySpends();
    getDailySpendTotals();
  };

  $scope.$on('SpendingCategoriesLoaded', $scope.onDataLoad);

  if ($scope.dataIsLoaded) {
    $scope.onDataLoad();
  }
}

function BudgetingEditCtrl ($scope, $http) {
  
  $scope.onDataLoad = function() {
    for (var category in $scope.spending_categories) {
      category.editing = false;
    }
  };

  $scope.saveEdit = function(category) {
    category.editing = false;

    // Send updates to backend
    var url = "/users/" + $scope.user.user_id.toString() +
        "/spending_categories/" + category.spending_category_id.toString();
    var data = {"monthly_allowance": category.monthly_allowance };

    $http.put(url, data).success(function(data, status, headers, config){
      $scope.refreshData();
    });
  };

  $scope.editCategory = function(category) {
    category.editing = true;
  };

  // No confirmations for now
  $scope.deleteCategory = function(category) {
    // Pull out the id now for deleting from the API
    var categoryId = category.spending_category_id;

    // Remove it from the list now so that the user sees instant change
    var index = $scope.spending_categories.indexOf(category);
    $scope.spending_categories.splice(index, 1);

    // Remove the category from the backend
    var url = "/users/" + $scope.user.user_id.toString() + "/spending_categories/" + categoryId.toString();
    $http.delete(url).success(function(data, status, headers, config) {
      $scope.refreshData();
    });

  };

  $scope.editUserCatchAll = function() {
    $scope.editingCatchAll = true;
  };

  $scope.saveUserCatchAll = function() {
    $scope.editingCatchAll = false;

    // Save changes to backend
    var url = "/users/" + $scope.user.user_id.toString();
    var data = {"other_monthly_allowance": $scope.user.other_monthly_allowance};
    $http.put(url, data).success(function(data, status, headers, config) {
      $scope.refreshData();
    });

  };

  $scope.openModal = function () {
    $scope.modalOpen = true;
    $scope.newCategory = {
      "category_name": "",
      "monthly_allowance": 0
    };
  };

  $scope.closeModal = function () {
    $scope.modalOpen = false;
  };

  $scope.saveNewCategory = function() {
    var url = "/users/" + $scope.user.user_id.toString() + "/spending_categories";
    var data = $scope.newCategory;
    $http.post(url, data).success(function(data, success, headers, config) {
      $scope.closeModal();
      $scope.refreshData();
    });
  };

  // $scope.items = ['item1', 'item2'];

  $scope.opts = {
    backdropFade: true,
    dialogFade:true
  };

  $scope.$on('SpendingCategoriesLoaded', $scope.onDataLoad);

  if ($scope.dataIsLoaded) {
    $scope.onDataLoad();
  }
}

