from feeds_analysis.models import SubList

__author__ = 'akino'


def collect_sublist_by_info(info):
    """

    :param info: FeedInfo
    """
    all_info = SubList.objects.filter(feed_info=info)