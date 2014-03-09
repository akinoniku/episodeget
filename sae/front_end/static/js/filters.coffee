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
      weeks = hours * 24 * 7
      months = days * 30
      myDate = new Date(Date.parse(input))
      myDate = new Date(input.replace(/-/g, "/")) if (isNaN(myDate))
      nowtime = new Date()
      longtime = nowtime.getTime() - myDate.getTime()
      switch
        when longtime > months then "#{ Math.floor(longtime / months)}个月前"
        when longtime > weeks then "#{ Math.floor(longtime / (days * 7))}周前"
        when longtime > days then "#{ Math.floor(longtime / days)}天前"
        when longtime > hours then "#{Math.floor(longtime / hours)}小时前"
        when longtime > minutes then "#{Math.floor(longtime / minutes)}分钟前"
        # when longtime > second then "#{Math.floor(longtime / second)}秒前"
        else "刚刚"
  ])
  .filter('averageDate',[ ->
    (rssList) ->
      counter = weekDay = weekHour = 0
      weekDays = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
      result = ''
      for id,rss of rssList
        myDate = new Date(Date.parse(rss.timestamp))
        myDate = new Date(rss.timestamp.replace(/-/g, "/")) if (isNaN(myDate))
        weekDays[myDate.getDay()]++
        weekHour += myDate.getHours()
        counter++
      lastCount = 0
      for day, count of weekDays
        if count > lastCount
          weekDay = day
      weekHour = weekHour/counter

      result = switch parseInt(weekDay, 10)
        when 0 then '星期天'
        when 1 then '星期一'
        when 2 then '星期二'
        when 3 then '星期三'
        when 4 then '星期四'
        when 5 then '星期五'
        when 6 then '星期六'
        else '不定时'

      result += switch
        when weekHour < 6 then '凌晨'
        when weekHour < 12 then '早上'
        when weekHour < 18 then '下午'
        else '晚上'
  ])
