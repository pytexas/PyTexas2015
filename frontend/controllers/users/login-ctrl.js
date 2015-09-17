pytx.controller('LoginCtrl', function($scope, $routeParams, $location, $timeout, $mdToast, $rootScope, APIFactory, StorageService) {
  $scope.APIService = new APIFactory('v1', $scope);
  $scope.set_title('Login');
  $scope.form = {};
  var searchObject = $location.search();
  $scope.next = searchObject.next || '/';
  
  $scope.do_login = function () {
    if ($scope.loginForm.$valid) {
      $scope.APIService.post_form('token-auth', $scope.form).success($scope.do_next)
    }
    
    else {
      $scope.show_error('Invalid form data');
    }
  };
  
  $scope.do_next = function (data) {
    $mdToast.show(
      $mdToast.simple()
        .content('Login Successful!')
        .position('bottom left')
        .hideDelay(5000)
    );
    
    StorageService.set('pytx_jwt', data.token);
    $rootScope.logged_in = true;
    
    $timeout(function () {
      $location.url($scope.next);
    }, 210);
  };
});
