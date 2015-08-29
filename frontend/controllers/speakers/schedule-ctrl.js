pytx.controller('ScheduleCtrl', function($scope, $routeParams, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  $scope.set_title('Schedule');
  $scope.selectedIndex = 0;
  
  var today = new Date();
  
  $scope.load_schedule = function (data) {
    $scope.schedule = data;
    
    for (var i=0; i < $scope.schedule.length; i++) {
      var day = $scope.schedule[i];
      
      if (day.year == today.getFullYear() && day.month == (today.getMonth() + 1) && day.day == today.getDate()) {
        $scope.selectedIndex = i;
      }
      
      var pc = 50;
      
      if (day.rooms.length == 3) {
        pc = 33;
      }
      
      else if (day.rooms.length == 4) {
        pc = 25;
      }
      
      else if (day.rooms.length == 5) {
        pc = 20;
      }
      
      for (var j=0; j < day.hours.length; j++) {
        var hour = day.hours[j];
        var flexs = [];
        var flex_pc = pc;
        
        for (var f=1; f <= day.rooms.length; f++) {
          flexs.push(f);
        }
        
        for (var room_key in hour) {
          var r = hour[room_key];
          
          if (room_key == 'all') {
            r.flex_order = '';
            flex_pc = 100;
            flexs = [];
          }
          
          else {
            r.flex_order = day.rooms.indexOf(room_key) + 1;
            
            if (flexs.indexOf(r.flex_order) > -1) {
              flexs.splice(flexs.indexOf(r.flex_order), 1);
            }
          }
        }
        
        if (flexs.length > 0) {
          flex_pc = pc;
        }
        
        var h = {flexs: flexs, rooms: hour, flex_pc: flex_pc};
        day.hours[j] = h;
      }
    }
  };
  
  $scope.get_schedule = function () {
    $scope.APIService.get('speakers/schedule')
      .success($scope.load_schedule)
      .error(function () {
        $scope.show_error('Error Loading Schedule');
      });
  };
  
  $scope.get_schedule();
});
