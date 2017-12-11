var hamsterMod = angular.module('hamster', [
  'ngAnimate',
  'ngCookies', 
  'ngMaterial',
  'ngRoute',
  'ngMessages',
  'hamster.directive.Chart',
  'hamster.directive.TableDiv',
  'hamster.directive.TableShelf',
  'hamster.service.dataService'
  ]);


hamsterMod.config(function($locationProvider, $routeProvider) { 
      $routeProvider
        .when('/project', {
            templateUrl: 'project/project.html',
            controller: ProjectCtrl,
            controllerAs: 'projectCtrl',
            reloadOnSearch: false
        })
        .otherwise({redirectTo: '/project'});
    });