pytx.controller('BlogCtrl', function($scope, $location, $routeParams, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  $scope.set_title("Blog");
  
  $scope.load_posts = function (data) {
    $scope.data = data;
    $scope.set_title(data.title);
  };
  
  $scope.get_posts = function () {
    var search = angular.copy($location.search());
    search = search || {};
    
    if ($routeParams.cat) {
      search.cat = $routeParams.cat
    }
    
    $scope.APIService.get('blog/posts', search)
      .success($scope.load_posts)
      .error(function () {
        $scope.show_error('Error Loading Blog Posts');
      });
  };
  
  $scope.get_posts();
});

pytx.controller('BlogPostCtrl', function($scope, $routeParams, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  
  $scope.load_post = function (data) {
    $scope.post = data;
    $scope.set_title(data.title);
  };
  
  $scope.get_post = function () {
    $scope.APIService.get('blog/post/' + $routeParams.slug)
      .success($scope.load_post)
      .error(function () {
        $scope.show_error('Error Loading Blog Post');
      });
  };
  
  $scope.get_post();
});
