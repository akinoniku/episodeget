angular.module('episodeGet', ['ui.bootstrap','ui.sortable', 'episodeGet.controllers', 'episodeGet.services', 'episodeGet.filter'], null)
  .config(['$routeProvider', ($routeProvider) ->
    $routeProvider
      .when('/', {templateUrl: 'static/partials/home_page.html', controller:'HomePageCtrl'})
      .when('/list/:sort', {templateUrl: 'static/partials/info_list.html', controller:'InfoListCtrl'})
      .when('/view/:sort/:id', {templateUrl: 'static/partials/info_view.html', controller:'InfoViewCtrl'})
      .when('/accounts/', {templateUrl: 'static/partials/accounts.html', controller:'UserAccountCtrl'})
      .when('/accounts/prefer/', {templateUrl: 'static/partials/list_prefer.html', controller:'PreferCtrl'})
      .otherwise({redirectTo: '/'})
  ])
  .config(['$compileProvider', ($compileProvider) ->
    $compileProvider.urlSanitizationWhitelist(/^\s*(https?|ftp|mailto|magnet):/)
  ])
  .config(['$httpProvider', ($httpProvider) ->
    $httpProvider.defaults.headers.post['X-CSRFToken']=$.cookie('csrftoken')
    $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded"
  ])
