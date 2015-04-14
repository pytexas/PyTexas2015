pytx.controller('VerifyCtrl', function($scope, $location, APIFactory) {
  $scope.APIService = new APIFactory('v1');
  $scope.set_title('E-Mail Verification');
  $scope.message = null;
  
  $scope.error = function () {
    $scope.message = 'Invalid verification key provided.';
  };
  
  $scope.success = function () {
    $scope.message = 'Your E-Mail has been successfully validated';
  };
  
  var searchObject = $location.search();
  if (searchObject.secret) {
    $scope.APIService.post('users/verify', {secret: searchObject.secret})
      .success($scope.success)
      .error($scope.error);
  }
  
  else {
    $scope.message = 'No verification key provided.';
  }
});
