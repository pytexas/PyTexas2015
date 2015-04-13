function tpl (path) {
  return CONFIG.dir + 'templates/' + path;
}

function img_path (path) {
  return CONFIG.dir + 'img/' + path;
}

var pytx = angular.module('pytx',
  ['ngAnimate', 'ngMaterial', 'ngRoute', 'ngSanitize', 'ngCookies', 'hc.marked']
);

pytx.config(function ($routeProvider, $locationProvider, $httpProvider, markedProvider) {
  $locationProvider.html5Mode(true);
  
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  
  $routeProvider
    .when('/', {
      controller:'HomeCtrl',
      templateUrl: tpl('home.html'),
    })
    .when('/sponsors', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Our Sponsors'
    })
    .when('/sponsors/prospectus', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Sponsor Prospectus'
    })
    .when('/about/privacy-policy', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Privacy Policy'
    })
    .when('/about/code-of-conduct', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Code of Conduct'
    })
    .when('/speakers/call-for-proposals', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Call for Proposals'
    })
    .when('/speakers/proposals', {
      controller:'ProposedTalksCtrl',
      templateUrl: tpl('speakers/proposed-talks.html'),
      title: 'Proposed Talks'
    })
    
    .otherwise({controller:'ErrorCtrl', templateUrl: tpl('404.html')});
    
  markedProvider.setOptions({gfm: false});
});

pytx.run(function ($rootScope, $mdSidenav, $mdDialog) {
  $rootScope.tpl = tpl;
  $rootScope.img_path = img_path;
  $rootScope.title = 'PyTexas ' + CONFIG.conf;
  $rootScope.conf = CONFIG.conf;
  
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
  
  $rootScope.close_side = function () {
    $mdSidenav('leftnav').close();
  };
  
  $rootScope.show_error = function (error) {
    var alert = $mdDialog.alert()
      .title('Error Encountered!')
      .content(error)
      .ok('Close');
      
    $mdDialog.show(alert);
  };
  
  $rootScope.$on('$locationChangeStart', function (event) {
    $rootScope.close_side();
  });
  
  $rootScope.menu = [
    ['Sponsors', [
      {title: 'Become A Sponsor', url: 'sponsors/prospectus'},
      {title: 'Our Sponsors', url: 'sponsors'},
    ]],
    ['Speakers', [
      {title: 'Call For Proposals', url: 'speakers/call-for-proposals'},
      {title: 'Proposed Talks', url: 'speakers/proposals'},
    ]],
    ['About', [
      {title: 'Privacy Policy', url: 'about/privacy-policy'},
      {title: 'Code of Conduct', url: 'about/code-of-conduct'},
    ]]
  ];
});
