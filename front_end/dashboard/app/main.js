var app = angular.module('dashboard_main', []);
app.controller('dashboard_main_controller', ['$scope', function ($scope) {

    //$scope.templateURL = 'teacher_dashboard.html';
    $scope.templateURL = 'select_category.html';

    $scope.LoadDashboard = function(){
        $scope.templateURL = 'startup.html';
    };

    $scope.AddPapers = function(){
        $scope.templateURL = 'add_questions.html';
    };

    //nikan

}]);
