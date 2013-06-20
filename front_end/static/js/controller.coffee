angular.module('episodeGet.controllers', [])
  .controller('HomePageCtrl', ->
    $('.home-hero').height $(window).height()-4
    $(window).resize -> $('.home-hero').height $(window).height()-4
    $('.btn-reg-top').click -> $.scrollTo('.login-screen',1000)
    $('.hero-help').click -> $.scrollTo('.feature-intro-word',800)
    $('.feature-item').mouseenter -> $(@).stop().addClass('animated swing')
  )

  .controller('NavCtrl', ($scope, $http, userService)->
    $scope.user = userService.user
    $scope.$on('userService.update', (event, user)-> $scope.user = user )
    $scope.login =
      username: ''
      password: ''
      status: true
      show: false
      login_id : 'top'
      logined : !!userService.user.id
      showLogin : () -> @show = !@show
      isShownLogin : () -> @show
      isLogined : () ->@logined
      loginActionStatus: () -> @status
      loginSubmit: () -> $scope.login.status = userService.loginSubmit(@username, @password)
      checkLogin:  ->
        if not $scope.login.logined
          $http({method: 'GET', url: '/accounts/current/'})
            .success((data)->
              userService.updateUser(data)
              $scope.login.logined = (data.id isnt 0)
            )
            .error(->
              $scope.user = userService.user
              $scope.login.logined = false
            )
    $scope.$on('userService.login', (event, user)->
      $scope.user = user
      $scope.login.status = !!user.id
      if user.id
        $scope.login.logined = true
        $scope.login.show = false
    )
    $scope.login.checkLogin()
  )

  .controller('InfoListCtrl', ($scope, $http, $routeParams, infoListService)->
    sort = $routeParams.sort
    $scope.$on('infoListService.update', (event, List)-> $scope.currentList = List[sort] )
    $scope.currentList = infoListService.list[sort]
    $scope.sortInfo = infoListService.sortInfo
    $scope.sort = sort
    $scope.inListView = true;
    infoListService.getList(sort)
  )

  .controller('InfoViewCtrl', ($scope, $http, $routeParams, $location, infoListService, infoService, tagsListService, subListService, userService)->

    [id, sort] = [$routeParams.id, $routeParams.sort]
    # set user
    $scope.user = userService.user
    $scope.$on('userService.update', (event, user)-> $scope.user = user )

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
    $scope.tagClass = -> if @tag.switch then 'tag' else 'tag disabled'
    $scope.pickTag = (style, id) -> subListService.pickTag(style, id)
    $scope.filterClean = -> subListService.filterClean()
    $scope.addListBtn = '添加'

    #add subList for user
    $scope.addSubList = ->
      $http({method: 'POST', url: 'add_list_ajax/', data: $.param(list_id: @list.id)})
        .success(-> $location.path('/accounts'))
        .error(-> $scope.addListBtn = '咦，好像出错了' )
  )

  .controller('UserAccountCtrl', ($scope, $http, userService, $filter)->
    $scope.inAccount = true;
    $scope.user = userService.user
    userService.listUpdate()
    $scope.$on('userService.listUpdate', (event, user)->
      $scope.user = user
      for list in user.list
        list.tagsString = ''
        for tag in list.tags
         list.tagsString += ' '+ $filter('getTagNameById')(tag, list.sort)
    )
    $scope.removeSubList = ->
      $http({method: 'POST', url: 'remove_list_ajax/', data: $.param(list_id: @list.id)})
        .success(-> userService.listUpdate() )
  )
  .controller('PreferCtrl', ($scope, $http, userService, tagsListService)->
    $scope.inAccount = true;
    $scope.user = userService.user
    $scope.tagsList = {}
    resortTag = (tags) ->
      subListTags = {'TM': [], 'CL': [], 'FM': [], 'LG': []}
      for k,tag of tags
        subListTags[tag.style].push(tag)
      subListTags

    for sort in ['an', 'ep']
      $scope.$on('tagsListService.update', (event, list)-> $scope.tagsList[sort] = resortTag(list) )
      tagsListService.getList(sort)
      $scope.tagsList[sort] = resortTag(tagsListService.list[sort])

    # this should be sortable
    # get the tags local storage
    # preview the prefer list in old style
    # render to responce
  )
