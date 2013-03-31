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
