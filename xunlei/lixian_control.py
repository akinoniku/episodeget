from xunlei.lixian import XunleiClient


def add_task(user, rss):
    xunlei = XunleiClient(username='acgclub', password='a15017509396', cookie_path='acgclub')
    xunlei.add_torrent_task_by_link(rss.link)
