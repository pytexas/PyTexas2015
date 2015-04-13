pytx.controller('ProposedTalksCtrl', function($scope, $rootScope, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  $scope.set_title('Proposed Talks');
  
  $scope.load_talks = function (data) {
    $scope.talks = data;
  };
  
  $scope.get_talks = function () {
    $scope.APIService.get('speakers/proposed-talks')
      .success($scope.load_talks)
      .error(function () {
        $scope.show_error('Error Loading Talks');
      });
  };
  
  $scope.get_talks();
});
