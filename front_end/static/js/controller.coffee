angular.module('episodeGet.controllers', [])
  .controller('HomePageCtrl', ->
    $('.home-hero').height $(window).height()-4
    $(window).resize -> $('.home-hero').height $(window).height()-4
    $('.feature-item').mouseenter -> $(@).stop().addClass('animated swing')
    $('.btn-reg-top').click -> $.scrollTo('.login-screen',1000)
    $('.hero-help').click -> $.scrollTo('.feature-intro-word',800)
  )

  .controller('NavCtrl', ($scope,$location, $http, userService)->
    now = Date.parse(new Date())
    if localStorage.getItem('info_timeout')? and now - localStorage.getItem('info_timeout') > 259200000
      localStorage.removeItem('infoList_an')
      localStorage.removeItem('infoList_ep')

    if localStorage.getItem('tags_timeout')? and now - localStorage.getItem('tags_timeout') > 259200000
      localStorage.removeItem('tagsList_an')
      localStorage.removeItem('tagsList_ep')

    $scope.$on('infoListService.update', (event, List)->
      localStorage.setItem('info_timeout', now)
    )
    $scope.$on('tagsListService.update', (event, list)->
      localStorage.setItem('tags_timeout', now)
    )

    $scope.login =
      email:''
      username: ''
      password: ''
      status: false # login status
      show: false # login form shown
      show_reg: false
      msg: ''
      login_id : 'top'
      logined : !!userService.user.id
      loginSubmit: -> userService.loginSubmit(@username, @password)
      regSubmit: -> userService.regSubmit(@email ,@username, @password)
      logout: -> userService.logoutSubmit()
      checkLogin:  ->
        if not $scope.login.logined
          $http({method: 'GET', url: '/accounts/current/'})
            .success((data)->
              if data
                userService.updateUser(data)
                $scope.login.logined = (data.id isnt 0 and data.id?)
              else
                $scope.user = userService.user
                $scope.login.logined = false
            )
    $scope.$on('userService.login', (event, user)->
      $scope.user = user
      $scope.login.status = !user.id
      if user.id isnt 0
        $scope.login.logined = true
        $scope.login.show = false
        $scope.login.show_reg = false
        if $location.path() is '/'
          $location.path('/accounts/')
    )

    $scope.user = userService.user
    $scope.$on('userService.update', (event, user)-> $scope.user = user )

    $scope.$on('userService.reg', (event, user, status, msg)->
      $scope.user = user
      $scope.login.status = status
      $scope.login.msg = ''
      if status
        $scope.login.logined = true
        $scope.login.show = false
        $scope.login.show_reg = false
        if $location.path() is '/'
          $location.path('/accounts/prefer')
      else
        $scope.login.msg = msg
    )

    $scope.$on('userService.logout', (event, user)->
      $scope.user = user
      $scope.login.status = !!user.id
      if not user.id
        $scope.login.logined = false
        $scope.login.show = false
    )

    $scope.tab = ->
      if $location.path().indexOf('an') isnt -1
        return 'an'
      else if $location.path().indexOf('ep') isnt -1
        return 'ep'
      else if $location.path().indexOf('accounts') isnt -1
        return 'accounts'

    $scope.login.checkLogin()
  )

  .controller('InfoListCtrl', ($scope, $http, $routeParams, infoListService)->
    sort = $routeParams.sort
    $scope.sort = sort
    $scope.page = if $routeParams.page then $routeParams.page else 1
    $scope.sort = sort
    infoListService.getList(sort)
    $scope.createPage = (list, sort, page) ->
      $scope.currentList = list[sort]
      if not $scope.currentList?
        return false
      totalPage = parseInt($scope.currentList.length/8)
      $scope.pages = [1..totalPage]
      $scope.previewPage = if parseInt($scope.page) is 1 then 1 else page-1
      $scope.nextPage = if parseInt($scope.page) is totalPage then parseInt($scope.page) else parseInt($scope.page)+1
      startItem = if 0 < parseInt(page) <= totalPage then (page - 1) * 8 else 0
      endItem = if parseInt(page) > totalPage then false else startItem + 7
      if endItem
        $scope.currentPage = list[sort][startItem..endItem]
      else
        $scope.currentPage = list[sort][startItem..]

    $scope.$on('infoListService.update', (event, List)->
      $scope.createPage(List, sort, $scope.page)
    )

    $scope.sortInfo = infoListService.sortInfo
    $scope.inListView = true;
    $scope.createPage(infoListService.list, sort, $scope.page)
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
    $scope.addSubList = (id)->
      $http({method: 'POST', url: 'add_list_ajax/', data: $.param(list_id: id)})
        .success(-> $location.path('/accounts'))
        .error(-> $scope.addListBtn = '咦，好像出错了' )

    $scope.calOneClick = ->
      $http({method: 'POST', url: 'add_list_one_click/', data: $.param(infoId: id)})
      .success(-> $location.path('/accounts'))
  )

  .controller('UserAccountCtrl', ($scope, $location, $http, userService, $filter, tagsListService)->
    $scope.inAccount = true;
    $scope.user = userService.user
    userService.listUpdate()
    $scope.$on('userService.listUpdate', (event, user)->
      $scope.user = user
      $scope.feedUrl = "http://episodeget.sinaapp.com/feed/#{$scope.user.username}.rss"
      for list in user.list
        list.tagsString = ''
        for tag in list.tags
         list.tagsString += ' '+ $filter('getTagNameById')(tag, list.sort)
    )
    $scope.removeSubList = ->
      $http({method: 'POST', url: 'remove_list_ajax/', data: $.param(list_id: @list.id)})
        .success(-> userService.listUpdate() )

    for sort in ['an', 'ep']
      tagsListService.getList(sort)

    $scope.$on('tagsListService.update', (event, list, sort)->
      $scope.tagsList[sort] = resortTag(list[sort])
      $scope.unsortTags[sort] = list[sort]
    )
  )

  .controller('PreferCtrl', ($scope, $location, $http, userService, tagsListService, subListService)->
    $scope.inAccount = true
    $scope.sort= 'an'
    $scope.user = userService.user
    $scope.tagsList = {}
    $scope.unsortTags = {}
    $scope.userPrefer = angular.fromJson('{"AN":[128,10,15,13,50,11,14,41,51,123,126,133],"EP":[170,844,186]}')
    $scope.searchInput = ''

    $scope.selectExample = (listType)->
      preferExample =
        normal: '{"AN":[128,10,15,13,50,11,14,41,51,123,126,133],"EP":[170,844,186]}'
        clear: '{"AN":[128,10,15,13,50,11,14,41,51,124,129],"EP":[170,844,184]}'
        learner: '{"AN":[138,128,129],"EP":[181,183]}'
      $http({method: 'POST', url: '/accounts/prefer/save/', data: $.param({list:preferExample[listType]})})
      .success(-> $location.path('/accounts'))


    # cal init data
    resortTag = (tags) ->
      preSubListTags = {'TM': [], 'CL': [], 'FM': [], 'LG': []}
      preSubListTags[tag.style].push(tag) for k,tag of tags
      subListTags = []
      subListTags.push tags for k,tags of preSubListTags
      subListTags

    $scope.$on('tagsListService.update', (event, list, sort)->
      $scope.tagsList[sort] = resortTag(list[sort])
      $scope.unsortTags[sort] = list[sort]

      subListService.getUserPrefer()
    )

    for sort in ['an', 'ep']
      tagsListService.getList(sort)

    $scope.$on('preferList.update', (event, result)->
      $scope.userPrefer = result
    )

    $scope.searchTags = (sort, input) ->
      return false if not input
      tags = []
      for key,tag of $scope.unsortTags[sort]
        tags.push(tag) if tag.tags.toString().indexOf(input) isnt -1
      tags

    $scope.addTag = (tag) ->
      $scope.userPrefer[$scope.sort].push tag if tag not in $scope.userPrefer
      $scope.searchInput = ''

    $scope.removeTag = (key) -> $scope.userPrefer[$scope.sort].splice(key,1)

    $scope.savePrefer = ->
      list = {AN: [], EP: []}
      for sort in ['AN', 'EP']
        list[sort].push tag.id for tag in $scope.userPrefer[sort.toLowerCase()]
        localStorage.setItem('test_prefer_list', angular.toJson(list))
      $http({method: 'POST', url: '/accounts/prefer/save/', data: $.param({list: angular.toJson(list)})})
      .success(-> $location.path('/accounts'))

    $scope.getSortClass = (sort)->
       if $scope.sort is sort then 'btn btn-primary active' else 'btn btn-primary'
  )
