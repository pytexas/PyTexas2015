pytx.controller('VideosCtrl', function($scope, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  $scope.set_title('Videos');
  
  $scope.load_videos = function (data) {
    $scope.videos = data;
  };
  
  $scope.get_videos = function () {
    $scope.APIService.get('speakers/videos')
      .success($scope.load_videos)
      .error(function () {
        $scope.show_error('Error Loading Videos');
      });
  };
  
  $scope.get_videos();
});
