$('.has-tooltip').tooltip()
$('.home-hero').height $(window).height()-4
$(window).resize ->
  $('.home-hero').height $(window).height()-4
$('.info-item').mouseenter ->
  $(this).find('.info-border').stop().animate({
    'border-width': '5px 15px 40px 15px',
    'margin-left': '-10px',
  })
$('.info-item').mouseleave ->
  $(this).find('.info-border').stop().animate({
    'border-width': '5px 5px 5px 5px',
    'margin-left': '0',
  })
