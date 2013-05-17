# maybe all pages

#form csrf
csrfSafeMethod = (method) -> (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
$.ajaxSetup(
    crossDomain: false,
    beforeSend: (xhr, settings) ->
        if not csrfSafeMethod(settings.type)
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))
    );

#tooltip
$('.has-tooltip').tooltip()

#login
$('.nav-login').click ->
  $('.index-upper-reg').hide();
  $('.index-upper-login').fadeToggle();
$('.login-form-new').find('.login-btn').click (e) ->
  e.preventDefault()
  $login_form = $(this).parents('.login-form-new')
  $login_form.find('.alert').slideUp('fast')
  $.ajax(
    dataType: 'json'
    url: $login_form.attr('action')
    type: 'post'
    data: $login_form.serialize()
    error: -> $login_form.find('.alert').slideDown('fast')
    success: (data) -> window.location = data.url if data.status
  )

#reg
$('.nav-reg').click ->
  $('.index-upper-login').hide();
  $('.index-upper-reg').fadeToggle();
$('.login-form-new').find('.reg-btn').click (e) ->
  e.preventDefault()
  $login_form = $(this).parents('.login-form-new')
  $login_form.find('.alert').slideUp('fast')
  $.ajax({
    dataType: 'json'
    url: $login_form.attr('action')
    type: 'post'
    data: $login_form.serialize()
    error: -> $login_form.find('.alert').slideDown('fast')
    success: (data) ->
      if(data.status)
        window.location = data.url if data.status
      else
        $login_form.find('.alert').text(data.msg).slideDown('fast')
  })



#info item animation
$('.info-item').parent().mouseenter ->
  $(this).find('.info-border').stop().animate(
    'border-width': '25px 25px 40px 25px'
    'margin-left': '-20px'
    'margin-top': '-15px'
  , 'fast')
$('.info-item').parent().mouseleave ->
  $(this).find('.info-border').stop().animate(
    'border-width': '5px 5px 5px 5px'
    'margin-left': '0'
    'margin-top': '0'
  ,'fast')