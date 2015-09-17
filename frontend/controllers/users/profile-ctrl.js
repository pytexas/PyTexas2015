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

pytx.controller('AvatarCtrl', function($scope, $mdToast, $location, APIFactory, StorageService) {
  $scope.APIService = new APIFactory('v1', $scope);
  $scope.set_title('My Profile Image');
  $scope.ret = $location.path();
  $scope.jwt = StorageService.get('pytx_jwt');
  var search_object = $location.search();
  
  $scope.get_image = function () {
    $scope.APIService.get('users/my-profile-image')
      .success($scope.load_image)
      .error(function () {
        $scope.show_error('Error getting image data.');
      });
  };
  
  $scope.load_image = function (data) {
    $scope.image = data;
  };
  
  $scope.load_gravatar = function (data) {
    $scope.load_image(data);
    var element = document.querySelector("#main-content");
    element.scrollTop = 0;
    
    $mdToast.show(
      $mdToast.simple()
        .content('Image Updated Successfully!')
        .position('bottom left')
        .hideDelay(5000)
    );
  };
  
  $scope.use_gravatar = function () {
    $scope.APIService.post('users/my-profile-image', {gravatar: 'true'})
      .success($scope.load_gravatar)
      .error(function () {
        $scope.show_error('Error setting Gravatar.');
      });
  };
  
  if (!$scope.logged_in) {
    $location.url('/user/login?next=' + encodeURIComponent($location.path()));
  }
  
  else {
    $scope.get_image();
    
    if (search_object.success) {
      $mdToast.show(
        $mdToast.simple()
          .content('Image Saved Successfully!')
          .position('bottom left')
          .hideDelay(5000)
      );
    }
    
    else if (search_object.error) {
      $scope.show_error('Error saving image.');
    }
  }
});
