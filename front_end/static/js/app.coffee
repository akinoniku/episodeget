angular.module('episodeGet', ['episodeGet.controllers', 'episodeGet.services', 'episodeGet.filter'], null)
  .config(['$routeProvider', ($routeProvider) ->
    $routeProvider
      .when('/', {templateUrl: 'static/partials/home_page.html', controller:'HomePageCtrl'})
      .when('/list/:sort', {templateUrl: 'static/partials/info_list.html', controller:'InfoListCtrl'})
      .when('/view/:sort/:id', {templateUrl: 'static/partials/info_view.html', controller:'InfoViewCtrl'})
      .otherwise({redirectTo: '/'})
])