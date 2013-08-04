function BudgetingCtrl ($scope, $location, $http) {

  // request to confirm login
  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    // console.log(data);
    if (!("user" in $scope.data)) {
      $location.path('/');
    }
    $scope.user = $scope.data["user"];
    $scope.$parent.logged_in = true;

    $scope.spending_categories_route = '/users/' + $scope.user.user_id + '/spending_categories';

    getSpendingCategories();
  });

  var getSpendingCategories = function() {
  	$http.get($scope.spending_categories_route).success(function(data, status, headers, config) {
  		$scope.spending_categories = data;
  		console.log($scope.spending_categories);
  	});
  }

  $scope.changeBudgetedAmount = function(spending_category) {
  	alert(spending_category.category_name)
  }

}