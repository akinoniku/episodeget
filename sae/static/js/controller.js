// Generated by CoffeeScript 1.6.3
(function() {
  var __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  angular.module('episodeGet.controllers', []).controller('HomePageCtrl', function() {
    $('.home-hero').height($(window).height() - 4);
    $(window).resize(function() {
      return $('.home-hero').height($(window).height() - 4);
    });
    $('.feature-item').mouseenter(function() {
      return $(this).stop().addClass('animated swing');
    });
    $('.btn-reg-top').click(function() {
      return $.scrollTo('.login-screen', 1000);
    });
    return $('.hero-help').click(function() {
      return $.scrollTo('.feature-intro-word', 800);
    });
  }).controller('NavCtrl', function($scope, $location, $http, userService) {
    var now;
    now = Date.parse(new Date());
    if ((localStorage.getItem('info_timeout') != null) && now - localStorage.getItem('info_timeout') > 259200000) {
      localStorage.removeItem('infoList_an');
      localStorage.removeItem('infoList_ep');
    }
    if ((localStorage.getItem('tags_timeout') != null) && now - localStorage.getItem('tags_timeout') > 259200000) {
      localStorage.removeItem('tagsList_an');
      localStorage.removeItem('tagsList_ep');
    }
    $scope.$on('infoListService.update', function(event, List) {
      return localStorage.setItem('info_timeout', now);
    });
    $scope.$on('tagsListService.update', function(event, list) {
      return localStorage.setItem('tags_timeout', now);
    });
    $scope.login = {
      email: '',
      username: '',
      password: '',
      status: false,
      show: false,
      show_reg: false,
      msg: '',
      login_id: 'top',
      logined: !!userService.user.id,
      loginSubmit: function() {
        return userService.loginSubmit(this.username, this.password);
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
            if (data) {
              userService.updateUser(data);
              return $scope.login.logined = data.id !== 0 && (data.id != null);
            } else {
              $scope.user = userService.user;
              return $scope.login.logined = false;
            }
          });
        }
      }
    };
    $scope.$on('userService.login', function(event, user) {
      $scope.user = user;
      $scope.login.status = !user.id;
      if (user.id !== 0) {
        $scope.login.logined = true;
        $scope.login.show = false;
        $scope.login.show_reg = false;
        if ($location.path() === '/') {
          return $location.path('/accounts/');
        }
      }
    });
    $scope.user = userService.user;
    $scope.$on('userService.update', function(event, user) {
      return $scope.user = user;
    });
    $scope.$on('userService.reg', function(event, user, status, msg) {
      $scope.user = user;
      $scope.login.status = status;
      $scope.login.msg = '';
      if (status) {
        $scope.login.logined = true;
        $scope.login.show = false;
        $scope.login.show_reg = false;
        if ($location.path() === '/') {
          return $location.path('/accounts/prefer');
        }
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
    $scope.tab = function() {
      if ($location.path().indexOf('an') !== -1) {
        return 'an';
      } else if ($location.path().indexOf('ep') !== -1) {
        return 'ep';
      } else if ($location.path().indexOf('accounts') !== -1) {
        return 'accounts';
      }
    };
    return $scope.login.checkLogin();
  }).controller('InfoListCtrl', function($scope, $http, $routeParams, infoListService) {
    var sort;
    sort = $routeParams.sort;
    $scope.sort = sort;
    $scope.page = $routeParams.page ? $routeParams.page : 1;
    $scope.sort = sort;
    infoListService.getList(sort);
    $scope.createPage = function(list, sort, page) {
      var endItem, startItem, totalPage, _i, _ref, _results;
      $scope.currentList = list[sort];
      if ($scope.currentList == null) {
        return false;
      }
      totalPage = parseInt($scope.currentList.length / 12);
      $scope.pages = (function() {
        _results = [];
        for (var _i = 1; 1 <= totalPage ? _i <= totalPage : _i >= totalPage; 1 <= totalPage ? _i++ : _i--){ _results.push(_i); }
        return _results;
      }).apply(this);
      $scope.previewPage = parseInt($scope.page) === 1 ? 1 : page - 1;
      $scope.nextPage = parseInt($scope.page) === totalPage ? parseInt($scope.page) : parseInt($scope.page) + 1;
      startItem = (0 < (_ref = parseInt(page)) && _ref <= totalPage) ? (page - 1) * 12 : 0;
      endItem = parseInt(page) > totalPage ? false : startItem + 11;
      if (endItem) {
        return $scope.currentPage = list[sort].slice(startItem, +endItem + 1 || 9e9);
      } else {
        return $scope.currentPage = list[sort].slice(startItem);
      }
    };
    $scope.$on('infoListService.update', function(event, List) {
      return $scope.createPage(List, sort, $scope.page);
    });
    $scope.sortInfo = infoListService.sortInfo;
    $scope.inListView = true;
    return $scope.createPage(infoListService.list, sort, $scope.page);
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
      return $http({
        method: 'POST',
        url: 'add_list_one_click/',
        data: $.param({
          infoId: id
        })
      }).success(function() {
        return $location.path('/accounts');
      });
    };
  }).controller('UserAccountCtrl', function($scope, $location, $http, userService, $filter, tagsListService) {
    var sort, _i, _len, _ref;
    $scope.inAccount = true;
    $scope.user = userService.user;
    userService.listUpdate();
    $scope.$on('userService.listUpdate', function(event, user) {
      var list, tag, _i, _len, _ref, _results;
      $scope.user = user;
      $scope.feedUrl = "http://episodeget.sinaapp.com/feed/" + $scope.user.username + ".rss";
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
    $scope.removeSubList = function() {
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
    _ref = ['an', 'ep'];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      sort = _ref[_i];
      tagsListService.getList(sort);
    }
    return $scope.$on('tagsListService.update', function(event, list, sort) {
      $scope.tagsList[sort] = resortTag(list[sort]);
      return $scope.unsortTags[sort] = list[sort];
    });
  }).controller('PreferCtrl', function($scope, $location, $http, userService, tagsListService, subListService) {
    var resortTag, sort, _i, _len, _ref;
    $scope.inAccount = true;
    $scope.sort = 'an';
    $scope.user = userService.user;
    $scope.tagsList = {};
    $scope.unsortTags = {};
    $scope.userPrefer = angular.fromJson('{"AN":[128,10,15,13,50,11,14,41,51,123,126,133],"EP":[170,844,186]}');
    $scope.searchInput = '';
    $scope.selectExample = function(listType) {
      var preferExample;
      preferExample = {
        normal: '{"AN":[128,10,15,13,50,11,14,41,51,123,126,133],"EP":[170,844,186]}',
        clear: '{"AN":[128,10,15,13,50,11,14,41,51,124,129],"EP":[170,844,184]}',
        learner: '{"AN":[138,128,129],"EP":[181,183]}'
      };
      return $http({
        method: 'POST',
        url: '/accounts/prefer/save/',
        data: $.param({
          list: preferExample[listType]
        })
      }).success(function() {
        return $location.path('/accounts');
      });
    };
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
    $scope.$on('tagsListService.update', function(event, list, sort) {
      $scope.tagsList[sort] = resortTag(list[sort]);
      $scope.unsortTags[sort] = list[sort];
      return subListService.getUserPrefer();
    });
    _ref = ['an', 'ep'];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      sort = _ref[_i];
      tagsListService.getList(sort);
    }
    $scope.$on('preferList.update', function(event, result) {
      return $scope.userPrefer = result;
    });
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
        AN: [],
        EP: []
      };
      _ref1 = ['AN', 'EP'];
      for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
        sort = _ref1[_j];
        _ref2 = $scope.userPrefer[sort.toLowerCase()];
        for (_k = 0, _len2 = _ref2.length; _k < _len2; _k++) {
          tag = _ref2[_k];
          list[sort].push(tag.id);
        }
        localStorage.setItem('test_prefer_list', angular.toJson(list));
      }
      return $http({
        method: 'POST',
        url: '/accounts/prefer/save/',
        data: $.param({
          list: angular.toJson(list)
        })
      }).success(function() {
        return $location.path('/accounts');
      });
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