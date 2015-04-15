pytx.controller('ResetCtrl', function($scope, $location, APIFactory) {
  $scope.APIService = new APIFactory('v1', $scope);
  $scope.set_title('Retrieve Password');
  $scope.form = {};
  $scope.success = false;
  var searchObject = $location.search();
  $scope.secret = searchObject.secret;
  
  $scope.do_reset = function () {
    if ($scope.form.username && $scope.form.email) {
      $scope.show_error('Fill in one field only.');
    }
    
    else if ($scope.form.username || $scope.form.email) {
      $scope.APIService.post_form('users/reset-password', $scope.form)
        .success($scope.do_success);
    }
    
    else {
      $scope.show_error('Fill in a username or e-mail.');
    }
  };
  
  $scope.do_success = function () {
    $scope.success = true;
  };
  
  $scope.check_secret = function () {
    $scope.APIService.post('users/reset-password-finish', {secret: $scope.secret})
      .success($scope.do_check_success)
      .error($scope.do_check_error)
      .finally(function () {
        $scope.checking = false;
      });
  };
  
  $scope.do_check_success = function () {
    $scope.show_reset_form = true;
  };
  
  $scope.do_check_error = function () {
    $scope.check_error = true;
  };
  
  $scope.do_finish = function () {
    if ($scope.resetForm.$valid) {
      if ($scope.form.password == $scope.form.confirm) {
        $scope.APIService.post_form('users/reset-password-finish', {secret: $scope.secret, password: $scope.form.password})
          .success($scope.do_finish_success);
      }
      
      else {
        $scope.show_error('Password and confirmation do not match.');
      }
    }
    
    else {
      $scope.show_error('Fill in a password and confirmation.');
    }
  };
  
  $scope.do_finish_success = function () {
    $scope.finish_success = true;
    $scope.show_reset_form = false;
  };
  
  if ($scope.secret) {
    $scope.checking = true;
    $scope.check_secret();
  }
});
