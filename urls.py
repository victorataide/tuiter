from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tuiter/', include('tuiter.foo.urls')),
    (r'^$', 'tuiter.microblog.views.index'),
    (r'^login$', 'tuiter.microblog.views.login'),
    (r'^logout$', 'tuiter.microblog.views.logout'),
    (r'^signup$', 'tuiter.microblog.views.signup'),
    (r'^dopost$', 'tuiter.microblog.views.dopost'),
    (r'^whotofollow$', 'tuiter.microblog.views.whotofollow'),
    (r'^follow$', 'tuiter.microblog.views.follow'),
    (r'^userpage$', 'tuiter.microblog.views.userpage'),
    (r'^search$', 'tuiter.microblog.views.search'),
    (r'^error$', 'tuiter.microblog.views.search'),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/victor/projects/tuiter/media'}),


    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
