from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'Goonrak.views.home'),

    # user auth urls
    url(r'^accounts/login/$', 'Goonrak.views.login'),
    url(r'^accounts/auth/$', 'Goonrak.views.auth_view'),
    url(r'^accounts/logout/$', 'Goonrak.views.logout'),
    url(r'^accounts/register/$', 'Goonrak.views.register_user'),
    # url(r'^Goonrak/', include('Goonrak.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # psyChat app    
    url(r'^psychat/', include( 'PsyChat.urls' )),
)
