pytx.controller('TalkDetailCtrl', function($scope, $routeParams, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  $scope.set_title('Talk Details');
  
  $scope.load_talk = function (data) {
    $scope.talk = data;
    $scope.set_title(data.name);
  };
  
  $scope.get_talk = function () {
    $scope.APIService.get('speakers/talk/' + $routeParams.id)
      .success($scope.load_talk)
      .error(function () {
        $scope.show_error('Error Loading Talk');
      });
  };
  
  $scope.get_talk();
});
