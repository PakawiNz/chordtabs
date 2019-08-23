from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from viewer.views import SongViewSet, create_room, add_to_room, remove_from_room, index

router = routers.SimpleRouter()
router.register(r'api/songs', SongViewSet)

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api/create_room/', create_room),
    path('api/add_to_room/<int:room>/<int:song>/', add_to_room),
    path('api/remove_from_room/<int:room>/<int:song>/', remove_from_room),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
