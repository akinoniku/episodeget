clone = (obj) ->
  if not obj? or typeof obj isnt 'object'
    return obj

  if obj instanceof Date
    return new Date(obj.getTime())

  if obj instanceof RegExp
    flags = ''
    flags += 'g' if obj.global?
    flags += 'i' if obj.ignoreCase?
    flags += 'm' if obj.multiline?
    flags += 'y' if obj.sticky?
    return new RegExp(obj.source, flags)

  newInstance = new obj.constructor()

  for key of obj
    newInstance[key] = clone obj[key]

  return newInstance


info_id = $('#info-view').data('id')
info_sort = $('#info-view').data('sort')
sub_lists = JSON.parse(localStorage.getItem('sub_list_'+info_id))
tags_lists = JSON.parse(localStorage.getItem('tags_list_'+info_sort))

# get select tags
$('.tags').find('.tags-picker').find('.tag').click ->
  if($(@).is('.disabled'))
    return false
  tag_id = $(@).data('id')
  if($('.selected-tags').find('[data-id='+tag_id+']').length > 0)
    $('.selected-tags').find('[data-id='+tag_id+']').remove()
    if($('.selected-tags').find('.tag[data-id]').length is 0)
      $('.tags').find('.tags-picker').find('.tag').removeClass('passed')
      $('.tags').find('.tags-picker').find('.tag').removeClass('disabled')
      return false
  else
    $(@).clone(true).appendTo($('.selected-tags'))

  $('.selected-tags').find('.tag .tagsinput-remove-link').removeClass('fui-plus-16').addClass('fui-cross-16')
  aviable_list()

aviable_list =(current_list) ->
  current_list = clone(sub_lists) if not current_list
  selected_list = []
  flag = true
  $('.selected-tags').find('.tag').each ->
    id = (String) $(@).data('id')
    new_list = []
    for key, tags of current_list
      if id in tags and key not in new_list
        new_list.push(key)
    if flag
      selected_list = clone(new_list)
    else
      for key, value of selected_list
        if value not in new_list
          delete selected_list[key]

    flag = false
    for key, tags of current_list
      if key not in selected_list
        delete current_list[key]

  passed_tags = []
  current_list_length = (key for key, value of current_list).length
  if(current_list_length is 0)
    $('.add-select.dk_container').addClass('disabled').find('.dk_label').text('请先从右边添加筛选条件');
  else if(current_list_length is 1)
    $('.add-select.dk_container').removeClass('disabled').find('.dk_label').text('结果唯一，点击添加');
  else
    $('.add-select.dk_container').removeClass('disabled').find('.dk_label').text('有 ' +current_list_length + ' 个结果，点击查看列表');
  $('#list-selector-dp').empty()
  for key, tags of current_list
    # get list names
    tags_title = ''
    for innerKey, tag of tags
      t = $('#sub-list-tag-id-'+ tag).data('title')
      tags_title += t + ' | ' if t
    $('#list-selector-dp').append("""<li><a data-value="#{key}">#{tags_title}</a></li>""")

    # get passed tags
    if key in selected_list
      for key, tag of tags
        if tag not in passed_tags
          passed_tags.push(tag)

  # view staff
  $('.tags').find('.tags-picker').find('.tag').removeClass('passed')
  $('.tags').find('.tags-picker').find('.tag').removeClass('disabled')
  for key, tag of passed_tags
    $('.tags').find('.tags-picker').find('.tag[data-id="'+tag+'"]').addClass('passed')
  $('.tags').find('.tags-picker').find('.tag').not('.passed').addClass('disabled')
