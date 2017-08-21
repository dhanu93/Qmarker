var app = angular.module('dashboard_main', []);
app.controller('dashboard_main_controller', ['$scope', '$compile', function ($scope, $compile) {

    //$scope.templateURL = 'teacher_dashboard.html';
    $scope.templateURL = 'add_questions.html';

    $scope.newly_added_question_remover = false;

    $scope.LoadDashboard = function(){
    	$scope.templateURL = 'startup.html';
    };

    $scope.AddPapers = function(){
    	$scope.templateURL = 'add_questions.html';
    };

    $scope.AddAnotherQuestionForm = function(){

    	if(!$scope.newly_added_question_remover){
    		$scope.newly_added_question_remover = true;
    	}

    	var myElements = angular.element(document.querySelector('#form-holder'));    	
    	var html = angular.element(myElements[0].children[0]).clone();
    	console.log(myElements);
    	angular.element(myElements[0].children[myElements[0].children.length - 2]).after(html);
    	$compile(html)($scope);
    }

    $scope.RemoveAddedQuestion = function(eve){
    	var myElements = angular.element(eve.currentTarget);
    	var parent = angular.element(myElements.parent())
    	
    	console.log(parent.length);

    	if(parent.length <= 2){
    		$scope.newly_added_question_remover = false;
    	}

    	parent.remove();
    	$compile(parent);   	
    }
}]);