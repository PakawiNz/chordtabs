import datetime

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from viewer.models import Song, RoomItem, Room
from viewer.serializers import SongSerializer


def index(request):
    return render(request, 'index.html')


class SongViewSet(ReadOnlyModelViewSet):
    queryset = Song.objects.all().exclude(chord_url='')
    serializer_class = SongSerializer

    def filter_queryset(self, queryset):
        room = self.request.query_params.get('room')
        if room:
            items = RoomItem.objects.filter(room__code=room).values('song')
            queryset = queryset.filter(pk__in=items)

        description = self.request.query_params.get('description')
        if description:
            queryset = queryset.filter(description__contains=description)

        return queryset[:50]

    @action(detail=True)
    def cache_song(self, request, pk=None):
        Song.objects.get(pk=pk).get_remote_chord()
        return Response('success')


def create_room(request):
    code = datetime.datetime.now().timestamp()
    code = int(code)
    Room.objects.create(code=code)
    return HttpResponse(code)


def add_to_room(request, room, song):
    room = Room.objects.get(code=room)
    song = Song.objects.get(id=song)
    RoomItem.objects.create(room=room, song=song)
    return HttpResponse('')


def remove_from_room(request, room, song):
    RoomItem.objects.filter(room__code=room, song__id=song).delete()
    return HttpResponse('')
