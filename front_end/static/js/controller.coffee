angular.module('episodeGet.controllers', [])
  .controller('HomePageCtrl', ($scope, $http) ->
    $http.defaults.headers.post['X-CSRFToken']=$.cookie('csrftoken');
    $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
    $('.home-hero').height $(window).height()-4
    $(window).resize -> $('.home-hero').height $(window).height()-4
    $('.btn-reg-top').click -> $.scrollTo('.login-screen',1000)
    $('.hero-help').click -> $.scrollTo('.feature-intro-word',800)
    $('.feature-item').mouseenter -> $(@).stop().addClass('animated swing')
  )
  .controller('UserCtrl', ($scope, $http, userService)->
    $http.defaults.headers.post['X-CSRFToken']=$.cookie('csrftoken');
    $scope.user = userService.user
    $scope.$on('userService.update', (event, user)-> $scope.user = user )
  )
  .controller('NavCtrl', ($scope, $http, userService)->
    $scope.login =
      username: ''
      password: ''
      status: true
      show: false
      login_id : 'top'
      logined : !!userService.user.id
      showLogin : () -> @.show = !@.show
      isShownLogin : () -> @.show
      isLogined : () ->@.logined
      loginActionStatus: () -> @.status
      loginSubmit: () ->
        $http({method: 'POST', url: '/accounts/login/ajax/', data: $.param({username: @.username, password: @.password})})
          .success((data) ->
              $scope.login.status = !!data.id
              if data.id
                userService.updateUser(data)
                $scope.login.logined = true
                $scope.login.show = false
          )
      checkLogin : () ->
        if not $scope.login.logined
          $http({method: 'GET', url: '/accounts/current/'})
            .success((data)->
              userService.updateUser(data)
              $scope.login.logined = (data.id isnt 0)
            )
            .error((data) ->
              $scope.user = userService.user
              $scope.login.logined = false
            )
    $scope.login.checkLogin()
  )
  .controller('InfoListCtrl', ($scope, $http, $routeParams, infoListService)->
    sort = $routeParams.sort
    $scope.$on('infoListService.update', (event, infoList)-> $scope.currentList = infoList.list[sort] )
    $scope.currentList = infoListService.infoList.list[sort]
    $scope.sortInfo = infoListService.infoList.sortInfo
    $scope.sort = sort
    infoListService.infoList.getList(sort)
  )
  .controller('InfoViewCtrl', ($scope, $http, $routeParams, infoListService)->
    id = $routeParams.id
    sort = $routeParams.sort
    $scope.$on('infoListService.update', (event, infoList)-> $scope.infoList = infoList )
    bigList = infoListService.infoList.list[sort]
    if bigList
      $scope.info = bigList[id]
    else
      $http({method: 'GET', url: '/info/'+id+'/.json'})
        .success((data) =>
          $scope.info = data
        )
  )