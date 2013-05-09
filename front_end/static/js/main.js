// Generated by CoffeeScript 1.6.2
(function() {
  $('.home-hero').height($(window).height() - 4);

  $('.nav-login').click(function() {
    return $('.index-upper-login').fadeToggle();
  });

  $('.btn-reg-top').click(function() {
    return $.scrollTo('.login-screen', 1000);
  });

  $('.hero-help').click(function() {
    return $.scrollTo('.feature-intro-word', 800);
  });

  $('.login-form-new').find('.login-btn').click(function(e) {
    var $login_form;

    e.preventDefault();
    $login_form = $(this).parents('.login-form-new');
    return $.ajax({
      dataType: 'json',
      url: $login_form.attr('action'),
      type: 'post',
      data: {
        username: $login_form.find('#login-name').val(),
        password: $login_form.find('#login-pass').val(),
        remember: $login_form.find('.login-remember').val()
      },
      success: function(data) {
        return console.log(data);
      }
    });
  });

}).call(this);
