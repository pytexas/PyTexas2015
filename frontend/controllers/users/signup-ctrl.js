pytx.controller('SignUpCtrl', function($scope, $routeParams, $location, $timeout, $mdToast, $rootScope, APIFactory) {
  $scope.APIService = new APIFactory('v1', $scope);
  $scope.set_title('Sign Up');
  $scope.form = {};
  var searchObject = $location.search();
  $scope.next = searchObject.next || '/';
  
  $scope.do_signup = function () {
    if ($scope.signupForm.$valid) {
      $scope.APIService.post_form('users/sign-up', $scope.form)
        .success($scope.do_next);
    }
    
    else {
      $scope.show_error('Invalid form data');
    }
  };
  
  $scope.do_next = function (data) {
    $mdToast.show(
      $mdToast.simple()
        .content('Sign Up Successful!')
        .position('bottom left')
        .hideDelay(5000)
    );
    $rootScope.logged_in = true;
    
    $timeout(function () {
      $location.url($scope.next);
    }, 210);
  };
  
  $scope.remove_handle = function ($index) {
    $scope.form.social_handles.splice($index, 1);
  };
  
  $scope.add_handle = function () {
    if (!$scope.form.social_handles) {
      $scope.form.social_handles = [];
    }
    
    $scope.form.social_handles.unshift({username: '', site: 'twitter'});
  };
});
