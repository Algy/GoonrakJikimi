from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^update/$', 'PsyChat.views.update'),
    url(r'^downdate/$', 'PsyChat.views.downdate'),
    url(r'^send/$', 'PsyChat.views.send'),
    url(r'^$', 'PsyChat.views.default'),
    url(r'^startbot/$', 'PsyChat.views.startBot'),
)