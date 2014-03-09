angular.module('episodeGet.services', [])
  .service('userService', ['$rootScope', '$http',($rootScope, $http) ->
    user:
      id: 0
      last_login: null
      username: "游客"
      email: null
      list: null
      showUsername: () -> @username
    updateUser: (user) ->
      @user = user
      $rootScope.$broadcast('userService.update', @user)
    loginSubmit: (username, password) ->
      $http({method: 'POST', url: '/accounts/login/ajax/', data: $.param({username: username, password: password})})
      .success( (data) =>
          @user = data
          $rootScope.$broadcast('userService.login', @user)
          $rootScope.$broadcast('userService.update', @user)
          )
    regSubmit: (email, username, password) ->
      $http({method: 'POST', url: '/accounts/reg/', data: $.param({email: email, username: username, password: password})})
      .success( (data) =>
          @user = data.user if data.status
          $rootScope.$broadcast('userService.reg', @user, data.status, data.msg)
          $rootScope.$broadcast('userService.update', @user)
          )
    logoutSubmit: ->
      $http({method: 'GET', url: '/accounts/logout/'})
      .success( (data) =>
          @user =
            id: 0
            last_login: null
            username: "游客"
            email: null
            list: null
          $rootScope.$broadcast('userService.logout', @user)
          $rootScope.$broadcast('userService.update', @user)
        )
    listUpdate: ->
      $http({method: 'GET', url: '/sub_list/.json', params:{user: 'me'}})
      .success((data) =>
          @user.list = data.results
          $rootScope.$broadcast('userService.listUpdate', @user)
        )
  ])
  .service('infoListService', ['$rootScope', '$http', ($rootScope, $http)->
      list:
        an: angular.fromJson(localStorage.getItem('infoList_an'))
        ep: angular.fromJson(localStorage.getItem('infoList_ep'))
      getList: (sort) ->
        if not @list[sort]
          $http({method: 'GET', url: '/info/.json', params:{nowplaying: 1, sort: sort}})
            .success((data) =>
              localStorage.setItem('infoList_' + sort, angular.toJson(data.results))
              @list[sort] = data.results
              @updateList(sort ,data.results)
            )
      updateList: (sort ,list) ->
        @list[sort] = list
        $rootScope.$broadcast('infoListService.update', @list)
      sortInfo : (info) ->
        -info.douban.average
  ])
  .service('infoService', ['$rootScope', '$http', 'infoListService', ($rootScope, $http, infoListService) ->
    getInfo:(sort, id)->
      bigInfoList = infoListService.list[sort]
      if bigInfoList
        for info in bigInfoList
          if info.id is parseInt(id, 10)
            break
        return info
      else
        $http({method: 'GET', url: "/info/#{id}/.json"})
          .success((data) =>
            return data
          )
  ])
  .service('tagsListService', ['$rootScope', '$http', ($rootScope, $http)->
    list:
      an: angular.fromJson(localStorage.getItem('tagsList_an'))
      ep: angular.fromJson(localStorage.getItem('tagsList_ep'))
    getList: (sort) ->
      if not @list[sort]
        $http({method: 'GET', url: '/tags/.json', params:{sort: sort}})
          .success((data) =>
            tagListWithIDKey = {}
            for tag in data.results
              tag.tags = angular.fromJson(tag.tags)
              tagListWithIDKey[tag.id] = tag
            localStorage.setItem('tagsList_' + sort, angular.toJson(tagListWithIDKey))
            @list[sort] = tagListWithIDKey
            @updateList(sort ,tagListWithIDKey)
          )
      $rootScope.$broadcast('tagsListService.update', @list, sort)
    updateList: (sort ,list) ->
      @list[sort] = list
      $rootScope.$broadcast('tagsListService.update', @list, sort)
  ])

  .service('subListService', ['$rootScope', '$http', 'tagsListService', ($rootScope, $http, tagsListService)->
    subList: false
    subListTags:
      TM: []
      CL: []
      FM: []
      LG: []
    getList: (sort, info)->
      $http({method: 'GET', url: '/sub_list/.json', params:{info: info}})
        .success((data)=> @calList(data.results))
    calList:(subList=@subList) ->
      @subList = subList
      for list in @subList
        list.show = true
      @subListTags =
        TM: []
        CL: []
        FM: []
        LG: []
      #getSubListTags
      checkExtArray = []
      for subList in @subList
        tagsList = tagsListService.list[angular.lowercase(subList.sort)]
        #get a tags list
        for tagId in subList.tags
          tagId = parseInt(tagId, 10)
          if tagId not in checkExtArray
            checkExtArray.push(tagId)
            for id, tag of tagsList
              if parseInt(tag.id, 10) is tagId
                tag.switch = true
                @subListTags[tag.style].push(tag)
                break
      $rootScope.$broadcast('subListService.update', @subList, @subListTags)

    pickTag: (style, tagId) ->
      for tag in @subListTags[style]
        if tag.id is tagId
          if tag.switch then tag.switch = false else return
      for list in @subList
        if list.show then list.show = parseInt(tagId, 10) in list.tags
      avaliableTags = []
      for list in @subList
        if list.show
          for tag in list.tags
            tag = parseInt(tag, 10)
            if tag not in avaliableTags
              avaliableTags.push(tag)
      for key, tagStyle of @subListTags
        for tag in tagStyle
          if parseInt(tag.id, 10) not in avaliableTags
            tag.switch = false
      $rootScope.$broadcast('subListService.update', @subList, @subListTags)

    filterClean: () ->
      for key, tagStyle of @subListTags
        for tag in tagStyle
            tag.switch = true
      for list in @subList
        list.show = true

    getUserPrefer: ->
      $http({method: 'GET', url: '/accounts/prefer/get/'})
      .success((data)->
          lists = data
          tagsList = tagsListService.list
          result = {an:[], ep:[]}
          if lists isnt 'false'
            for sort, list of lists
              for tagId in list
                result[sort.toLowerCase()].push tagsList[sort.toLowerCase()][tagId]
          $rootScope.$broadcast('preferList.update', result)
        )

    getUserPreferNum: (sort)->
      return angular.fromJson(localStorage.getItem('test_prefer_list'))[sort]
  ])
