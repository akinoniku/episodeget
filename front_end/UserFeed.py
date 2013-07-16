# coding=utf-8
from django.contrib.syndication.views import Feed
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.template import loader, TemplateDoesNotExist, RequestContext
from django.utils import feedgenerator, tzinfo
from django.utils.encoding import smart_text
from django.utils.timezone import is_naive

from front_end.views import rss_feed


class UserFeed(Feed):
    title = "星祈娘"
    link = 'magnet:?xt=urn:btih:'
    domain = 'xingqiniang.com'
    description = "这是星祈娘生成的RSS订阅"

    def get_object(self, request, userId):
        result = rss_feed(userId)
        return result

    def items(self, obj):
        return obj

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.title

    def item_link(self, item):
        return item.link

    def __get_dynamic_attr(self, attname, obj, default=None):
        try:
            attr = getattr(self, attname)
        except AttributeError:
            return default
        if callable(attr):
            # Check __code__.co_argcount rather than try/excepting the
            # function and catching the TypeError, because something inside
            # the function may raise the TypeError. This technique is more
            # accurate.
            if hasattr(attr, '__code__'):
                argcount = attr.__code__.co_argcount
            else:
                argcount = attr.__call__.__code__.co_argcount
            if argcount == 2: # one argument is 'self'
                return attr(obj)
            else:
                return attr()
        return attr

    def get_feed(self, obj, request):
        """
        Returns a feedgenerator.DefaultFeed object, fully populated, for
        this feed. Raises FeedDoesNotExist for invalid parameters.
        """
        current_site = get_current_site(request)

        link = self.__get_dynamic_attr('link', obj).decode('utf-8')
        #link = add_domain(current_site.domain, link, request.is_secure())

        feed = self.feed_type(
            title = self.__get_dynamic_attr('title', obj),
            subtitle = self.__get_dynamic_attr('subtitle', obj),
            link = link.decode('utf-8'),
            description = self.__get_dynamic_attr('description', obj),
            language = settings.LANGUAGE_CODE,
            feed_url =  self.__get_dynamic_attr('feed_url', obj) or request.path,
            author_name = self.__get_dynamic_attr('author_name', obj),
            author_link = self.__get_dynamic_attr('author_link', obj),
            author_email = self.__get_dynamic_attr('author_email', obj),
            categories = self.__get_dynamic_attr('categories', obj),
            feed_copyright = self.__get_dynamic_attr('feed_copyright', obj),
            feed_guid = self.__get_dynamic_attr('feed_guid', obj),
            ttl = self.__get_dynamic_attr('ttl', obj),
            **self.feed_extra_kwargs(obj)
        )

        title_tmp = None
        if self.title_template is not None:
            try:
                title_tmp = loader.get_template(self.title_template)
            except TemplateDoesNotExist:
                pass

        description_tmp = None
        if self.description_template is not None:
            try:
                description_tmp = loader.get_template(self.description_template)
            except TemplateDoesNotExist:
                pass

        for item in self.__get_dynamic_attr('items', obj):
            if title_tmp is not None:
                title = title_tmp.render(RequestContext(request, {'obj': item, 'site': current_site}))
            else:
                title = self.__get_dynamic_attr('item_title', item)
            if description_tmp is not None:
                description = description_tmp.render(RequestContext(request, {'obj': item, 'site': current_site}))
            else:
                description = self.__get_dynamic_attr('item_description', item)
                link = self.__get_dynamic_attr('item_link', item).decode('utf-8'),
            enc = None
            enc_url = self.__get_dynamic_attr('item_enclosure_url', item)
            if enc_url:
                enc = feedgenerator.Enclosure(
                    url = smart_text(enc_url),
                    length = smart_text(self.__get_dynamic_attr('item_enclosure_length', item)),
                    mime_type = smart_text(self.__get_dynamic_attr('item_enclosure_mime_type', item))
                )
            author_name = self.__get_dynamic_attr('item_author_name', item)
            if author_name is not None:
                author_email = self.__get_dynamic_attr('item_author_email', item)
                author_link = self.__get_dynamic_attr('item_author_link', item)
            else:
                author_email = author_link = None

            pubdate = self.__get_dynamic_attr('item_pubdate', item)
            if pubdate and is_naive(pubdate):
                ltz = tzinfo.LocalTimezone(pubdate)
                pubdate = pubdate.replace(tzinfo=ltz)
            link = link[0]

            feed.add_item(
                title = title,
                link = link.decode('utf-8'),
                description = description,
                unique_id = self.__get_dynamic_attr('item_guid', item, link),
                enclosure = enc,
                pubdate = pubdate,
                author_name = author_name,
                author_email = author_email,
                author_link = author_link,
                categories = self.__get_dynamic_attr('item_categories', item),
                item_copyright = self.__get_dynamic_attr('item_copyright', item),
                **self.item_extra_kwargs(item)
            )
        return feed
