pytx.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      controller:'HomeCtrl',
      templateUrl: tpl('home.html'),
    })
    .when('/sponsors', {
      controller:'SponsorCtrl',
      templateUrl: tpl('sponsors.html'),
      title: 'Our Sponsors'
    })
    .when('/sponsors/prospectus', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Sponsor Prospectus'
    })
    .when('/about', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'About The Conference'
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
    .when('/about/diversity-statement', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Diversity Statement'
    })
    .when('/about/registration', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Registration Info'
    })
    .when('/about/faq', {
      controller: 'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Frequently Asked Questions'
    })
    
    .when('/community/meetups', {
      controller: 'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Local Python Meetups'
    })
    
    .when('/community/employers', {
      controller: 'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Texas Python Employers'
    })
    
    .when('/community/mailing-list', {
      controller: 'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Mailing List'
    })
    
    .when('/venue', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'The Venue'
    })
    .when('/venue/hotels', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Hotels'
    })
    .when('/venue/map', {
      controller:'PageCtrl',
      templateUrl: tpl('page.html'),
      title: 'Map'
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
    .when('/speakers/submit-talk', {
      controller:'SubmitTalkCtrl',
      templateUrl: tpl('speakers/submit-talk.html')
    })
    .when('/talk/:id', {
      controller:'TalkDetailCtrl',
      templateUrl: tpl('speakers/talk-detail.html')
    })
    .when('/videos', {
      controller:'VideosCtrl',
      templateUrl: tpl('speakers/videos.html')
    })
    .when('/schedule', {
      controller:'ScheduleCtrl',
      templateUrl: tpl('speakers/schedule.html')
    })
    
    .when('/user/login', {
      controller:'LoginCtrl',
      templateUrl: tpl('users/login.html')
    })
    .when('/user/my-talks', {
      controller:'TalkListCtrl',
      templateUrl: tpl('users/my-talks.html')
    })
    .when('/user/my-profile', {
      controller:'ProfileCtrl',
      templateUrl: tpl('users/my-profile.html')
    })
    .when('/user/my-avatar', {
      controller:'AvatarCtrl',
      templateUrl: tpl('users/my-avatar.html')
    })
    .when('/user/talk/:id', {
      controller:'EditTalkCtrl',
      templateUrl: tpl('users/edit-talk.html')
    })
    .when('/user/sign-up', {
      controller:'SignUpCtrl',
      templateUrl: tpl('users/sign-up.html')
    })
    .when('/user/reset-password', {
      controller:'ResetCtrl',
      templateUrl: tpl('users/reset-password.html')
    })
    .when('/user/verify', {
      controller:'VerifyCtrl',
      templateUrl: tpl('users/verify.html')
    })
    .when('/user/:username', {
      controller:'UserDetailCtrl',
      templateUrl: tpl('users/user-detail.html')
    })
    
    .when('/blog', {
      controller:'BlogCtrl',
      templateUrl: tpl('blog/index.html')
    })
    .when('/blog/:slug', {
      controller:'BlogPostCtrl',
      templateUrl: tpl('blog/post-detail.html')
    })
    .when('/blog/category/:cat', {
      controller:'BlogCtrl',
      templateUrl: tpl('blog/index.html')
    })
    
    .when('/prizes', {
      controller:'PrizeCtrl',
      templateUrl: tpl('prizes.html')
    })
    
    .otherwise({controller:'ErrorCtrl', templateUrl: tpl('404.html')});
});
