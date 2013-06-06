// Generated by CoffeeScript 2.0.0-beta5
angular.module('episodeGet.services', []).service('userService', [
  '$rootScope',
  function ($rootScope) {
    return {
      user: {
        id: 0,
        last_login: '',
        username: '\u6e38\u5ba2',
        email: '',
        showUsername: function () {
          return this.username;
        }
      },
      updateUser: function (user) {
        this.user = user;
        return $rootScope.$broadcast('userService.update', this.user);
      }
    };
  }
]).service('infoListService', [
  '$rootScope',
  '$http',
  function ($rootScope, $http) {
    return {
      list: {
        an: angular.fromJson(localStorage.getItem('infoList_an')),
        ep: angular.fromJson(localStorage.getItem('infoList_ep'))
      },
      getList: function (sort) {
        var this$;
        if (!this.list[sort])
          return $http({
            method: 'GET',
            url: '/info/.json',
            params: {
              nowplaying: 1,
              sort: sort
            }
          }).success((this$ = this, function (data) {
            localStorage.setItem('infoList_' + sort, angular.toJson(data.results));
            this$.list[sort] = data.results;
            return this$.updateList(sort, data.results);
          }));
      },
      updateList: function (sort, list) {
        this.list[sort] = list;
        return $rootScope.$broadcast('infoListService.update', this.list);
      },
      sortInfo: function (info) {
        return -info.douban.average;
      }
    };
  }
]).service('infoService', [
  '$rootScope',
  '$http',
  'infoListService',
  function ($rootScope, $http, infoListService) {
    return {
      getInfo: function (sort, id) {
        var bigInfoList, info;
        bigInfoList = infoListService.list[sort];
        if (bigInfoList) {
          for (var i$ = 0, length$ = bigInfoList.length; i$ < length$; ++i$) {
            info = bigInfoList[i$];
            if (info.id === parseInt(id, 10))
              break;
          }
          return info;
        } else {
          return $http({
            method: 'GET',
            url: '/info/' + id + '/.json'
          }).success(function (data) {
            return data;
          });
        }
      }
    };
  }
]).service('tagsListService', [
  '$rootScope',
  '$http',
  function ($rootScope, $http) {
    return {
      list: {
        an: angular.fromJson(localStorage.getItem('tagsList_an')),
        ep: angular.fromJson(localStorage.getItem('tagsList_ep'))
      },
      getList: function (sort) {
        var this$;
        if (!this.list[sort])
          return $http({
            method: 'GET',
            url: '/tags/.json',
            params: { sort: sort }
          }).success((this$ = this, function (data) {
            var tag, tagListWithIDKey;
            tagListWithIDKey = {};
            for (var i$ = 0, length$ = data.results.length; i$ < length$; ++i$) {
              tag = data.results[i$];
              tagListWithIDKey[tag.id] = tag;
            }
            localStorage.setItem('tagsList_' + sort, angular.toJson(tagListWithIDKey));
            this$.list[sort] = tagListWithIDKey;
            return this$.updateList(sort, tagListWithIDKey);
          }));
      },
      updateList: function (sort, list) {
        this.list[sort] = list;
        return $rootScope.$broadcast('tagsListService.update', this.list);
      }
    };
  }
]).service('subListService', [
  '$rootScope',
  '$http',
  'tagsListService',
  function ($rootScope, $http, tagsListService) {
    return {
      subList: false,
      subListTags: {
        TM: [],
        CL: [],
        FM: [],
        LG: []
      },
      getList: function (sort, info) {
        var this$;
        return $http({
          method: 'GET',
          url: '/sub_list/.json',
          params: { info: info }
        }).success((this$ = this, function (data) {
          var checkExtArray, id, list, subList, tag, tagId, tagsList;
          this$.subList = data.results;
          for (var i$ = 0, length$ = this$.subList.length; i$ < length$; ++i$) {
            list = this$.subList[i$];
            list.show = true;
          }
          this$.subListTags = {
            TM: [],
            CL: [],
            FM: [],
            LG: []
          };
          tagsList = tagsListService.list[sort];
          checkExtArray = [];
          for (var i$1 = 0, length$1 = this$.subList.length; i$1 < length$1; ++i$1) {
            subList = this$.subList[i$1];
            for (var i$2 = 0, length$2 = subList.tags.length; i$2 < length$2; ++i$2) {
              tagId = subList.tags[i$2];
              tagId = parseInt(tagId, 10);
              if (!in$(tagId, checkExtArray)) {
                checkExtArray.push(tagId);
                for (id in tagsList) {
                  tag = tagsList[id];
                  if (parseInt(tag.id, 10) === tagId) {
                    tag['switch'] = true;
                    this$.subListTags[tag.style].push(tag);
                    break;
                  }
                }
              }
            }
          }
          return $rootScope.$broadcast('subListService.update', this$.subList, this$.subListTags);
        }));
      },
      pickTag: function (style, tagId) {
        var avaliableTags, key, list, tag, tagStyle;
        for (var i$ = 0, length$ = this.subListTags[style].length; i$ < length$; ++i$) {
          tag = this.subListTags[style][i$];
          if (tag.id === tagId)
            if (tag['switch']) {
              tag['switch'] = false;
            } else {
              return;
            }
        }
        for (var i$1 = 0, length$1 = this.subList.length; i$1 < length$1; ++i$1) {
          list = this.subList[i$1];
          if (list.show)
            list.show = in$(parseInt(tagId, 10), list.tags);
        }
        avaliableTags = [];
        for (var i$2 = 0, length$2 = this.subList.length; i$2 < length$2; ++i$2) {
          list = this.subList[i$2];
          if (list.show)
            for (var i$3 = 0, length$3 = list.tags.length; i$3 < length$3; ++i$3) {
              tag = list.tags[i$3];
              tag = parseInt(tag, 10);
              if (!in$(tag, avaliableTags))
                avaliableTags.push(tag);
            }
        }
        for (key in this.subListTags) {
          tagStyle = this.subListTags[key];
          for (var i$4 = 0, length$4 = tagStyle.length; i$4 < length$4; ++i$4) {
            tag = tagStyle[i$4];
            if (!in$(parseInt(tag.id, 10), avaliableTags))
              tag['switch'] = false;
          }
        }
        return $rootScope.$broadcast('subListService.update', this.subList, this.subListTags);
      },
      filterClean: function () {
        var key, tag, tagStyle;
        for (key in this.subListTags) {
          tagStyle = this.subListTags[key];
          for (var i$ = 0, length$ = tagStyle.length; i$ < length$; ++i$) {
            tag = tagStyle[i$];
            tag['switch'] = true;
          }
        }
        return function (accum$) {
          var list;
          for (var i$1 = 0, length$1 = this.subList.length; i$1 < length$1; ++i$1) {
            list = this.subList[i$1];
            accum$.push(list.show = true);
          }
          return accum$;
        }.call(this, []);
      }
    };
  }
]);
function in$(member, list) {
  for (var i = 0, length = list.length; i < length; ++i)
    if (i in list && list[i] === member)
      return true;
  return false;
}
