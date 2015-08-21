pytx.controller('PageCtrl', function($scope, $route, marked, $http) {
  $scope.set_title($route.current.$$route.title);
  
  $scope.page_url = CONFIG.dir + 'pages' + $route.current.$$route.originalPath + '.md';
  $scope.page_source = '';
  
  $http.get($scope.page_url)
    .success(function (data) {
      data = data.replace(/\(img\/(.*?)\)/g, "(" + CONFIG.dir + "img/$1)");
      $scope.page_source = data;
    });
});
