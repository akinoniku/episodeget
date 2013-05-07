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
  for key, tags of current_list
    if key in selected_list
      for key, tag of tags
        if tag not in passed_tags
          passed_tags.push(tag)

  $('.tags').find('.tags-picker').find('.tag').removeClass('passed')
  $('.tags').find('.tags-picker').find('.tag').removeClass('disabled')
  for key, tag of passed_tags
    $('.tags').find('.tags-picker').find('.tag[data-id="'+tag+'"]').addClass('passed')
  $('.tags').find('.tags-picker').find('.tag').not('.passed').addClass('disabled')
  if (key for key, value of current_list).length is 0
    $('.btn-add-list').addClass('disabled')
      .attr('data-original-title', '请先从右边选择条件')
  else if (key for key, value of current_list).length is 1
    $('.btn-add-list').addClass('btn-primary').removeClass('disabled')
      .attr('data-original-title', '结果唯一，点击添加')
  else
    $('.btn-add-list').removeClass('btn-success').removeClass('disabled')
      .attr('data-original-title', '有多个结果，请继续添加条件或点击添加，系统会从符合条件的全部选项中筛选')
