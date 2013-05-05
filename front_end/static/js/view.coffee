info_id = $('.info-view').data('id')
info_sort = $('.info-view').data('sort')
sub_lists = localStorage.getItem('sub_list_'+info_id)
tags_lists = localStorage.getItem('sub_list_'+info_sort)

# get select tags
$('.tags').find('.tag').click ->
  $(@).clone(true).appendTo($('.selected_tags'))
