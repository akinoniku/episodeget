// Generated by CoffeeScript 1.6.2
(function() {
  var __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  angular.module('episodeGet.controllers', []).controller('HomePageCtrl', function() {
    $('.home-hero').height($(window).height() - 4);
    $(window).resize(function() {
      return $('.home-hero').height($(window).height() - 4);
    });
    $('.btn-reg-top').click(function() {
      return $.scrollTo('.login-screen', 1000);
    });
    $('.hero-help').click(function() {
      return $.scrollTo('.feature-intro-word', 800);
    });
    return $('.feature-item').mouseenter(function() {
      return $(this).stop().addClass('animated swing');
    });
  }).controller('NavCtrl', function($scope, $http, userService) {
    $scope.user = userService.user;
    $scope.$on('userService.update', function(event, user) {
      return $scope.user = user;
    });
    $scope.login = {
      email: '',
      username: '',
      password: '',
      status: true,
      show: false,
      show_reg: false,
      msg: '',
      login_id: 'top',
      logined: !!userService.user.id,
      loginSubmit: function() {
        return $scope.login.status = userService.loginSubmit(this.username, this.password);
      },
      regSubmit: function() {
        return userService.regSubmit(this.email, this.username, this.password);
      },
      logout: function() {
        return userService.logoutSubmit();
      },
      checkLogin: function() {
        if (!$scope.login.logined) {
          return $http({
            method: 'GET',
            url: '/accounts/current/'
          }).success(function(data) {
            userService.updateUser(data);
            return $scope.login.logined = data.id !== 0;
          }).error(function() {
            $scope.user = userService.user;
            return $scope.login.logined = false;
          });
        }
      }
    };
    $scope.$on('userService.login', function(event, user) {
      $scope.user = user;
      $scope.login.status = !!user.id;
      if (user.id !== 0) {
        $scope.login.logined = true;
        $scope.login.show = false;
        return $scope.login.show_reg = false;
      }
    });
    $scope.$on('userService.reg', function(event, user, status, msg) {
      $scope.user = user;
      $scope.login.status = status;
      $scope.login.msg = '';
      if (status) {
        $scope.login.logined = true;
        $scope.login.show = false;
        return $scope.login.show_reg = false;
      } else {
        return $scope.login.msg = msg;
      }
    });
    $scope.$on('userService.logout', function(event, user) {
      $scope.user = user;
      $scope.login.status = !!user.id;
      if (!user.id) {
        $scope.login.logined = false;
        return $scope.login.show = false;
      }
    });
    return $scope.login.checkLogin();
  }).controller('InfoListCtrl', function($scope, $http, $routeParams, infoListService) {
    var sort;

    sort = $routeParams.sort;
    $scope.$on('infoListService.update', function(event, List) {
      return $scope.currentList = List[sort];
    });
    $scope.currentList = infoListService.list[sort];
    $scope.sortInfo = infoListService.sortInfo;
    $scope.sort = sort;
    $scope.inListView = true;
    return infoListService.getList(sort);
  }).controller('InfoViewCtrl', function($scope, $http, $routeParams, $location, infoListService, infoService, tagsListService, subListService, userService) {
    var id, sort, _ref;

    _ref = [$routeParams.id, $routeParams.sort], id = _ref[0], sort = _ref[1];
    $scope.user = userService.user;
    $scope.$on('userService.update', function(event, user) {
      return $scope.user = user;
    });
    $scope.$on('infoListService.update', function(event, List) {
      return $scope.list = List;
    });
    $scope.info = infoService.getInfo(sort, id);
    $scope.$on('tagsListService.update', function(event, list) {
      return $scope.tagsList = list;
    });
    tagsListService.getList(sort);
    $scope.tagsList = tagsListService.list[sort];
    subListService.getList(sort, id);
    $scope.$on('subListService.update', function(event, subList, subListTags) {
      $scope.subList = subList;
      return $scope.subListTags = subListTags;
    });
    $scope.tagClass = function() {
      if (this.tag["switch"]) {
        return 'tag';
      } else {
        return 'tag disabled';
      }
    };
    $scope.pickTag = function(style, id) {
      return subListService.pickTag(style, id);
    };
    $scope.filterClean = function() {
      return subListService.filterClean();
    };
    $scope.addListBtn = '添加';
    $scope.addSubList = function(id) {
      return $http({
        method: 'POST',
        url: 'add_list_ajax/',
        data: $.param({
          list_id: id
        })
      }).success(function() {
        return $location.path('/accounts');
      }).error(function() {
        return $scope.addListBtn = '咦，好像出错了';
      });
    };
    return $scope.calOneClick = function() {
      var largestWeight, list, newList, newest, subList, tagId, tagStyle, _i, _j, _k, _len, _len1, _len2, _ref1, _ref2;

      list = subListService.getUserPreferNum(sort);
      largestWeight = 0;
      _ref1 = $scope.subList;
      for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
        subList = _ref1[_i];
        for (_j = 0, _len1 = list.length; _j < _len1; _j++) {
          tagId = list[_j];
          if (__indexOf.call(subList.tags, tagId) >= 0) {
            tagStyle = $scope.tagsList[tagId].style;
            if ((_ref2 = subList.styleList) == null) {
              subList.styleList = [];
            }
            if (__indexOf.call(subList.styleList, tagStyle) < 0) {
              subList.styleList.push(tagStyle);
              subList.weight = subList.styleList.length;
              if (largestWeight < subList.weight) {
                largestWeight = subList.weight;
              }
            }
          }
        }
      }
      newList = $scope.subList.filter(function(x) {
        return x.weight === largestWeight;
      });
      newest = newList[0];
      for (_k = 0, _len2 = newList.length; _k < _len2; _k++) {
        list = newList[_k];
        if (list.update_time > newest.update_time) {
          newest = list;
        }
      }
      return $scope.addSubList(newest.id);
    };
  }).controller('UserAccountCtrl', function($scope, $http, userService, $filter) {
    $scope.inAccount = true;
    $scope.user = userService.user;
    userService.listUpdate();
    $scope.$on('userService.listUpdate', function(event, user) {
      var list, tag, _i, _len, _ref, _results;

      $scope.user = user;
      _ref = user.list;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        list = _ref[_i];
        list.tagsString = '';
        _results.push((function() {
          var _j, _len1, _ref1, _results1;

          _ref1 = list.tags;
          _results1 = [];
          for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
            tag = _ref1[_j];
            _results1.push(list.tagsString += ' ' + $filter('getTagNameById')(tag, list.sort));
          }
          return _results1;
        })());
      }
      return _results;
    });
    return $scope.removeSubList = function() {
      return $http({
        method: 'POST',
        url: 'remove_list_ajax/',
        data: $.param({
          list_id: this.list.id
        })
      }).success(function() {
        return userService.listUpdate();
      });
    };
  }).controller('PreferCtrl', function($scope, $http, userService, tagsListService, subListService) {
    var resortTag, sort, _i, _len, _ref;

    $scope.inAccount = true;
    $scope.sort = 'an';
    $scope.user = userService.user;
    $scope.tagsList = {};
    $scope.unsortTags = {};
    $scope.userPrefer = subListService.getUserPrefer();
    $scope.searchInput = '';
    resortTag = function(tags) {
      var k, preSubListTags, subListTags, tag;

      preSubListTags = {
        'TM': [],
        'CL': [],
        'FM': [],
        'LG': []
      };
      for (k in tags) {
        tag = tags[k];
        preSubListTags[tag.style].push(tag);
      }
      subListTags = [];
      for (k in preSubListTags) {
        tags = preSubListTags[k];
        subListTags.push(tags);
      }
      return subListTags;
    };
    _ref = ['an', 'ep'];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      sort = _ref[_i];
      $scope.$on('tagsListService.update', function(event, list) {
        $scope.tagsList[sort] = resortTag(list[sort]);
        return $scope.unsortTags[sort] = list[sort];
      });
      tagsListService.getList(sort);
    }
    $scope.searchTags = function(sort, input) {
      var key, tag, tags, _ref1;

      if (!input) {
        return false;
      }
      tags = [];
      _ref1 = $scope.unsortTags[sort];
      for (key in _ref1) {
        tag = _ref1[key];
        if (tag.tags.toString().indexOf(input) !== -1) {
          tags.push(tag);
        }
      }
      return tags;
    };
    $scope.addTag = function(tag) {
      if (__indexOf.call($scope.userPrefer, tag) < 0) {
        $scope.userPrefer[$scope.sort].push(tag);
      }
      return $scope.searchInput = '';
    };
    $scope.removeTag = function(key) {
      return $scope.userPrefer[$scope.sort].splice(key, 1);
    };
    $scope.savePrefer = function() {
      var list, tag, _j, _k, _len1, _len2, _ref1, _ref2;

      list = {
        an: [],
        ep: []
      };
      _ref1 = ['an', 'ep'];
      for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
        sort = _ref1[_j];
        _ref2 = $scope.userPrefer[sort];
        for (_k = 0, _len2 = _ref2.length; _k < _len2; _k++) {
          tag = _ref2[_k];
          list[sort].push(tag.id);
        }
        localStorage.setItem('test_prefer_list', angular.toJson(list));
      }
      return list;
    };
    return $scope.getSortClass = function(sort) {
      if ($scope.sort === sort) {
        return 'btn btn-primary active';
      } else {
        return 'btn btn-primary';
      }
    };
  });

}).call(this);

/*
//@ sourceMappingURL=controller.map
*/
