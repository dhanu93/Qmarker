var app = angular.module('app', []);
app.controller('appCtrl', ['$scope', '$compile', function ($scope, $compile) {

    $scope.templatePage = 'dashboard.html';
    $scope.accountType = 'Teacher';

    $scope.LoadDashboard = function(){
		$scope.templatePage = 'dashboard.html';
    };

}]);
