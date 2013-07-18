function WeeklySpendingCtrl ($scope, $location, $http) {

  $scope.hasReport = false;
  
  $http.get('/login').success(function(data, status, headers, config) {
    $scope.data = data;
    // console.log(data);
    if (!("user" in $scope.data)) {
      $location.path('/');
    }
    $scope.user = $scope.data["user"];
    getSpendingReport(); 
  });

  var getSpendingReport = function() {
    $http.get('/users/' + $scope.user.user_id + '/spending_report').success(function(data, status, headers, config) {      
      //console.log(data);
      $scope.spending_categories = objToPairs(data.spending_categories);
      $scope.daily_spends_maps = data.daily_spends;
      $scope.weeks_spending = 0.0
      for (var i = 0 ; i < $scope.daily_spends_maps.length ; i++) {
        $scope.weeks_spending += $scope.daily_spends_maps[i].total_spend;
      }
      $scope.daily_spends = dailySpendsTransform($scope.daily_spends_maps);
      $scope.weeks_spending = $scope.weeks_spending.toFixed(2);
      $scope.hasReport = true;
    });
  }

  var objToPairs = function(obj) {
    pairs = [];
    for (var key in obj) {
      pairs.push([key, obj[key]]);
    }
    return pairs;
  }

  var dailySpendsTransform = function(daily_spends_maps) {
    daily_spends = [];
    for (var i = 0 ; i < daily_spends_maps.length ; i++) {
      daily_spends.push(kvDateTotalToList(daily_spends_maps[i]));
    }
    return daily_spends;
  }

  var kvDateTotalToList = function (kvDateTotal) {
    return [kvDateTotal.date, kvDateTotal.total_spend];
  }

  $scope.categoryChartTitle = "Spending by category";
  $scope.categoryChartWidth = 300;
  $scope.categoryChartHeight = 250;

  $scope.dailyChartTitle = "Amount spent each day";
  $scope.dailyChartWidth = 300;
  $scope.dailyChartHeight = 250;




}