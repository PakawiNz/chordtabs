import os
import urllib.request

from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.IntegerField(unique=True, default=0)
    name = models.TextField(default="")
    artist = models.ForeignKey('Artist', models.CASCADE, default=None, null=True)
    album = models.ForeignKey('Album', models.CASCADE, default=None, null=True)
    description = models.TextField(default="")
    chord_image = models.ImageField(default="", upload_to='chords')
    chord_url = models.URLField(default="")

    def get_remote_chord(self):
        if not self.chord_url:
            return

        if not self.chord_image or not os.path.isfile(self.chord_image.path):
            filename = os.path.basename(self.chord_url)

            img_temp = NamedTemporaryFile()
            img_temp.write(urllib.request.urlopen(self.chord_url).read())
            img_temp.flush()

            self.chord_image.save(filename, File(img_temp))
            self.save()


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.EmailField(unique=True, max_length=50)
    password = models.CharField(max_length=50)
    displayname = models.CharField(max_length=50)


class View(models.Model):
    id = models.AutoField(primary_key=True)
    song = models.ForeignKey('Song', models.CASCADE, related_name='views')
    user = models.ForeignKey('User', models.CASCADE, null=True)
    count = models.IntegerField(default=0)
    isFavorite = models.BooleanField(default=False)


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('User', models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()

    class META:
        unique_together = (('owner', 'name'),)


class PlaylistItem(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    song = models.ForeignKey('Song', models.CASCADE)
    playlist = models.ForeignKey('Playlist', models.CASCADE, related_name='items')

    class META:
        unique_together = (('number', 'playlist'), ('song', 'playlist'))


class Room(models.Model):
    code = models.CharField(max_length=100)

class RoomItem(models.Model):
    room = models.ForeignKey('Room', models.CASCADE)
    song = models.ForeignKey('Song', models.CASCADE)
