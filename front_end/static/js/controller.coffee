angular.module('episodeGet.controllers', [])
  .controller('HomePageCtrl', [() ->
    $('.home-hero').height $(window).height()-4
    $(window).resize -> $('.home-hero').height $(window).height()-4
    $('.btn-reg-top').click -> $.scrollTo('.login-screen',1000)
    $('.hero-help').click -> $.scrollTo('.feature-intro-word',800)
    $('.feature-item').mouseenter -> $(@).stop().addClass('animated swing')
  ])
  .controller('NavCtrl', ($scope)->
    $scope.template={name: 'nav.html', url: 'static/partials/nav.html'}
  )
