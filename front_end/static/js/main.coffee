#for index
$('.home-hero').height $(window).height()-4
$(window).resize -> $('.home-hero').height $(window).height()-4
$('.btn-reg-top').click -> $.scrollTo('.login-screen',1000);
$('.hero-help').click -> $.scrollTo('.feature-intro-word',800);
