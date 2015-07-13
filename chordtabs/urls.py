from django.conf.urls import patterns, include, url
from django.contrib import admin
from viewer import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chordtabs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.homepage),
    url(r'^refresh/$', views.refresh),
    url(r'^favorite/$', views.favorite),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^search/(\w+)/$', views.search),
    url(r'^view_chord/(\w+)/$', views.view_chord),
)
