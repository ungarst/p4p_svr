function SignUpCtrl ($scope, $location, $http) {

  $(document).ready(function(){
    $("body").css({
      "background-image":""
    });
  });

  $scope.params = {
    "first_name": "",
    "last_name": "",
    "email_address": "",
    "password": "",
    "confirm": ""
  };

  $scope.signup = function() {
    if($scope.params.confirm == $scope.params.password && $scope.params.password !== ""){
      $http.post('/signup', $scope.params).success(function(data, status, headers, config) {
        if (Object.prototype.hasOwnProperty.call(data, "error")) {
          toastr.error("Use another one and try again", "Email address already taken");
        } else {
          $location.path('/home');
        }
      });
    } else {
      toastr.error("Passwords do not match.");
      $scope.params.password = "";
      $scope.params.confirm = "";
    }
  };

  console.log("In the sign up controller");
}