// Generated by CoffeeScript 1.6.2
(function() {
  var csrfSafeMethod, csrftoken;

  csrftoken = $.cookie('csrftoken');

  csrfSafeMethod = function(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  };

  $.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
        return xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  $('.has-tooltip').tooltip();

  $('.nav-reg').click(function() {
    $('.index-upper-login').hide();
    return $('.index-upper-reg').fadeToggle();
  });

  $('.login-form-new').find('.reg-btn').click(function(e) {
    var $login_form;

    e.preventDefault();
    $login_form = $(this).parents('.login-form-new');
    $login_form.find('.alert').slideUp('fast');
    return $.ajax({
      dataType: 'json',
      url: $login_form.attr('action'),
      type: 'post',
      data: $login_form.serialize(),
      error: function() {
        return $login_form.find('.alert').slideDown('fast');
      },
      success: function(data) {
        if (data.status) {
          return window.location = data.url;
        } else {
          return $login_form.find('.alert').text(data.msg).slideDown('fast');
        }
      }
    });
  });

  $('.info-item').parent().mouseenter(function() {
    return $(this).find('.info-border').stop().animate({
      'border-width': '25px 25px 40px 25px',
      'margin-left': '-20px',
      'margin-top': '-15px'
    }, 'fast');
  });

  $('.info-item').parent().mouseleave(function() {
    return $(this).find('.info-border').stop().animate({
      'border-width': '5px 5px 5px 5px',
      'margin-left': '0',
      'margin-top': '0'
    }, 'fast');
  });

}).call(this);
