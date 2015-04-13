pytx.controller('LoginCtrl', function($scope, $routeParams, $location, $timeout, $mdToast, $rootScope, APIFactory) {
  $scope.APIService = new APIFactory('v1', $scope);
  $scope.set_title('Login');
  $scope.form = {};
  
  $scope.do_login = function () {
    if ($scope.loginForm.$valid) {
      $scope.APIService.post_form('users/login', $scope.form).success($scope.next)
    }
    
    else {
      $scope.show_error('Invalid form data');
    }
  };
  
  $scope.next = function (data) {
    var searchObject = $location.search();
    var next = searchObject.next || '/';
    $mdToast.show(
      $mdToast.simple()
        .content('Login Successful!')
        .position('bottom left')
        .hideDelay(5000)
    );
    $rootScope.logged_in = true;
    
    $timeout(function () {
      $location.url(next);
    }, 210);
  };
});
