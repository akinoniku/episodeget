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
    infoList:
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