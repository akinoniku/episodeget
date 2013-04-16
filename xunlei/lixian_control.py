from user_settings.models import Xunlei
from xunlei.lixian import XunleiClient


def add_task(user, rss):
    xunlei_user = Xunlei.objects.get(user=user)
    xunlei = XunleiClient(username=xunlei_user.xunlei_id, password=xunlei_user.xunlei_pass,
                          cookie_path=xunlei_user.xunlei_id)
    xunlei.add_torrent_task_by_link(rss.link)
