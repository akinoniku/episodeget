from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from feeds_analysis.views import *
from front_end import views
import front_end

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'episodeget.views.home', name='home'),
                       # url(r'^episodeget/', include('episodeget.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       # front_end
                       url(r'^i$', front_end.views.index),
                       url(r'^index.manifest$', front_end.views.index_manifest),

                       # feed_analysis
                       url(r'^update_all$', update_all),
                       url(r'^ana_rss/(\d+)$', ana_rss),
                       url(r'^ana_rss_all$', ana_rss_all),
                       url(r'^read_old_db$', read_old_db),
                       url(r'^add_task$', add_task_test),

                       # rest
                       url(r'^rss/$', RssList.as_view(), name='rss-list'),
                       url(r'^rss/(?P<pk>\d+)/$', RssDetail.as_view(), name='rss-detail'),

                       # social auth
                       url(r'', include('social_auth.urls')),

                       # test function
                       url(r'init_test', init_test),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += patterns('', url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')))
