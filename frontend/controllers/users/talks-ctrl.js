pytx.controller('TalkListCtrl', function($scope, $location, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  $scope.set_title('My Talks');
  
  $scope.load_talks = function (data) {
    $scope.talks = data;
  };
  
  $scope.get_talks = function () {
    $scope.APIService.get('speakers/my-talks')
      .success($scope.load_talks)
      .error(function () {
        $scope.show_error('Error Loading Talks');
      });
  };
  
  if (!$scope.logged_in) {
    $location.url('/user/login?next=' + encodeURIComponent($location.path()));
  }
  
  else {
    $scope.get_talks();
  }
});
