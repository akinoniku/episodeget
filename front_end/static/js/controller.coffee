angular.module('episodeGet.controllers', [])
  .controller('HomePageCtrl', ($scope, $http) ->
    $http.defaults.headers.post['X-CSRFToken']=$.cookie('csrftoken');
    $('.home-hero').height $(window).height()-4
    $(window).resize -> $('.home-hero').height $(window).height()-4
    $('.btn-reg-top').click -> $.scrollTo('.login-screen',1000)
    $('.hero-help').click -> $.scrollTo('.feature-intro-word',800)
    $('.feature-item').mouseenter -> $(@).stop().addClass('animated swing')
  )
  .controller('UserCtrl', ($scope, $http)->
    $http.defaults.headers.post['X-CSRFToken']=$.cookie('csrftoken');
    $scope.user =
      id: 0
      last_login: ""
      username: "游客"
      email: ""
    $scope.login =
      login_id : 'top'
      logined : false
    $scope.checkLogin = () ->
      $http({method: 'GET', url: '/accounts/current/'})
        .success((data, status, headers, config)->
          $scope.user=data
          $scope.login.logined = (data.id is not 0)
        )
        .error((data) ->
          $scope.user =
            id: 0
            last_login: ""
            username: "游客"
            email: ""
          $scope.login.logined = false
        )
    $scope.checkLogin()
  )
  .controller('NavCtrl', ($scope)->
    $scope.template={name: 'nav.html', url: 'static/partials/nav.html'}
  )
