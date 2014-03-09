$('.account-setting-btn').click -> $('.account-setting').slideToggle()
$('#xunleiNeedLogin').find('.btn-primary').click (e) ->
  e.preventDefault()
  e.stopPropagation()
  $('#xunleiNeedLogin').find('.alert').slideUp('fast')
  $.ajax
    url: '/accounts/xunlei/'
    dataType: 'json'
    type: 'post'
    data: $('#xunleiNeedLogin').serialize()
    success: (data) ->
      if data.status
        $('#xunleiNeedLogin').hide()
        $('#xunleiLogined').show()
      else
        $('#xunleiNeedLogin').find('.alert').slideDown('fast')
