pytx.controller('ProfileCtrl', function($scope, $routeParams, $location, $timeout, $mdToast, $rootScope, APIFactory) {
  $scope.APIService = new APIFactory('v1', $scope);
  $scope.set_title('My Profile');
  $scope.form = {};
  $scope.update = true;
  var searchObject = $location.search();
  $scope.next = searchObject.next;
  
  $scope.do_edit = function () {
    if ($scope.signupForm.$valid) {
      $scope.APIService.post_form('users/my-profile', $scope.form)
        .success($scope.do_next);
    }
    
    else {
      $scope.show_error('Invalid form data');
    }
  };
  
  $scope.do_next = function (data) {
    $mdToast.show(
      $mdToast.simple()
        .content('Profile Updated Successfully!')
        .position('bottom left')
        .hideDelay(5000)
    );
    
    if ($scope.next) {
      $timeout(function () {
        $location.url($scope.next);
      }, 210);
    }
  };
  
  $scope.remove_handle = function ($index) {
    $scope.form.social_handles.splice($index, 1);
  };
  
  $scope.add_handle = function () {
    $scope.form.social_handles.unshift({username: '', site: 'twitter'});
  };
  
  $scope.get_profile = function () {
    $scope.APIService.get('users/my-profile', $scope.form)
      .success($scope.load_profile);
  };
  
  $scope.load_profile = function (data) {
    $scope.form = data;
  };
  
  if (!$scope.logged_in) {
    $location.url('/user/login?next=' + encodeURIComponent($location.path()));
  }
  
  else {
    $scope.get_profile();
  }
});
