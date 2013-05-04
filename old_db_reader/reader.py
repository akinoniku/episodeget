# coding=utf-8
import json
import platform
from django.db import connection
from extra_app.langcov import langconv
from feeds_analysis.models import Rss, Tags, Info

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
        new_ani_rss = Rss(
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
            Rss.objects.bulk_create(sql_list)
            sql_list = []

    counter = 0
    sql_list = []
    old_db = epi_rss_sql()
    total = len(old_db)
    for row in old_db:
        new_epi_rss = Rss(
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
            Rss.objects.bulk_create(sql_list)
            sql_list = []

    #mapper = {1: 'TM', 2: 'Tl', 3: 'CL', 4: 'FM', 5: 'LG'}

    #old_db = ani_tags_sql()
    #for row in old_db:
    #    if row[2] != 2 and not Tags.objects.filter(sort='AN', title=row[1]):
    #        new_tag = Tags(
    #            sort='AN',
    #            title=row[1],
    #            style=mapper[row[2]],
    #            tags=json.dumps(row[3].split(','))
    #        )
    #        new_tag.save()

    #old_db = epi_tags_sql()
    #for row in old_db:
    #    if row[2] != 2 and not Tags.objects.filter(sort='EP', title=row[1]):
    #        new_tag = Tags(
    #            sort='EP',
    #            title=row[1],
    #            style=mapper[row[2]],
    #            tags=json.dumps(row[3].split(','))
    #        )
    #        new_tag.save()

    #c = langconv.Converter('zh-hans')
    #plat = platform.system()
    #old_db = ani_info_sql()
    #for row in old_db:
    #    if plat == "Windows":
    #        title = c.convert(unicode(row[2], "utf-8"))
    #    else:
    #        title = c.convert(unicode(row[2]))
    #    if not Info.objects.filter(title=title):
    #        new_info = Info(
    #            sort='AN',
    #            title=title,
    #            now_playing=row[6],
    #        )
    #        new_info.save()

    #old_db = epi_info_sql()
    #for row in old_db:
    #    if not Info.objects.filter(title=row[2]):
    #        new_info = Info(
    #            sort='EP',
    #            title=row[2],
    #            now_playing=row[6],
    #        )
    #        new_info.save()
    return True


def newTags():
    json1 = {"type": "format", "items": ["mp4", "rmvb", "mkv", "rm", "avi", "flv", "m4a"]}
    json2 = {"type": "others",
             "items": ["x264", "flac", "hi10p", "aac", "10bit", "8bit", "avc", "PSP_PC", "psp", "2acc", "pc", "psv",
                       "BDMV", "PSP兼容"]}
    json3 = {"type": "rip", "items": ["bdrip", "tvrip", "dvdrip", "hdtv"]}
    json4 = {"type": "subgroup", "items": ["异域动漫", "TSDM字幕组", "千夏字幕组", "DHR动研字幕组", "动音漫影", "恶魔岛字幕组"
        , "猪猪字幕组", "极影字幕社", "澄空学园", "流云字幕组", "诸神kamigami字", "轻之国度", "华盟字幕社", "幻樱字幕组", "动漫国字幕组"
        , "雪酷字幕组", "风之圣殿", "ACT-SUB", "动漫FANS字幕组", "自由字幕组", "微笑字幕组", "白恋字幕组", "天使动漫论坛", "夜莺工作室", "生徒会字幕组",
                                           "ANK-Project", "WOLF字幕组", "DA同音爱漫", "旋风字幕组", "天の字幕组", "幻龙字幕组", "极速字幕工作",
                                           "悠哈C9字幕社", "雪飘工作室", "梦幻恋樱", "SOSG字幕团", "萌月字幕组", "THK字幕组", "动漫先锋",
                                           "Sakura Cafe", "听潺社", "光荣字幕组", "星尘字幕组", "RH字幕组", "HKACG香港动漫", "曙光社字幕组",
                                           "枫雪连载制作", "四魂制作组", "漫猫字幕组", "漫盟之影字幕", "幻之字幕组", "HKG字幕组", "W-zone字幕组",
                                           "摇篮字幕组", "TAMASHII字幕组", "A.I.R.nesSub", "Astral", "Union", "漫游字幕组", "你妹发佈",
                                           "夏砂字幕组", "太古遗产", "柯南事务所", "BBA字幕组", "勇气字幕组", "琵琶行字幕组", "梦幻旋律", "KRL字幕组",
                                           "紫音动漫&发佈", "风车字幕组", "天使字幕组", "HSQ-rip组", "Sphere-HoLic", "铃风字幕组", "天空字幕组",
                                           "萌猫同好会", "无根之树分享", "漫娱论坛", "月光恋曲字幕", "恋爱糖霜字幕", "乌贼发佈", "萌幻字幕组", "WHITE",
                                           "MOON", "幻想字幕组", "圣域字幕组", "夏雪字幕组", "萌网", "星光字幕组", "傲娇字幕组", "2次元字幕组",
                                           "NTR字幕组", "AQUA工作室", "KIDFansClub", "音乐@花园", "异域-11番小队", "GAL-Sora论坛",
                                           "汐染字幕社", "指尖奶茶应援", "动萌字幕组", "卡通空间", "游风字幕组", "宅结界汉化组", "吖吖日剧字幕", "JPSEEK",
                                           "米花学园汉化", "月舞字幕组", "水晶海汉化组", "白选馆汉化组", "漫游FREEWIND", "C2Club", "梦域理想乡",
                                           "枫组@花园", "下午茶字幕组", "K2字幕组", "萌动漫字幕组", "紫月发佈组", "黑白映画字幕", "永恒动漫", "中国废柴协会",
                                           "ANK-Raws", "暮秋夏夜の部", "空岛字幕组", "自压组", "花园奥义社团", "散漫字幕组", "繁体动画字幕", "字幕千本桜",
                                           "银光字幕组", "WLGO", "DA同音字幕组", "光荣", "galaxy", "白月字幕", "Dymy字幕组", "千夏字幕組",
                                           "漫樱字幕", "悠哈璃羽字幕社", "YYeTs人人影视", "OPFans枫雪动漫", "HKG", "启萌字幕组",
                                           "诸神字幕组", "SumiSora", "FLSnow", "AcgmTHK字幕社", "天空树中日双语字幕组", "Gauss字幕组", "J2",
                                           "Comicat", "RH", "异域字幕组", "百度字幕", "EPClub", "Sphere HoLic", "U2-Rip",
                                           "天夜字幕组"]}

    for row in json3['items']:
        if not Tags.objects.filter(sort='EP', title__contains=row):
            print(row)
            tags = [row.upper(), row.lower()]
            new_tag = Tags(
                sort='EP',
                title=row,
                style='CL',
                tags=json.dumps(tags)
            )
            new_tag.save()
