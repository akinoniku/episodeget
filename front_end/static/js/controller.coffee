angular.module('episodeGet.controllers', [])
  .controller('HomePageCtrl', ($scope, $http) ->
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
    $http.defaults.headers.post['X-CSRFToken']=$.cookie('csrftoken');
    $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
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
    $scope.$on('infoListService.update', (event, List)-> $scope.currentList = List[sort] )
    $scope.currentList = infoListService.list[sort]
    $scope.sortInfo = infoListService.sortInfo
    $scope.sort = sort
    infoListService.getList(sort)
  )

  .controller('InfoViewCtrl', ($scope, $http, $routeParams, infoListService, infoService, tagsListService, subListService)->
    id = $routeParams.id
    sort = $routeParams.sort

    # # for list information
    $scope.$on('infoListService.update', (event, List)-> $scope.list = List )
    $scope.info = infoService.getInfo(sort, id)

    # tags info
    $scope.$on('tagsListService.update', (event, list)-> $scope.tagsList = list )
    tagsListService.getList(sort)
    $scope.tagsList = tagsListService.list[sort]

    # sublist
    subListService.getList(sort, id)
    $scope.$on('subListService.update', (event, subList, subListTags)->
      $scope.subList = subList
      $scope.subListTags = subListTags
    )

    #tag select
    $scope.tagClass = ()->
      if @tag.switch then 'tag' else 'tag disabled'
    $scope.pickTag = (style, id)->
      subListService.pickTag(style, id)
    $scope.filterClean = ()->
      subListService.filterClean()
  )

  .controller('UserAccountCtrl', ($scope, $http) ->
    $scope.test = 1
  )
