from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from viewer import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chordtabs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.homepage),
    url(r'^refresh/$', views.refresh),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),

    url(r'^view_playlist/(\w+)/$', views.view_playlist),
    url(r'^view_chord/(\w+)/$', views.view_chord),
    url(r'^favorite/$', views.favorite),
    url(r'^playlist/$', views.playlist),
    url(r'^search/', views.search),
    
    url(r'^set_favorite/(\w+)/$', views.set_favorite),
    url(r'^unset_favorite/(\w+)/$', views.unset_favorite),

    url(r'^get-playlist/$', views.get_playlist),
    url(r'^new-playlist/$', views.new_playlist),
    url(r'^del-playlist/(\w+)/$', views.del_playlist),
    url(r'^add-to-playlist/$', views.add_to_playlist),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))