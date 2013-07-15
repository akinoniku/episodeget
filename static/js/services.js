// Generated by CoffeeScript 1.6.2
(function() {
  var __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  angular.module('episodeGet.services', []).service('userService', [
    '$rootScope', '$http', function($rootScope, $http) {
      return {
        user: {
          id: 0,
          last_login: null,
          username: "游客",
          email: null,
          list: null,
          showUsername: function() {
            return this.username;
          }
        },
        updateUser: function(user) {
          this.user = user;
          return $rootScope.$broadcast('userService.update', this.user);
        },
        loginSubmit: function(username, password) {
          var _this = this;

          return $http({
            method: 'POST',
            url: '/accounts/login/ajax/',
            data: $.param({
              username: username,
              password: password
            })
          }).success(function(data) {
            _this.user = data;
            $rootScope.$broadcast('userService.login', _this.user);
            return $rootScope.$broadcast('userService.update', _this.user);
          });
        },
        regSubmit: function(email, username, password) {
          var _this = this;

          return $http({
            method: 'POST',
            url: '/accounts/reg/',
            data: $.param({
              email: email,
              username: username,
              password: password
            })
          }).success(function(data) {
            if (data.status) {
              _this.user = data.user;
            }
            $rootScope.$broadcast('userService.reg', _this.user, data.status, data.msg);
            return $rootScope.$broadcast('userService.update', _this.user);
          });
        },
        logoutSubmit: function() {
          var _this = this;

          return $http({
            method: 'GET',
            url: '/accounts/logout/'
          }).success(function(data) {
            _this.user = {
              id: 0,
              last_login: null,
              username: "游客",
              email: null,
              list: null
            };
            $rootScope.$broadcast('userService.logout', _this.user);
            return $rootScope.$broadcast('userService.update', _this.user);
          });
        },
        listUpdate: function() {
          var _this = this;

          return $http({
            method: 'GET',
            url: '/sub_list/.json',
            params: {
              user: 'me'
            }
          }).success(function(data) {
            _this.user.list = data.results;
            return $rootScope.$broadcast('userService.listUpdate', _this.user);
          });
        }
      };
    }
  ]).service('infoListService', [
    '$rootScope', '$http', function($rootScope, $http) {
      return {
        list: {
          an: angular.fromJson(localStorage.getItem('infoList_an')),
          ep: angular.fromJson(localStorage.getItem('infoList_ep'))
        },
        getList: function(sort) {
          var _this = this;

          if (!this.list[sort]) {
            return $http({
              method: 'GET',
              url: '/info/.json',
              params: {
                nowplaying: 1,
                sort: sort
              }
            }).success(function(data) {
              localStorage.setItem('infoList_' + sort, angular.toJson(data.results));
              _this.list[sort] = data.results;
              return _this.updateList(sort, data.results);
            });
          }
        },
        updateList: function(sort, list) {
          this.list[sort] = list;
          return $rootScope.$broadcast('infoListService.update', this.list);
        },
        sortInfo: function(info) {
          return -info.douban.average;
        }
      };
    }
  ]).service('infoService', [
    '$rootScope', '$http', 'infoListService', function($rootScope, $http, infoListService) {
      return {
        getInfo: function(sort, id) {
          var bigInfoList, info, _i, _len,
            _this = this;

          bigInfoList = infoListService.list[sort];
          if (bigInfoList) {
            for (_i = 0, _len = bigInfoList.length; _i < _len; _i++) {
              info = bigInfoList[_i];
              if (info.id === parseInt(id, 10)) {
                break;
              }
            }
            return info;
          } else {
            return $http({
              method: 'GET',
              url: "/info/" + id + "/.json"
            }).success(function(data) {
              return data;
            });
          }
        }
      };
    }
  ]).service('tagsListService', [
    '$rootScope', '$http', function($rootScope, $http) {
      return {
        list: {
          an: angular.fromJson(localStorage.getItem('tagsList_an')),
          ep: angular.fromJson(localStorage.getItem('tagsList_ep'))
        },
        getList: function(sort) {
          var _this = this;

          if (!this.list[sort]) {
            $http({
              method: 'GET',
              url: '/tags/.json',
              params: {
                sort: sort
              }
            }).success(function(data) {
              var tag, tagListWithIDKey, _i, _len, _ref;

              tagListWithIDKey = {};
              _ref = data.results;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                tag = _ref[_i];
                tag.tags = angular.fromJson(tag.tags);
                tagListWithIDKey[tag.id] = tag;
              }
              localStorage.setItem('tagsList_' + sort, angular.toJson(tagListWithIDKey));
              _this.list[sort] = tagListWithIDKey;
              return _this.updateList(sort, tagListWithIDKey);
            });
          }
          return $rootScope.$broadcast('tagsListService.update', this.list, sort);
        },
        updateList: function(sort, list) {
          this.list[sort] = list;
          return $rootScope.$broadcast('tagsListService.update', this.list, sort);
        }
      };
    }
  ]).service('subListService', [
    '$rootScope', '$http', 'tagsListService', function($rootScope, $http, tagsListService) {
      return {
        subList: false,
        subListTags: {
          TM: [],
          CL: [],
          FM: [],
          LG: []
        },
        getList: function(sort, info) {
          var _this = this;

          return $http({
            method: 'GET',
            url: '/sub_list/.json',
            params: {
              info: info
            }
          }).success(function(data) {
            return _this.calList(data.results);
          });
        },
        calList: function(subList) {
          var checkExtArray, id, list, tag, tagId, tagsList, _i, _j, _k, _len, _len1, _len2, _ref, _ref1, _ref2;

          if (subList == null) {
            subList = this.subList;
          }
          this.subList = subList;
          _ref = this.subList;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            list = _ref[_i];
            list.show = true;
          }
          this.subListTags = {
            TM: [],
            CL: [],
            FM: [],
            LG: []
          };
          checkExtArray = [];
          _ref1 = this.subList;
          for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
            subList = _ref1[_j];
            tagsList = tagsListService.list[angular.lowercase(subList.sort)];
            _ref2 = subList.tags;
            for (_k = 0, _len2 = _ref2.length; _k < _len2; _k++) {
              tagId = _ref2[_k];
              tagId = parseInt(tagId, 10);
              if (__indexOf.call(checkExtArray, tagId) < 0) {
                checkExtArray.push(tagId);
                for (id in tagsList) {
                  tag = tagsList[id];
                  if (parseInt(tag.id, 10) === tagId) {
                    tag["switch"] = true;
                    this.subListTags[tag.style].push(tag);
                    break;
                  }
                }
              }
            }
          }
          return $rootScope.$broadcast('subListService.update', this.subList, this.subListTags);
        },
        pickTag: function(style, tagId) {
          var avaliableTags, key, list, tag, tagStyle, _i, _j, _k, _l, _len, _len1, _len2, _len3, _len4, _m, _ref, _ref1, _ref2, _ref3, _ref4, _ref5, _ref6;

          _ref = this.subListTags[style];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            tag = _ref[_i];
            if (tag.id === tagId) {
              if (tag["switch"]) {
                tag["switch"] = false;
              } else {
                return;
              }
            }
          }
          _ref1 = this.subList;
          for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
            list = _ref1[_j];
            if (list.show) {
              list.show = (_ref2 = parseInt(tagId, 10), __indexOf.call(list.tags, _ref2) >= 0);
            }
          }
          avaliableTags = [];
          _ref3 = this.subList;
          for (_k = 0, _len2 = _ref3.length; _k < _len2; _k++) {
            list = _ref3[_k];
            if (list.show) {
              _ref4 = list.tags;
              for (_l = 0, _len3 = _ref4.length; _l < _len3; _l++) {
                tag = _ref4[_l];
                tag = parseInt(tag, 10);
                if (__indexOf.call(avaliableTags, tag) < 0) {
                  avaliableTags.push(tag);
                }
              }
            }
          }
          _ref5 = this.subListTags;
          for (key in _ref5) {
            tagStyle = _ref5[key];
            for (_m = 0, _len4 = tagStyle.length; _m < _len4; _m++) {
              tag = tagStyle[_m];
              if (_ref6 = parseInt(tag.id, 10), __indexOf.call(avaliableTags, _ref6) < 0) {
                tag["switch"] = false;
              }
            }
          }
          return $rootScope.$broadcast('subListService.update', this.subList, this.subListTags);
        },
        filterClean: function() {
          var key, list, tag, tagStyle, _i, _j, _len, _len1, _ref, _ref1, _results;

          _ref = this.subListTags;
          for (key in _ref) {
            tagStyle = _ref[key];
            for (_i = 0, _len = tagStyle.length; _i < _len; _i++) {
              tag = tagStyle[_i];
              tag["switch"] = true;
            }
          }
          _ref1 = this.subList;
          _results = [];
          for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
            list = _ref1[_j];
            _results.push(list.show = true);
          }
          return _results;
        },
        getUserPrefer: function() {
          return $http({
            method: 'GET',
            url: '/accounts/prefer/get/'
          }).success(function(data) {
            var list, lists, result, sort, tagId, tagsList, _i, _len;

            lists = data;
            tagsList = tagsListService.list;
            result = {
              an: [],
              ep: []
            };
            if (lists !== 'false') {
              for (sort in lists) {
                list = lists[sort];
                for (_i = 0, _len = list.length; _i < _len; _i++) {
                  tagId = list[_i];
                  result[sort.toLowerCase()].push(tagsList[sort.toLowerCase()][tagId]);
                }
              }
            }
            return $rootScope.$broadcast('preferList.update', result);
          });
        },
        getUserPreferNum: function(sort) {
          return angular.fromJson(localStorage.getItem('test_prefer_list'))[sort];
        }
      };
    }
  ]);

}).call(this);

/*
//@ sourceMappingURL=services.map
*/
