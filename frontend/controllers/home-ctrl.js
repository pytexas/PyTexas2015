pytx.controller('HomeCtrl', function($scope, APIFactory) {
  $scope.set_title();
  $scope.APIService = new APIFactory('v1');
  $scope.latest_post = null;
  
  $scope.load_post = function (data) {
    $scope.latest_post = data;
  };
  
  $scope.get_post = function () {
    $scope.APIService.get('blog/latest')
      .success($scope.load_post)
      .error(function () {
        console.log('Silently failing post retrieval :-(');
      });
  };
  
  $scope.get_post();
});