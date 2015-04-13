pytx.config(function ($routeProvider) {
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
      templateUrl: tpl('speakers/proposed-talks.html')
    })
    .when('/talk/:id', {
      controller:'TalkDetailCtrl',
      templateUrl: tpl('speakers/talk-detail.html')
    })
    
    .when('/user/login', {
      controller:'LoginCtrl',
      templateUrl: tpl('users/login.html')
    })
    .when('/user/:username', {
      controller:'UserDetailCtrl',
      templateUrl: tpl('users/user-detail.html')
    })
    
    .otherwise({controller:'ErrorCtrl', templateUrl: tpl('404.html')});
});
