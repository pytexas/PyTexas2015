function tpl (path) {
  return CONFIG.dir + 'templates/' + path;
}

function img_path (path) {
  return CONFIG.dir + '/img/' + path;
}

var pytx = angular.module('pytx',
  ['ngAnimate', 'ngMaterial', 'ngRoute', 'ngSanitize', 'ngCookies']
);

pytx.config(function ($routeProvider, $locationProvider, $httpProvider) {
  $locationProvider.html5Mode(true);
  
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  
  $routeProvider
    .when('/', {
      controller:'HomeCtrl',
      templateUrl: tpl('home.html'),
    })
      
    .otherwise({controller:'ErrorCtrl', templateUrl: tpl('404.html')});
});

pytx.run(function ($rootScope, $mdSidenav, $mdDialog) {
  $rootScope.tpl = tpl;
  $rootScope.img_path = img_path;
  $rootScope.title = 'PyTexas ' + CONFIG.conf;
  
  $rootScope.set_title = function (t) {
    $rootScope.title = '';
    
    if (t) {
      $rootScope.title = t + ' | ';
    }
    
    $rootScope.title += 'PyTexas ' + CONFIG.conf;
  };
  
  $rootScope.toggle_side = function () {
    $mdSidenav('leftnav').toggle();
  };
});
