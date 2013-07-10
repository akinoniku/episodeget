// Generated by CoffeeScript 2.0.0-beta5
angular.module('episodeGet.controllers', []).controller('HomePageCtrl', function () {
  $('.home-hero').height($(window).height() - 4);
  $(window).resize(function () {
    return $('.home-hero').height($(window).height() - 4);
  });
  $('.btn-reg-top').click(function () {
    return $.scrollTo('.login-screen', 1e3);
  });
  $('.hero-help').click(function () {
    return $.scrollTo('.feature-intro-word', 800);
  });
  return $('.feature-item').mouseenter(function () {
    return $(this).stop().addClass('animated swing');
  });
}).controller('NavCtrl', function ($scope, $http, userService) {
  $scope.user = userService.user;
  $scope.$on('userService.update', function (event, user) {
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
    loginSubmit: function () {
      return $scope.login.status = userService.loginSubmit(this.username, this.password);
    },
    regSubmit: function () {
      return userService.regSubmit(this.email, this.username, this.password);
    },
    logout: function () {
      return userService.logoutSubmit();
    },
    checkLogin: function () {
      if (!$scope.login.logined)
        return $http({
          method: 'GET',
          url: '/accounts/current/'
        }).success(function (data) {
          userService.updateUser(data);
          return $scope.login.logined = data.id !== 0;
        }).error(function () {
          $scope.user = userService.user;
          return $scope.login.logined = false;
        });
    }
  };
  $scope.$on('userService.login', function (event, user) {
    $scope.user = user;
    $scope.login.status = !!user.id;
    if (user.id !== 0) {
      $scope.login.logined = true;
      $scope.login.show = false;
      return $scope.login.show_reg = false;
    }
  });
  $scope.$on('userService.reg', function (event, user, status, msg) {
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
  $scope.$on('userService.logout', function (event, user) {
    $scope.user = user;
    $scope.login.status = !!user.id;
    if (!user.id) {
      $scope.login.logined = false;
      return $scope.login.show = false;
    }
  });
  return $scope.login.checkLogin();
}).controller('InfoListCtrl', function ($scope, $http, $routeParams, infoListService) {
  var sort;
  sort = $routeParams.sort;
  $scope.$on('infoListService.update', function (event, List) {
    return $scope.currentList = List[sort];
  });
  $scope.currentList = infoListService.list[sort];
  $scope.sortInfo = infoListService.sortInfo;
  $scope.sort = sort;
  $scope.inListView = true;
  return infoListService.getList(sort);
}).controller('InfoViewCtrl', function ($scope, $http, $routeParams, $location, infoListService, infoService, tagsListService, subListService, userService) {
  var cache$, id, sort;
  cache$ = [
    $routeParams.id,
    $routeParams.sort
  ];
  id = cache$[0];
  sort = cache$[1];
  $scope.user = userService.user;
  $scope.$on('userService.update', function (event, user) {
    return $scope.user = user;
  });
  $scope.$on('infoListService.update', function (event, List) {
    return $scope.list = List;
  });
  $scope.info = infoService.getInfo(sort, id);
  $scope.$on('tagsListService.update', function (event, list) {
    return $scope.tagsList = list;
  });
  tagsListService.getList(sort);
  $scope.tagsList = tagsListService.list[sort];
  subListService.getList(sort, id);
  $scope.$on('subListService.update', function (event, subList, subListTags) {
    $scope.subList = subList;
    return $scope.subListTags = subListTags;
  });
  $scope.tagClass = function () {
    if (this.tag['switch']) {
      return 'tag';
    } else {
      return 'tag disabled';
    }
  };
  $scope.pickTag = function (style, id) {
    return subListService.pickTag(style, id);
  };
  $scope.filterClean = function () {
    return subListService.filterClean();
  };
  $scope.addListBtn = '\u6dfb\u52a0';
  $scope.addSubList = function (id) {
    return $http({
      method: 'POST',
      url: 'add_list_ajax/',
      data: $.param({ list_id: id })
    }).success(function () {
      return $location.path('/accounts');
    }).error(function () {
      return $scope.addListBtn = '\u54a6\uff0c\u597d\u50cf\u51fa\u9519\u4e86';
    });
  };
  return $scope.calOneClick = function () {
    var largestWeight, list, newest, newList, subList, tagId, tagStyle;
    list = subListService.getUserPreferNum(sort);
    largestWeight = 0;
    for (var i$ = 0, length$ = $scope.subList.length; i$ < length$; ++i$) {
      subList = $scope.subList[i$];
      for (var i$1 = 0, length$1 = list.length; i$1 < length$1; ++i$1) {
        tagId = list[i$1];
        if (in$(tagId, subList.tags)) {
          tagStyle = $scope.tagsList[tagId].style;
          if (null != subList.styleList)
            subList.styleList;
          else
            subList.styleList = [];
          if (!in$(tagStyle, subList.styleList)) {
            subList.styleList.push(tagStyle);
            subList.weight = subList.styleList.length;
            if (largestWeight < subList.weight)
              largestWeight = subList.weight;
          }
        }
      }
    }
    newList = $scope.subList.filter(function (x) {
      return x.weight === largestWeight;
    });
    newest = newList[0];
    for (var i$2 = 0, length$2 = newList.length; i$2 < length$2; ++i$2) {
      list = newList[i$2];
      if (list.update_time > newest.update_time)
        newest = list;
    }
    return $scope.addSubList(newest.id);
  };
}).controller('UserAccountCtrl', function ($scope, $http, userService, $filter) {
  $scope.inAccount = true;
  $scope.user = userService.user;
  userService.listUpdate();
  $scope.$on('userService.listUpdate', function (event, user) {
    $scope.user = user;
    return function (accum$) {
      var list;
      for (var i$ = 0, length$ = user.list.length; i$ < length$; ++i$) {
        list = user.list[i$];
        list.tagsString = '';
        accum$.push(function (accum$1) {
          var tag;
          for (var i$1 = 0, length$1 = list.tags.length; i$1 < length$1; ++i$1) {
            tag = list.tags[i$1];
            accum$1.push(list.tagsString += ' ' + $filter('getTagNameById')(tag, list.sort));
          }
          return accum$1;
        }.call(this, []));
      }
      return accum$;
    }.call(this, []);
  });
  return $scope.removeSubList = function () {
    return $http({
      method: 'POST',
      url: 'remove_list_ajax/',
      data: $.param({ list_id: this.list.id })
    }).success(function () {
      return userService.listUpdate();
    });
  };
}).controller('PreferCtrl', function ($scope, $http, userService, tagsListService, subListService) {
  var resortTag, sort;
  $scope.inAccount = true;
  $scope.sort = 'an';
  $scope.user = userService.user;
  $scope.tagsList = {};
  $scope.unsortTags = {};
  $scope.userPrefer = subListService.getUserPrefer();
  $scope.searchInput = '';
  resortTag = function (tags) {
    var k, preSubListTags, subListTags, tag;
    preSubListTags = {
      TM: [],
      CL: [],
      FM: [],
      LG: []
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
  for (var cache$ = [
        'an',
        'ep'
      ], i$ = 0, length$ = cache$.length; i$ < length$; ++i$) {
    sort = cache$[i$];
    $scope.$on('tagsListService.update', function (event, list) {
      $scope.tagsList[sort] = resortTag(list[sort]);
      return $scope.unsortTags[sort] = list[sort];
    });
    tagsListService.getList(sort);
  }
  $scope.searchTags = function (sort, input) {
    var key, tag, tags;
    if (!input)
      return false;
    tags = [];
    for (key in $scope.unsortTags[sort]) {
      tag = $scope.unsortTags[sort][key];
      if (tag.tags.toString().indexOf(input) !== -1)
        tags.push(tag);
    }
    return tags;
  };
  $scope.addTag = function (tag) {
    if (!in$(tag, $scope.userPrefer))
      $scope.userPrefer[$scope.sort].push(tag);
    return $scope.searchInput = '';
  };
  $scope.removeTag = function (key) {
    return $scope.userPrefer[$scope.sort].splice(key, 1);
  };
  $scope.savePrefer = function () {
    var list, tag;
    list = {
      an: [],
      ep: []
    };
    for (var cache$1 = [
          'an',
          'ep'
        ], i$1 = 0, length$1 = cache$1.length; i$1 < length$1; ++i$1) {
      sort = cache$1[i$1];
      for (var i$2 = 0, length$2 = $scope.userPrefer[sort].length; i$2 < length$2; ++i$2) {
        tag = $scope.userPrefer[sort][i$2];
        list[sort].push(tag.id);
      }
      localStorage.setItem('test_prefer_list', angular.toJson(list));
    }
    return list;
  };
  return $scope.getSortClass = function (sort) {
    if ($scope.sort === sort) {
      return 'btn btn-primary active';
    } else {
      return 'btn btn-primary';
    }
  };
});
function in$(member, list) {
  for (var i = 0, length = list.length; i < length; ++i)
    if (i in list && list[i] === member)
      return true;
  return false;
}
