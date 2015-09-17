pytx.controller('EditTalkCtrl', function($scope, $location, $routeParams, $mdToast, APIFactory) {
  $scope.APIService = new APIFactory('v1', $scope);
  $scope.set_title('Edit Talk');
  $scope.id = $routeParams.id;
  
  $scope.do_submit = function () {
    if ($scope.talkForm.$valid) {
      $scope.APIService.post_form('speakers/edit-talk/' + $scope.id, $scope.form).success($scope.talk_accepted);
    }
    
    else {
      $scope.show_error('Invalid form data');
    }
  };
  
  $scope.get_talk = function () {
    $scope.APIService.get('speakers/edit-talk/' + $scope.id, $scope.form).success($scope.load_talk);
  };
  
  $scope.talk_accepted = function () {
    $mdToast.show(
      $mdToast.simple()
        .content('Talk Update Successful!')
        .position('bottom left')
        .hideDelay(5000)
    );
    
    $location.path('/user/my-talks');
  };
  
  $scope.load_talk = function (data) {
    $scope.form = data;
  };
  
  if (!$scope.logged_in) {
    $location.url('/user/login?next=' + encodeURIComponent($location.path()));
  }
  
  //todo: redo with jwt
  //else if ($cookies.angular_logged_in != 'speaker') {
  //  $location.url('/user/my-profile?next=' + encodeURIComponent($location.path()));
  //}
  
  else {
    $scope.get_talk();
  }
});
