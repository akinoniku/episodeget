$('.account-setting-btn').click -> $('.account-setting').slideToggle()
$('#xunleiNeedLogin').find('.btn-primary').click ->
  $.ajax
    url: '/accounts/xunlei'
    dataType: 'json'
    type: 'post'
    data: $('#xunleiNeedLogin').serialize()
    success: (data) ->
      if data.status
        $('#xunleiNeedLogin').hide()
        $('#xunleiLogined').show()
