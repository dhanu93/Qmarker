var app = angular.module('app', []);
app.controller('appCtrl', ['$scope', '$http', function ($scope, $http) {

    $scope.loading = false;

    $scope.addQuestions = function (data) {
        $scope.loading = true;
        $http.post("http://127.0.0.1:8000/add_questions/",data)
            .then(function (result) {
                $scope.loading = false;
                alert("Question added successfully.");
                $scope.data = {};
            });
    };

    $scope.dummyload = function (data) {
        $scope.data = {};
        $scope.data.question = "Where do pandas live?";
        $scope.data.answer = "Pandas live in China.";
        $scope.data.mark = "6";
    };

}]);
