from django.db import models

# Create your models here.

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
	code = models.IntegerField(unique=True,default=0)
	name = models.TextField(default="")
	artist = models.ForeignKey('Artist',default=None,null=True)
	album = models.ForeignKey('Album',default=None,null=True)
	description = models.TextField(default="")
	chord = models.ImageField(default="")
	viewed = models.ManyToManyField('User', through='View')

class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.EmailField(unique=True,max_length=50)
	password = models.CharField(max_length=50)
	displayname = models.CharField(max_length=50)

class View(models.Model):
	id = models.AutoField(primary_key=True)
	song = models.ForeignKey('Song')
	user = models.ForeignKey('User')
	count = models.IntegerField(default=0)
	isFavorite = models.BooleanField(default=False)
