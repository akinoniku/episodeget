angular.module('episodeGet.filter', [])
  .filter('tagStyle', ()->
    (input)->
      switch input
        when 'TM' then '字幕组'
        when 'TL' then '作品名'
        when 'CL' then '清晰度'
        when 'FM' then '格式'
        when 'LG' then '字幕语言'
        else '不知道'
  )
  .filter('getTagNameById', ['tagsListService', (tagsListService)->
    (input, sort)-> tagsListService.list[angular.lowercase(sort)][input]?.title ? ''
  ]
  )