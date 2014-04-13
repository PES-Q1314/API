from api.api import api
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponse


def home(request):
    html = "<html><body>API: <a href='/api/'></a></body></html>"
    return HttpResponse(html)


urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^', include(api.urls))
)


urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.STATIC_ROOT, 'show_indexes': True, }),
)