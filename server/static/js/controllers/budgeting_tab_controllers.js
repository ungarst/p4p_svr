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

	};

	$scope.$on('SpendingCategoriesLoaded', $scope.onDataLoad);

	if ($scope.dataIsLoaded) {
		$scope.onDataLoad();
	}
}

function BudgetingGraphsCtrl ($scope) {
	$scope.count = 0;
}

function BudgetingEditCtrl ($scope, $http) {
	
	$scope.editCategory = function(category) {

	};

	// Fuck confirmations for now
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
}

