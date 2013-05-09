# maybe all pages
csrfSafeMethod = (method) -> (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
$.ajaxSetup({
    crossDomain: false,
    beforeSend: (xhr, settings) ->
        if (!csrfSafeMethod(settings.type))
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))
    });
$('.has-tooltip').tooltip()
$(window).resize ->
  $('.home-hero').height $(window).height()-4
$('.info-item').parent().mouseenter ->
  $(this).find('.info-border').stop().animate({
    'border-width': '25px 25px 40px 25px',
    'margin-left': '-20px',
    'margin-top': '-15px',
  }, 'fast')
$('.info-item').parent().mouseleave ->
  $(this).find('.info-border').stop().animate({
    'border-width': '5px 5px 5px 5px',
    'margin-left': '0',
    'margin-top': '0',
  },'fast')