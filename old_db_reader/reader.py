from django.db import connection

__author__ = 'akino'


def ani_rss_sql():
    cursor = connection.cursor()
    cursor.execute('SELECT * from getepisode.get_ani_rss')
    return cursor.fetchall()


def epi_rss_sql():
    cursor = connection.cursor()
    cursor.execute('SELECT * from getepisode.get_epi_rss')
    return cursor.fetchall()


def ani_tags_sql():
    cursor = connection.cursor()
    cursor.execute('SELECT * from getepisode.get_ani_tags')
    return cursor.fetchall()


def epi_tags_sql():
    cursor = connection.cursor()
    cursor.execute('SELECT * from getepisode.get_epi_tags')
    return cursor.fetchall()


def ani_info_sql():
    cursor = connection.cursor()
    cursor.execute('SELECT * from getepisode.get_ani_info')
    return cursor.fetchall()


def epi_info_sql():
    cursor = connection.cursor()
    cursor.execute('SELECT * from getepisode.get_epi_info')
    return cursor.fetchall()


def old_db_reader():
    counter = 0
    sql_list = []
    old_db = ani_rss_sql()
    total = len(old_db)
    for row in old_db:
        # if not FeedRss.objects.filter(hash_code=row[2][20:52]):
        new_ani_rss = FeedRss(
            sort='AN',
            title=row[1],
            link=row[2],
            hash_code=row[2][20:52],
            episode_id=0,
            timestamp=row[3]
        )
        counter += 1
        sql_list.append(new_ani_rss)
        if len(sql_list) > 500 or total == counter:
            FeedRss.objects.bulk_create(sql_list)
            sql_list = []

    counter = 0
    sql_list = []
    old_db = epi_rss_sql()
    total = len(old_db)
    for row in old_db:
        #if not FeedRss.objects.filter(hash_code=row[2][20:52]):
        new_epi_rss = FeedRss(
            sort='EP',
            title=row[1],
            link=row[2],
            hash_code=row[2][20:52],
            episode_id=0,
            timestamp=row[3]
        )
        counter += 1
        sql_list.append(new_epi_rss)
        if len(sql_list) > 500 or total == counter:
            FeedRss.objects.bulk_create(sql_list)
            sql_list = []

    mapper = {1: 'TM', 2: 'Tl', 3: 'CL', 4: 'FM', 5: 'LG'}

    old_db = ani_tags_sql()
    for row in old_db:
        if row[2] != 2 and not FeedTags.objects.filter(sort='AN', title=row[1]):
            new_tag = FeedTags(
                sort='AN',
                title=row[1],
                style=mapper[row[2]],
                tags=json.dumps(row[3].split(','))
            )
            new_tag.save()

    old_db = epi_tags_sql()
    for row in old_db:
        if row[2] != 2 and not FeedTags.objects.filter(sort='EP', title=row[1]):
            new_tag = FeedTags(
                sort='EP',
                title=row[1],
                style=mapper[row[2]],
                tags=json.dumps(row[3].split(','))
            )
            new_tag.save()

    c = langconv.Converter('zh-hans')
    old_db = ani_info_sql()
    for row in old_db:
        # title = c.convert(unicode(row[2], "utf-8"))
        title = c.convert(unicode(row[2]))
        if not FeedInfo.objects.filter(title=title):
            new_info = FeedInfo(
                sort='AN',
                title=title,
                now_playing=row[6],
            )
            new_info.save()

    old_db = epi_info_sql()
    for row in old_db:
        if not FeedInfo.objects.filter(title=row[2]):
            new_info = FeedInfo(
                sort='EP',
                title=row[2],
                now_playing=row[6],
            )
            new_info.save()
    return True