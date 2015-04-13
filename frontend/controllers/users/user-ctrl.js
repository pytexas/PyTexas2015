pytx.controller('UserDetailCtrl', function($scope, $routeParams, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  $scope.set_title($routeParams.username);
  $scope.social_map = {
    'about.me': {'domain': 'about.me/', 'icon': 'fa-user'},
    'facebook': {'domain': 'facebook.com/', 'icon': 'fa-facebook-square'},
    'github': {'domain': 'github.com/', 'icon': 'fa-github-square'},
    'gplus': {'domain': 'plus.google.com/+', 'icon': 'fa-google-plus-square'},
    'twitter': {'domain': 'twitter.com/', 'icon': 'fa-twitter-square'},
  };
  
  $scope.load_user = function (data) {
    $scope.user = data;
    $scope.user.social_handles.forEach($scope.process_handle);
  };
  
  $scope.process_handle = function (element, index, array) {
    element.url = 'http://' + $scope.social_map[element.site].domain + element.username;
    element.icon = $scope.social_map[element.site].icon;
  };
  
  $scope.get_user = function () {
    $scope.APIService.get('users/profile/' + $routeParams.username)
      .success($scope.load_user)
      .error(function () {
        $scope.show_error('Error Loading User');
      });
  };
  
  $scope.get_user();
});
