// Generated by CoffeeScript 1.6.2
(function() {
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

  $('.feature-item').mouseenter(function() {
    return $(this).stop().addClass('animated swing');
  });

}).call(this);
