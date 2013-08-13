google.setOnLoadCallback(function() {
  angular.bootstrap(document.body, ['rppApp']);
});
google.load('visualization', '1', {packages: ['corechart']});

// Declares the modules that our app is going to use
var rppApp = angular.module('rppApp', ['ngCookies', 'ngResource', 'ui.utils', 'ui.bootstrap', '$strap.directives']); // , 'ui.bootstrap' 

// Need to use different symbols as flask uses {{ and }}
rppApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('<[');
    $interpolateProvider.endSymbol(']>');
});

// Routes for our application
rppApp.config(function($routeProvider) {
  $routeProvider
      .when('/',
      {
        templateUrl: 'static/partials/root.html',
        controller: 'RootCtrl'
      })
      .when ('/receipt/:receiptId',
      {
        templateUrl: 'static/partials/receipt.html',
        controller: 'ReceiptCtrl'
      })
      .when('/home',
      {
        templateUrl: 'static/partials/home.html',
        controller: 'HomeCtrl'
      })
      .when ('/signup',
      {
        templateUrl: 'static/partials/signup.html',
        controller: 'SignUpCtrl'
      })
      .when('/login',
      {
        templateUrl: 'static/partials/login.html',
        controller: 'LogInCtrl'
      })
      .when('/add_receipt',
      {
        templateUrl: 'static/partials/add_receipt.html',
        controller: 'AddReceiptCtrl'
      })
      .when('/smartcard',
      {
        templateUrl: 'static/partials/smartcard_settings.html',
        controller: 'SmartcardCtrl'
      })
      .when('/budgeting',
      {
        templateUrl: 'static/partials/budgeting.html',
        controller: 'BudgetingCtrl'
      })
      .otherwise(
      {
        redirectTo: "/"
      });
});

rppApp.directive('pieChart', function ($timeout) {
  return {
    restrict: 'EA',
    scope: {
      width:    '@width',
      height:   '@height',
      data:     '=data',
      selectFn: '&select'
    },
    link: function($scope, $elm, $attr) {
      
      // Create the data table and instantiate the chart
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Label');
      data.addColumn('number', 'Amount Spent');
      var chart = new google.visualization.PieChart($elm[0]);

      draw();
      
      // Watches, to refresh the chart when its data, title or dimensions change
      $scope.$watch('data', function() {
        draw();
      }, true); // true is for deep object equality checking
      $scope.$watch('title', function() {
        draw();
      });
      $scope.$watch('width', function() {
        draw();
      });
      $scope.$watch('height', function() {
        draw();
      });

      // Chart selection handler
      google.visualization.events.addListener(chart, 'select', function () {
        var selectedItem = chart.getSelection()[0];
        if (selectedItem) {
          $scope.$apply(function () {
            $scope.selectFn({selectedRowIndex: selectedItem.row});
          });
        }
      });
        
      function draw() {
        if (!draw.triggered) {
          draw.triggered = true;
          $timeout(function () {
            draw.triggered = false;
            var label, value;
            data.removeRows(0, data.getNumberOfRows());
            angular.forEach($scope.data, function(row) {
              label = row[0];
              value = parseFloat(row[1], 10);
              if (!isNaN(value)) {
                data.addRow([row[0], value]);
              }
            });
            var options = {'width': $scope.width,
                           'height': $scope.height,
                           'chartArea': {'width': '100%', 'height': '100%'}
                          };
            chart.draw(data, options);
            // No raw selected
            $scope.selectFn({selectedRowIndex: undefined});
          }, 0, true);
        }
      }
    }
  };
});

rppApp.directive('columnChart', function ($timeout) {
  return {
    restrict: 'EA',
    scope: {
      width:    '@width',
      height:   '@height',
      data:     '=data',
      selectFn: '&select'
    },
    link: function($scope, $elm, $attr) {
      
      // Create the data table and instantiate the chart
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Label');
      data.addColumn('number', 'Amount Spent');
      var chart = new google.visualization.ColumnChart($elm[0]);

      draw();
      
      // Watches, to refresh the chart when its data, title or dimensions change
      $scope.$watch('data', function() {
        draw();
      }, true); // true is for deep object equality checking
      $scope.$watch('title', function() {
        draw();
      });
      $scope.$watch('width', function() {
        draw();
      });
      $scope.$watch('height', function() {
        draw();
      });

      // Chart selection handler
      google.visualization.events.addListener(chart, 'select', function () {
        var selectedItem = chart.getSelection()[0];
        if (selectedItem) {
          $scope.$apply(function () {
            $scope.selectFn({selectedRowIndex: selectedItem.row});
          });
        }
      });
        
      function draw() {
        if (!draw.triggered) {
          draw.triggered = true;
          $timeout(function () {
            draw.triggered = false;
            var label, value;
            data.removeRows(0, data.getNumberOfRows());
            angular.forEach($scope.data, function(row) {
              label = row[0];
              value = parseFloat(row[1], 10);
              if (!isNaN(value)) {
                data.addRow([row[0], value]);
              }
            });
            var options = {'width': $scope.width,
                           'height': $scope.height,
                           // 'backgroundColor' : 'red',
                           'chartArea': {'width': '100%', 'height': '68%'},
                           'hAxis.textStyle': {'color': 'red'},
                           'hAxis' : {'slantedText': true,
                                      'slantedTextAngle': 60 },
                           'legend': {'position': 'none'},
                          };
            chart.draw(data, options);
            // No raw selected
            $scope.selectFn({selectedRowIndex: undefined});
          }, 0, true);
        }
      }
    }
  };
});


