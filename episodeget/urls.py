from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from feeds_analysis.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'episodeget.views.home', name='home'),
                       # url(r'^episodeget/', include('episodeget.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^get_ani_rss$', get_ani_rss),
                       url(r'^get_epi_rss$', get_epi_rss),
                       url(r'^get_ani_new$', get_ani_new),
                       url(r'^get_epi_new$', get_epi_new),
                       url(r'^ana_rss/(\d+)$', ana_rss),
                       url(r'^ana_rss_all$', ana_rss_all),
                       url(r'^read_old_db$', read_old_db),
)
