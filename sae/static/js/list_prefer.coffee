$(document).ready ->
  # sort tags
  $( ".sortable" ).sortable({
    axis: "y"
    cursor: 'move'
    opacity: 0.8
    scroll: true
  }).disableSelection()

  # sort
  $( ".p-sort" ).sortable({
    axis: "x"
    cursor: 'move'
    opacity: 0.8
  }).disableSelection()

  # change type of sort
  $('.type-select').find('.btn').click ->
    $(@).siblings().removeClass('active')
    sort = $(@).addClass('active').data('type')
    $('.p-container').hide()
    $('.p-container.'+sort).show()

  # Save
  getTypeSort = (type) -> $('.p-container.'+type).find( ".p-sort" ).sortable( "toArray", { attribute : "data-type" } )
  getTagsSort = (type, style) -> $('.p-container.'+type).find( ".p-tags." + style ).find( ".sortable" ).sortable( "toArray", { attribute : "data-id" } )
  $('.save-btn').click ->
    preferList = {}
    for type in ['an', 'ep']
      preferList[type] = {}
      for style in getTypeSort(type)
       preferList[type][style] = getTagsSort(type, style)
    localStorage.setItem('preferList', JSON.stringify(preferList))
    $.ajax({
      url: '/accounts/prefer/'
      type: 'post'
      dataType: 'json'
      data: {list:JSON.stringify(preferList)}
      success: (data)->
        console.log(data)
    })


  # Restore
  preferList= JSON.parse(localStorage.getItem('preferList'))
  for type, prefer of preferList
    $p_container = $('.p-container.'+type).find('.p-sort')
    for style, tag_list of prefer
      $p_container.append($p_container.find( ".p-tags." + style ))
      $style = $p_container.find( ".p-tags." + style ).find( ".sortable" )
      for key ,tag_id of tag_list
        $style.append($style.find("[data-id='#{ tag_id }']"))
