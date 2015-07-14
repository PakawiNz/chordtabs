from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os,urllib2,shutil

# Create your models here.
CHORDTABS_OLD_DIR = 'E:\Downloads\Chords'
CHORDTABS_NEW_DIR = 'C:\Workspace\chordtabs\media'

def _copyfromoldproject():
	_all = Song.objects.all().values_list('chord_image',flat=True)
	for path in _all :
		path = os.path.join(CHORDTABS_NEW_DIR,path)
		condition = not os.path.isfile(path) or os.stat(path).st_size < 10000
		if condition :
			afile = os.path.basename(path)
			oldpath = os.path.join(CHORDTABS_OLD_DIR,'c' + afile)
			if os.path.isfile(oldpath) :
				print path,oldpath
				shutil.copyfile(oldpath,path)

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
	chord_image = models.ImageField(default="",upload_to='chords')
	chord_url = models.URLField(default="")

	def get_remote_chord(self):
		if not self.chord_url :
			return

		if not self.chord_image or not os.path.isfile(self.chord_image.path):
			filename = os.path.basename(self.chord_url)
			oldpath = os.path.join(CHORDTABS_OLD_DIR,'c' + filename)

			img_temp = NamedTemporaryFile()
			img_temp.write(urllib2.urlopen(self.chord_url).read())
			img_temp.flush()

			self.chord_image.save(filename,File(img_temp))
			self.save()

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
