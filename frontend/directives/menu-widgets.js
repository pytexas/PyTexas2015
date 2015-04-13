pytx.directive('menuCollapse', function () {
  return {
    templateUrl: tpl('widgets/menu-collapse.html'),
    scope: {title: '=', items: '=', conf: '='},
    controller: function ($scope, $rootScope) {
      $scope.style = {height: 0};
      $scope.open = false;
      
      $scope.toggle_collapse = function () {
        if ($scope.style.height === 0) {
          var ul = $scope.element.children()[0].children[1].children[0];
          $scope.style.height = ul.clientHeight + 'px';
          $scope.open = true;
        }
        
        else {
          $scope.style.height = 0;
          $scope.open = false;
        }
      };
    },
    
    link: function(scope, element, attrs) {
      scope.element = element;
    }
  };
});
