pytx.controller('SubmitTalkCtrl', function($scope, $location, $timeout, APIFactory) {
  $scope.APIService = new APIFactory('v1', $scope);
  $scope.set_title('Submit A Talk');
  $scope.closed = true;
  
  $scope.do_submit = function () {
    if ($scope.talkForm.$valid) {
      $scope.APIService.post_form('speakers/submit-talk', $scope.form)
        .success($scope.talk_accepted);
    }
    
    else {
      $scope.show_error('Invalid form data');
    }
  };
  
  $scope.talk_accepted = function () {
    $scope.thanks = true;
  };
  
  $scope.reset = function () {
    var searchObject = $location.search();
    $scope.thanks = false;
    $scope.form = {
      stype: searchObject.stype || 'talk-short',
      level: 'beginner'
    };
  };
  
  $scope.is_closed = function () {
    if ($scope.conf_obj) {
      if ($scope.conf_obj.cfp_open && $scope.conf_obj.cfp_closed) {
        var now = moment();
        var open = moment($scope.conf_obj.cfp_open);
        var closed = moment($scope.conf_obj.cfp_closed);
        
        if (open <= now && now <= closed) {
          return false;
        }
      }
    }
    
    else {
      $timeout($scope.page_checks, 300);
    }
    
    return true;
  };
  
  $scope.page_checks = function () {
    if ($scope.is_closed()) {
      
    }
    
    else if (!$scope.logged_in) {
      $location.url('/user/login?next=' + encodeURIComponent($location.path()));
    }
    
    //todo: redo with jwt
    //else if ($cookies.angular_logged_in != 'speaker') {
    //  $location.url('/user/my-profile?next=' + encodeURIComponent($location.path()));
    //}
    
    else {
      $scope.closed = false;
      $scope.reset();
    }
  };
  
  $scope.page_checks();
});
