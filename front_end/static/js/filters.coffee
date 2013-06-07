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
  .filter('niceTime',[ ->
    (input) ->
      second = 1000
      minutes = second * 60
      hours = minutes * 60
      days = hours * 24
      months = days * 30
      twomonths = days * 365
      myDate = new Date(Date.parse(input))
      myDate = new Date(input.replace(/-/g, "/")) if (isNaN(myDate))
      nowtime = new Date()
      longtime = nowtime.getTime() - myDate.getTime()
      switch
        when longtime > months then "#{ Math.floor(longtime / months)}个月前"
        when longtime > days then "#{ Math.floor(longtime / (days * 7))}周前"
        when longtime > days then "#{ Math.floor(longtime / days)}天前"
        when longtime > hours then "#{Math.floor(longtime / hours)}小时前"
        when longtime > minutes then "#{Math.floor(longtime / minutes)}分钟前"
        # when longtime > second then "#{Math.floor(longtime / second)}秒前"
        else "刚刚";
  ])
