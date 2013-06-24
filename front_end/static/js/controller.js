// Generated by CoffeeScript 1.6.2
(function() {
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
      username: '',
      password: '',
      status: true,
      show: false,
      login_id: 'top',
      logined: !!userService.user.id,
      showLogin: function() {
        return this.show = !this.show;
      },
      isShownLogin: function() {
        return this.show;
      },
      isLogined: function() {
        return this.logined;
      },
      loginActionStatus: function() {
        return this.status;
      },
      loginSubmit: function() {
        return $scope.login.status = userService.loginSubmit(this.username, this.password);
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
      if (user.id) {
        $scope.login.logined = true;
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
    return $scope.addSubList = function() {
      return $http({
        method: 'POST',
        url: 'add_list_ajax/',
        data: $.param({
          list_id: this.list.id
        })
      }).success(function() {
        return $location.path('/accounts');
      }).error(function() {
        return $scope.addListBtn = '咦，好像出错了';
      });
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
  }).controller('PreferCtrl', function($scope, $http, userService, tagsListService) {
    var resortTag, sort, _i, _len, _ref, _results;

    $scope.inAccount = true;
    $scope.user = userService.user;
    $scope.tagsList = {};
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
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      sort = _ref[_i];
      $scope.$on('tagsListService.update', function(event, list) {
        return $scope.tagsList[sort] = resortTag(list);
      });
      tagsListService.getList(sort);
      _results.push($scope.tagsList[sort] = resortTag(tagsListService.list[sort]));
    }
    return _results;
  });

}).call(this);
