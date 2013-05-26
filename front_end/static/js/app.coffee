angular.module('episodeGet', ['episodeGet.controllers',])
  .config(['$routeProvider', ($routeProvider) ->
    $routeProvider.when('/home', {templateUrl: 'static/partials/home_page.html', controller:'HomePageCtrl'})
      .otherwise({redirectTo: '/home'})
])
