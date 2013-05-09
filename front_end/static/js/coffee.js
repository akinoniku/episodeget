// Generated by CoffeeScript 1.6.2
(function() {
  var csrfSafeMethod;

  csrfSafeMethod = function(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  };

  $.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
        return xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
      }
    }
  });

  $('.has-tooltip').tooltip();

  $(window).resize(function() {
    return $('.home-hero').height($(window).height() - 4);
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
