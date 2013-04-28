$('.home-hero').height $(window).height()-4
$(window).resize ->
  $('.home-hero').height $(window).height()-4
$(window).scroll ->
  if $(document).scrollTop()> $(window).height()*3/5
    $('.feature-item-1').fadeIn(1400)
  if $(document).scrollTop()> $(window).height()*3/5+20
    $('.feature-item-2').fadeIn(1400)
  if $(document).scrollTop()> $(window).height()*3/5+40
    $('.feature-item-3').fadeIn(1400)
  if $(document).scrollTop()> $(window).height()*3/5
   $('#time-line').animate 'margin-top': '30px'
