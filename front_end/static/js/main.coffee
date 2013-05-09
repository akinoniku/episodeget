#for index
$('.home-hero').height $(window).height()-4
$('.nav-login').click -> $('.index-upper-login').fadeToggle();
$('.btn-reg-top').click -> $.scrollTo('.login-screen',1000);
$('.hero-help').click -> $.scrollTo('.feature-intro-word',800);
$('.login-form-new').find('.login-btn').click (e) ->
  e.preventDefault()
  $login_form = $(this).parents('.login-form-new')
  $.ajax({
    dataType: 'json',
    url: $login_form.attr('action'),
    type: 'post',
    data: {
      username: $login_form.find('#login-name').val(),
      password: $login_form.find('#login-pass').val(),
      remember: $login_form.find('.login-remember').val()
    },
    success: (data) -> console.log(data)
  })