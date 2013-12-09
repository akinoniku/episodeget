from user_settings.models import Xunlei
from xunlei.lixian import XunleiClient

def add_user(user, xunlei_id, xunlei_pass):
    try:
        if not len(Xunlei.objects.filter(user=user)):
            xunlei = Xunlei(
                user=user,
                xunlei_id=xunlei_id,
                xunlei_pass=xunlei_pass,
            )
            xunlei.save()
        XunleiClient(username=xunlei_id, password=xunlei_pass)
        return True
    except Exception, data:
        qq = data.message
        return False

def add_task(user, rss):
    try:
        xunlei_user = Xunlei.objects.get(user=user)
        xunlei = XunleiClient(username=xunlei_user.xunlei_id, password=xunlei_user.xunlei_pass,
                              cookie_path=xunlei_user.xunlei_id)
        xunlei.add_torrent_task_by_link(rss.link)
        return True
    except:
        return False
