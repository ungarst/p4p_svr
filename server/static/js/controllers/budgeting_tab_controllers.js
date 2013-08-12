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

function BudgetingEditCtrl ($scope) {
	$scope.count = 0;
}

