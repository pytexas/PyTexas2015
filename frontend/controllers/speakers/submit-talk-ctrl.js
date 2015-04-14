pytx.controller('SubmitTalkCtrl', function($scope, $location, APIFactory) {
  $scope.APIService = new APIFactory('v1', $scope);
  $scope.set_title('Submit A Talk');
  
  $scope.do_submit = function () {
    if ($scope.talkForm.$valid) {
      $scope.APIService.post_form('speakers/submit-talk', $scope.form).success($scope.talk_accepted);
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
  
  if (!$scope.logged_in) {
    $location.url('/user/login?next=' + encodeURIComponent($location.path()));
  }
  
  $scope.reset();
});
