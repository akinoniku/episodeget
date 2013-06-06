angular.module('episodeGet.services', [])
  .service('userService', ['$rootScope',($rootScope) ->
    user:
      id: 0
      last_login: ""
      username: "游客"
      email: ""
      showUsername: () -> @username
    updateUser: (user) ->
      @user = user
      $rootScope.$broadcast('userService.update', @user)
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
              tagListWithIDKey[tag.id] = tag
            localStorage.setItem('tagsList_' + sort, angular.toJson(tagListWithIDKey))
            @list[sort] = tagListWithIDKey
            @updateList(sort ,tagListWithIDKey)
          )
    updateList: (sort ,list) ->
      @list[sort] = list
      $rootScope.$broadcast('tagsListService.update', @list)
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
        .success((data)=>
          @subList = data.results
          for list in @subList
            list.show = true
          @subListTags =
            TM: []
            CL: []
            FM: []
            LG: []
          #getSubListTags
          tagsList = tagsListService.list[sort]
          checkExtArray = []
          for subList in @subList
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
        )
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
  ])