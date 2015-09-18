function tpl (path) {
  return CONFIG.dir + 'templates/' + path;
}

function img_path (path) {
  return CONFIG.dir + 'img/' + path;
}

var pytx = angular.module('pytx',
  [
    'ngAnimate', 'ngMaterial', 'ngRoute', 'ngSanitize', 'hc.marked',
    'angularMoment', 'angulartics', 'angulartics.google.analytics', 'angular-jwt'
  ]
);

pytx.config(function ($locationProvider, $httpProvider, markedProvider, jwtInterceptorProvider) {
  $locationProvider.html5Mode(true);
  
  markedProvider.setOptions({gfm: false, sanitize: true});
  
  jwtInterceptorProvider.authPrefix = 'JWT ';
  jwtInterceptorProvider.tokenGetter = function (StorageService, jwtHelper) {
    var token = StorageService.get('pytx_jwt');
    if (token) {
      if (jwtHelper.isTokenExpired(token)) {
        return undefined;
      }
      
      else {
        return token;
      }
    }
    
    return undefined;
  };
  
  $httpProvider.interceptors.push('jwtInterceptor');
});

pytx.run(function ($rootScope, $location, $mdSidenav, $mdDialog, $mdToast, $timeout, APIFactory, StorageService, jwtHelper) {
  $rootScope.tpl = tpl;
  $rootScope.img_path = img_path;
  $rootScope.title = 'PyTexas ' + CONFIG.conf;
  $rootScope.conf = CONFIG.conf;
  $rootScope.logged_in = false;
  
  var token = StorageService.get('pytx_jwt');
  if (token) {
    if (jwtHelper.isTokenExpired(token)) {
      StorageService.remove('pytx_jwt');
    }
    
    else {
      $rootScope.logged_in = true;
    }
  }
  
  $rootScope.conf_data = function () {
    var APIService = new APIFactory('v1');
    APIService.get('conferences/data').success(function (data) {
      $rootScope.conf_obj = data;
    });
    
    APIService.get('conferences/sponsors').success(function (data) {
      $rootScope.sponsor_levels = data;
    });
  };
  
  $rootScope.conf_data();
  
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
    StorageService.remove('pytx_jwt');
    
    $rootScope.logged_in = false;
    $mdToast.show(
      $mdToast.simple()
        .content('Logout Successful')
        .position('bottom left')
        .hideDelay(5000)
    );
    
    $location.path('/');
  };
  
  $rootScope.show_error = function (error) {
    var alert = $mdDialog.alert()
      .title('Error Encountered!')
      .content(error)
      .ok('Close');
      
    $mdDialog.show(alert);
  };
  
  $rootScope.$on('$locationChangeSuccess', function (event) {
    $rootScope.close_side();
    $timeout(function () {
      var element = document.querySelector("#main-content");
      element.scrollTop = 0;
    }, 10);
  });
  
  $rootScope.menu = [
    ['Sponsors', [
      {title: 'Become A Sponsor', url: 'sponsors/prospectus'},
      {title: 'Our Sponsors', url: 'sponsors'},
    ]],
    ['Schedule', {url: 'schedule'}],
    /*['Speakers', [
      {title: 'Call For Proposals', url: 'speakers/call-for-proposals'},
      {title: 'Submit A Talk', url: 'speakers/submit-talk'},
      {title: 'Proposed Talks', url: 'speakers/proposals'},
    ]],*/
    ['Venue', [
      {title: 'The Venue', url: 'venue'},
      {title: 'Hotels', url: 'venue/hotels'},
      {title: 'Map & Parking', url: 'venue/map'},
    ]],
    ['About', [
      {title: 'About The Conference', url: 'about'},
      {title: 'Register', url: 'about/registration'},
      {title: 'Privacy Policy', url: 'about/privacy-policy'},
      {title: 'Code of Conduct', url: 'about/code-of-conduct'},
      {title: 'Diversity Statement', url: 'about/diversity-statement'},
      {title: 'Frequently Asked Questions', url: 'about/faq'}
    ]],
    ['Community', [
      {title: 'Chat Room', fullurl: 'https://gitter.im/pytexas/PyTexas'},
      {title: 'Mailing List', url: 'community/mailing-list'},
      {title: 'Local Python Meetups', url: 'community/meetups'},
      {title: 'Python Employers', url: 'community/employers'}
    ]],
    ['Blog', {url: 'blog'}],
    ['My Account', [
      {title: 'My Talks', url: 'user/my-talks'},
      {title: 'Profile', url: 'user/my-profile'},
      {title: 'Profile Image', url: 'user/my-avatar'}
    ]]
  ];
});

pytx.constant('angularMomentConfig', {
  timezone: 'America/Chicago'
});

pytx.filter('thumbnail', function() {
  return function (img_url, transforms) {
    if (img_url) {
      img_url = 'https://pytexas.imgix.net' + img_url;
      
      if (transforms) {
        img_url += '?' + transforms;
      }
    }
    
    return img_url;
  };
});

