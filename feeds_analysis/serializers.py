from rest_framework import serializers
from feeds_analysis.models import Info, Tags, Rss, Douban, SubList


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        # fields = ('id', 'sort', 'title', 'tags', 'douban', 'weekday', 'bgm_count', 'now_playing', 'image')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        # fields = ('id', 'sort', 'title', 'style', 'tags')


class RssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rss
        # fields = ('id', 'sort', 'title', 'link', 'hash_code', 'episode_id', 'timestamp')


class DoubanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Douban
        # fields = ('id', 'title', 'aka', 'original_title', 'alt', 'countries', 'current_season',
        #           'directors', 'genres', 'images', 'douban_id', 'average', 'episodes_count', 'summary', 'year')


class SubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubList
        # fields = ('id', 'sort', 'tags_index', 'info', 'tags', 'rss', 'user', 'create_time', 'update_time')
