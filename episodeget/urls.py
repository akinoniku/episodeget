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
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       # user setting
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'front_end/login_form.html'}),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
                       url(r'^accounts/reg/$', front_end.views.user_reg),
                       url(r'^accounts/prefer/$', front_end.views.user_prefer_list),
                       url(r'^accounts/xunlei/$', front_end.views.user_xunlei),
                       url(r'^accounts/$', front_end.views.user_account),
                       url(r'^accounts/login/ajax/$', front_end.views.login_ajax),
                       url(r'^accounts/current/$', front_end.views.get_current_user),
                       # url(r'^accounts/login/fail/$', front_end.views.login_fail),

                       # front_end
                       url(r'^$', front_end.views.index),
                       url(r'^index.manifest$', front_end.views.index_manifest),
                       # url(r'^list/(AN|EP|an|ep)$', front_end.views.info_list),
                       # url(r'^view/(\d+)$', front_end.views.info_view),
                       # url(r'^list_ajax/$', front_end.views.get_sub_list_rss),
                       url(r'^add_list_ajax/$', front_end.views.add_sub_list),
                       url(r'^remove_list_ajax/$', front_end.views.remove_sub_list),
                       url(r'^rss_feed/$', front_end.views.rss_feed),

                       # feed_analysis
                       url(r'^update_all$', update_all),
                       url(r'^ana_rss/(\d+)$', ana_rss),
                       url(r'^ana_rss_all$', ana_rss_all),
                       url(r'^read_old_db$', read_old_db),
                       url(r'^add_task$', add_task_test),
                       url(r'^test_notification$', test_notification),


                       # rest
                       url(r'^rss/$', RssList.as_view(), name='rss-list'),
                       url(r'^rss/(?P<pk>\d+)/$', RssDetail.as_view(), name='rss-detail'),
                       url(r'^info/$', InfoList.as_view(), name='info-list'),
                       url(r'^info/(?P<pk>\d+)/$', InfoDetail.as_view(), name='info-detail'),
                       url(r'^tags/$', TagsList.as_view(), name='tags-list'),
                       url(r'^tags/(?P<pk>\d+)/$', TagsDetail.as_view(), name='tags-detail'),
                       url(r'^user/$', UserList.as_view(), name='user-list'),
                       url(r'^user/(?P<pk>\d+)/$', UserDetail.as_view(), name='user-detail'),
                       url(r'^sub_list/$', SubListList.as_view(), name='sublist-list'),
                       url(r'^sub_list/(?P<pk>\d+)/$', SubListDetail.as_view(), name='sublist-detail'),

                       # social auth
                       url(r'', include('social_auth.urls')),

                       # test function
                       # url(r'init_test', init_test),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += patterns('', url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')))
