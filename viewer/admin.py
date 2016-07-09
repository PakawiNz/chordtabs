from django.contrib import admin
from .models import User,Song

# Register your models here.

class UserAdmin(admin.ModelAdmin):
	field = ('username','password')

class SongAdmin(admin.ModelAdmin):
	pass

admin.register(User,UserAdmin)
admin.register(Song,SongAdmin)