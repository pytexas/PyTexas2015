pytx.controller('PrizeCtrl', function($scope, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  
  $scope.get_attendees = function () {
    $scope.APIService.get('conferences/attendees')
      .success($scope.load_attendees)
      .error(function () {
        $scope.show_error('Error Loading Attendees');
      });
  };
  
  $scope.load_attendees = function (data) {
    $scope.attendees = data;
  };
  
  $scope.used = [];
  
  $scope.find_winner = function () {
    var max = $scope.attendees.length * 100;
    var choice;
    
    for (var i=0; i < max; i++) {
      choice = $scope.attendees[randomIndex()];
      
      if ($scope.used.indexOf(choice) == -1) {
        $scope.used.push(choice);
        return null;
      }
    }
    
    alert("No Winner Found");
  }
  
  function randomIndex () {
    return Math.floor($scope.attendees.length * Math.random());
  }
  
  $scope.get_attendees();
});
