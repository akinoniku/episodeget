$('.home-hero').height $(window).height()-4
$(window).resize ->
  $('.home-hero').height $(window).height()-4
$(window).scroll ->
  if $(document).scrollTop()> $(window).height()/2
    $('.feature-item-1').fadeIn(1400)
  if $(document).scrollTop()> $(window).height()/2-20
    $('.feature-item-2').fadeIn(1400)
  if $(document).scrollTop()> $(window).height()/2-20
    $('.feature-item-3').fadeIn(1400)
  if $(document).scrollTop()> $(window).height()/2
   $('#time-line').animate 'margin-top': '30px'
