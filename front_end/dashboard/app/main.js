var app = angular.module('dashboard_main', []);
app.controller('dashboard_main_controller', ['$scope', function ($scope) {

    $scope.templateURL = 'startup.html';

    $scope.LoadDashboard = function(){
        $scope.templateURL = 'startup.html';
    };

    $scope.AddPapers = function(){
        $scope.templateURL = 'add_paper.html';
    };

}]);
