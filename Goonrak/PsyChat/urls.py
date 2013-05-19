from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    r'^/update/$', 'PsyChat.views.update',
)
