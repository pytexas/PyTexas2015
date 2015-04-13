function tpl (path) {
  return CONFIG.dir + 'templates/' + path;
}

function img_path (path) {
  return CONFIG.dir + 'img/' + path;
}

var pytx = angular.module('pytx',
  ['ngAnimate', 'ngMaterial', 'ngRoute', 'ngSanitize', 'ngCookies', 'hc.marked', 'angularMoment']
);

pytx.config(function ($locationProvider, $httpProvider, markedProvider) {
  $locationProvider.html5Mode(true);
  
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  
  markedProvider.setOptions({gfm: false, sanitize: true});
});

pytx.run(function ($rootScope, $location, $mdSidenav, $mdDialog, $cookies, $mdToast, APIFactory) {
  $rootScope.tpl = tpl;
  $rootScope.img_path = img_path;
  $rootScope.title = 'PyTexas ' + CONFIG.conf;
  $rootScope.conf = CONFIG.conf;
  $rootScope.logged_in = false;
  if ($cookies.sessionid && $cookies.angular_logged_in) {
    $rootScope.logged_in = true;
  }
  
  $rootScope.url = function () {
    var u = $location.url();
    if (u.indexOf('/login') > -1) {
      u = '/';
    }
    
    return encodeURIComponent(u);
  };
  
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
  
  $rootScope.logout = function () {
    var APIService = new APIFactory('v1');
    APIService.post('users/logout')
      .success(function () {
        $rootScope.logged_in = false;
        $mdToast.show(
          $mdToast.simple()
            .content('Logout Successful')
            .position('bottom left')
            .hideDelay(5000)
        );
        
        $location.path('/');
      })
      .error(function () {
        $rootScope.show_error('Error logging out.');
      });
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

pytx.constant('angularMomentConfig', {
  timezone: 'America/Chicago'
});
